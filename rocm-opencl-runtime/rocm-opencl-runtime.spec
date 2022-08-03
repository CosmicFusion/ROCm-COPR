%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCCLR_GIT https://github.com/ROCm-Developer-Tools/ROCclr.git
%global ROCM_OCL_GIT https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime.git
%global ROCM_PATCH_1 rocclr-gfx803.patch



BuildRequires: clang
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: libglvnd-devel
BuildRequires: numactl-devel
BuildRequires: numactl
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: wget

Provides:      rocm-opencl
Provides:      rocm-opencl(x86-64)
Provides:      rocm-ocl-icd
Provides:      rocm-ocl-icd
Requires:      comgr
Requires:      hsa-rocr


Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-opencl-runtime
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       MIT and ASL 2.0
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - OpenCL runtime

%description
 Radeon Open Compute - OpenCL runtime

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCCLR_GIT}"

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_OCL_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocm-opencl-runtime
cd %{ROCM_BUILD_DIR}/rocm-opencl-runtime
pushd .

# Level 2 : GFX8 PATCH

cd %{ROCM_PATCH_DIR}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-opencl-runtime/%{ROCM_PATCH_1}

cd %{ROCM_GIT_DIR}/ROCclr
git reset --hard
git apply %{ROCM_PATCH_DIR}/rocclr-gfx803.patch


# Level 3 : Build

cd %{ROCM_BUILD_DIR}/rocm-opencl-runtime

cmake \
    -DCMAKE_PREFIX_PATH="%{ROCM_INSTALL_DIR}/opencl" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}/opencl" \
    -Dhsa-runtime64_DIR=%{ROCM_INSTALL_DIR}/lib/cmake/hsa-runtime64 \
    %{ROCM_GIT_DIR}/ROCm-OpenCL-Runtime
    make -j$(nproc)

# Level 4 : Package

DESTDIR=%{buildroot} make install

mkdir -p %{buildroot}/etc/OpenCL/vendors
touch %{buildroot}/etc/OpenCL/vendors/amdocl64.icd
echo libamdocl64.so > %{buildroot}/etc/OpenCL/vendors/amdocl64.icd
rm -r %{buildroot}/%{ROCM_INSTALL_DIR}/opencl/opencl
mkdir -p %{buildroot}/etc/ld.so.conf.d
touch %{buildroot}/etc/ld.so.conf.d/10-rocm-opencl.conf
echo /opt/rocm/opencl/lib > %{buildroot}/etc/ld.so.conf.d/10-rocm-opencl.conf

%files
%{ROCM_INSTALL_DIR}/opencl/bin/clinfo
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl2.hpp
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_dx9_media_sharing_intel.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_ext.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_ext_intel.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_gl_ext.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_gl.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl.hpp
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_icd.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_platform.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_va_api_media_sharing_intel.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_version.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/opencl.h
%{ROCM_INSTALL_DIR}/opencl/lib/libamdocl64.so
%{ROCM_INSTALL_DIR}/opencl/lib/libcltrace.so
%{ROCM_INSTALL_DIR}/opencl/lib/libOpenCL.so
%{ROCM_INSTALL_DIR}/opencl/lib/libOpenCL.so.1
%{ROCM_INSTALL_DIR}/opencl/lib/libOpenCL.so.1.2
%{ROCM_INSTALL_DIR}/opencl/share/doc/opencl/LICENSE*
%{ROCM_INSTALL_DIR}/opencl/share/doc/rocm-ocl-icd/LICENSE*
/etc/ld.so.conf.d/10-rocm-opencl.conf
/etc/OpenCL/vendors/amdocl64.icd
%exclude /src

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
