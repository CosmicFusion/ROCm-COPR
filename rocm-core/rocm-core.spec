%define _build_id_links none

%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_MAGIC_VERSION 79
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCCLR_GIT https://github.com/ROCm-Developer-Tools/ROCclr.git
%global ROCM_OCL_GIT https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime.git
%global ROCM_PATCH_1 rocclr-gfx803.patch


BuildRequires: wget

Requires:      libc.so.6()(64bit)
Requires:      libc.so.6(GLIBC_2.2.5)(64bit)
Requires:      libgcc_s.so.1()(64bit)
Requires:      libm.so.6()(64bit)
Requires:      librocm-core.so.1()(64bit)
Requires:      libstdc++.so.6()(64bit)

Provides:      librocm-core.so.1()(64bit)
Provides:      rocm-core
Provides:      rocm-core(x86-64)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-core
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute (ROCm) Runtime software stack

%description
Radeon Open Compute (ROCm) Runtime software stack

%build

# Level 1 : Create versioning from official packaging

## file N1 from official repos (rocm-core) :

mkdir -p %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info

touch %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version

echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version

#

## file N2 from official repos (rocm-core) :

mkdir -p %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include

touch %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h

echo '#ifndef ROCMCORE_WRAPPER_INCLUDE_ROCM_VERSION_H' > %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h
echo '#define ROCMCORE_WRAPPER_INCLUDE_ROCM_VERSION_H' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h
echo '#pragma message("This file is deprecated. Use file from include path /opt/rocm-ver/include/ and prefix with rocm-core")' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h
echo '#include "rocm-core/rocm_version.h"' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h
echo '#endif' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h

#

## file N3 from official repos (rocm-core) :

mkdir -p %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core

touch %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h

echo '#ifndef _ROCM_VERSION_H_' > %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '#define _ROCM_VERSION_H_' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '#ifdef __cplusplus' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo 'extern "C" {' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '#endif' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo "#define ROCM_VERSION_MAJOR   %{ROCM_MAJOR_VERSION}" >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo "#define ROCM_VERSION_MINOR   %{ROCM_MINOR_VERSION}" >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo "#define ROCM_VERSION_PATCH   %{ROCM_PATCH_VERSION}" >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo 'typedef enum {' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '	VerSuccess=0,' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '	VerIncorrecPararmeters,' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '	VerValuesNotDefined,' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '	VerErrorMAX' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '} VerErrors;' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo 'VerErrors getROCmVersion(unsigned int* Major, unsigned int* Minor, unsigned int* Patch) __attribute__((nonnull)) ;' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '#ifdef __cplusplus' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '#endif' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
echo '#endif' >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h

# Level 2 : Add config & package

mkdir -p %{buildroot}/etc/ld.so.conf.d
touch %{buildroot}/etc/ld.so.conf.d/10-rocm-core.conf
echo /opt/rocm/lib > %{buildroot}/etc/ld.so.conf.d/10-rocm-core.conf
echo /opt/rocm/lib64 >> %{buildroot}/etc/ld.so.conf.d/10-rocm-core.conf
mkdir -p %{buildroot}/etc/profile.d
touch %{buildroot}/etc/profile.d/rocm-core.sh
echo  "export ROC_ENABLE_PRE_VEGA=1"  >  %{buildroot}/etc/profile.d/rocm-core.sh
echo  'export PATH=$PATH:/opt/rocm/bin:/opt/rocm/rocprofiler/bin:/opt/rocm/opencl/bin' >>  %{buildroot}/etc/profile.d/rocm-core.sh
touch %{buildroot}/etc/adduser.conf
echo 'ADD_EXTRA_GROUPS=1' | tee -a %{buildroot}/etc/adduser.conf
echo 'EXTRA_GROUPS=video' | tee -a %{buildroot}/etc/adduser.conf
echo 'EXTRA_GROUPS=render' | tee -a %{buildroot}/etc/adduser.conf
mkdir -p %{buildroot}/etc/udev/rules.d/
touch %{buildroot}/etc/udev/rules.d/70-kfd.rules
echo 'SUBSYSTEM=="kfd", KERNEL=="kfd", TAG+="uaccess", GROUP="video"' | tee %{buildroot}/etc/udev/rules.d/70-kfd.rules
chmod +x %{buildroot}/etc/profile.d/rocm-core.sh

%files
/etc/adduser.conf
/etc/ld.so.conf.d/10-rocm-core.conf
/etc/udev/rules.d/70-kfd.rules
/etc/profile.d/rocm-core.sh
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version
%exclude /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/rocm_version.h

%post
/sbin/ldconfig
ln -s /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION} /opt/rocm

%postun
/sbin/ldconfig
rm -r /opt/rocm
