%define _build_id_links none


%global pkgname rocm-core
%global pkgver %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
%global builddir %{_builddir}/%{pkgname}-%{pkgver}
%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 3
%global ROCM_MAGIC_VERSION 109
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_GLOBAL_DIR /opt/rocm
%global ROCM_LIBPATCH_VERSION 50203
%global ROCM_GIT_DIR %{builddir}/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{builddir}/rocm-build/build
%global ROCM_PATCH_DIR %{builddir}/rocm-build/patch


BuildRequires: wget

Requires:      libc.so.6()(64bit)
Requires:      libc.so.6(GLIBC_2.2.5)(64bit)
Requires:      libgcc_s.so.1()(64bit)
Requires:      libstdc++.so.6()(64bit)

Provides:      librocm-core.so.1()(64bit)
Provides:      rocm-core
Provides:      rocm-core(x86-64)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute (ROCm) Runtime software stack

%description
Radeon Open Compute (ROCm) Runtime software stack

%build

# Level 1 : Create versioning from official packaging

## file N1 from official repos (rocm-core) :

mkdir -p %{buildroot}%{ROCM_INSTALL_DIR}/.info

touch %{buildroot}%{ROCM_INSTALL_DIR}/.info/version

echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}%{ROCM_INSTALL_DIR}/.info/version

#

## file N2 from official repos (rocm-core) :

mkdir -p %{buildroot}%{ROCM_INSTALL_DIR}/include

touch %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm_version.h

echo '#ifndef ROCMCORE_WRAPPER_INCLUDE_ROCM_VERSION_H' > %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm_version.h
echo '#define ROCMCORE_WRAPPER_INCLUDE_ROCM_VERSION_H' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm_version.h
echo '#pragma message("This file is deprecated. Use file from include path %{ROCM_GLOBAL_DIR}-ver/include/ and prefix with rocm-core")' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm_version.h
echo '#include "rocm-core/rocm_version.h"' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm_version.h
echo '#endif' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm_version.h

#

## file N3 from official repos (rocm-core) :

mkdir -p %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core

touch %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h

echo '#ifndef _ROCM_VERSION_H_' > %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '#define _ROCM_VERSION_H_' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '#ifdef __cplusplus' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo 'extern "C" {' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '#endif' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo "#define ROCM_VERSION_MAJOR   %{ROCM_MAJOR_VERSION}" >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo "#define ROCM_VERSION_MINOR   %{ROCM_MINOR_VERSION}" >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo "#define ROCM_VERSION_PATCH   %{ROCM_PATCH_VERSION}" >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo 'typedef enum {' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '	VerSuccess=0,' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '	VerIncorrecPararmeters,' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '	VerValuesNotDefined,' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '	VerErrorMAX' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '} VerErrors;' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo 'VerErrors getROCmVersion(unsigned int* Major, unsigned int* Minor, unsigned int* Patch) __attribute__((nonnull)) ;' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '#ifdef __cplusplus' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '#endif' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
echo '#endif' >> %{buildroot}%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h

# Level 2 : Add config & package

mkdir -p %{buildroot}/etc/ld.so.conf.d
touch %{buildroot}/etc/ld.so.conf.d/10-rocm-core.conf
echo %{ROCM_GLOBAL_DIR}/%{_lib} >> %{buildroot}/etc/ld.so.conf.d/10-rocm-core.conf
mkdir -p %{buildroot}/etc/profile.d
touch %{buildroot}/etc/profile.d/rocm-core.sh
echo  "export ROC_ENABLE_PRE_VEGA=1"  >  %{buildroot}/etc/profile.d/rocm-core.sh
echo  'export PATH=$PATH:%{ROCM_GLOBAL_DIR}/bin:%{ROCM_GLOBAL_DIR}/rocprofiler/bin:%{ROCM_GLOBAL_DIR}/opencl/bin' >>  %{buildroot}/etc/profile.d/rocm-core.sh
mkdir -p %{buildroot}/etc/udev/rules.d/
touch %{buildroot}/etc/udev/rules.d/70-kfd.rules
echo 'SUBSYSTEM=="kfd", KERNEL=="kfd", TAG+="uaccess", GROUP="video"' | tee %{buildroot}/etc/udev/rules.d/70-kfd.rules
chmod +x %{buildroot}/etc/profile.d/rocm-core.sh
ln -s %{ROCM_INSTALL_DIR} %{buildroot}%{ROCM_GLOBAL_DIR}

%files
/etc/ld.so.conf.d/10-rocm-core.conf
/etc/udev/rules.d/70-kfd.rules
/etc/profile.d/rocm-core.sh
%{ROCM_GLOBAL_DIR}
%{ROCM_INSTALL_DIR}/include/rocm-core/rocm_version.h
%{ROCM_INSTALL_DIR}/include/rocm_version.h
%{ROCM_INSTALL_DIR}/.info/version
%exclude %{ROCM_INSTALL_DIR}/rocm_version.h

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

