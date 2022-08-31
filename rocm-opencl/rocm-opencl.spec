%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-opencl
%global pkgver %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
%global builddir %{_builddir}/%{pkgname}-%{pkgver}
%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 3
%global GIT_MAJOR_VERSION 5
%global GIT_MINOR_VERSION 2
%global GIT_PATCH_VERSION 1
%global ROCM_MAGIC_VERSION 109
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_GLOBAL_DIR /opt/rocm
%global ROCM_LIBPATCH_VERSION 50203
%global ROCM_GIT_DIR %{builddir}/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{builddir}/rocm-build/build
%global ROCM_PATCH_DIR %{builddir}/rocm-build/patch
%global ROCM_GIT_URL_1 https://github.com/ROCm-Developer-Tools/ROCclr
%global ROCM_GIT_URL_2 https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime

%global toolchain clang

%global SRC0 rocclr-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz
%global SRC1 rocm-opencl-runtime-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz


BuildRequires:	binutils-devel
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	gnupg2
BuildRequires:	libedit-devel
BuildRequires:	libffi-devel
BuildRequires:	llvm-devel
BuildRequires:	multilib-rpm-config
BuildRequires:	ncurses-devel
BuildRequires:	ninja-build
BuildRequires:	python3-devel
BuildRequires:	python3-psutil
BuildRequires:	python3-recommonmark
BuildRequires:	python3-setuptools
BuildRequires:	python3-sphinx
BuildRequires: valgrind-devel
BuildRequires: zlib-devel
BuildRequires: rocm-comgr-devel
BuildRequires: clang
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: gcc-plugin-devel
BuildRequires: git
BuildRequires: rocm-hsa-devel
BuildRequires: rocm-hsakmt-roct-devel
BuildRequires: libdrm
BuildRequires: libdrm-devel
BuildRequires: libglvnd-devel
BuildRequires: libstdc++-devel
BuildRequires: ncurses-devel
BuildRequires: ninja-build
BuildRequires: numactl
BuildRequires: numactl-devel
BuildRequires: pciutils-devel
BuildRequires: perl
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: rocm-cmake
BuildRequires: rocm-device-libs
BuildRequires: rocm-llvm
BuildRequires: wget

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - OpenCL runtime

%description
Radeon Open Compute - OpenCL runtime

%package runtime
Requires:      rocm-comgr-devel
Requires:      rocm-core
Requires:      rocminfo
Requires:      hsa-rocr

Provides:      rocm-ocl-icd
Provides:      rocm-opencl
Provides:      rocm-ocl-icd(x86-64)
Provides:      rocm-opencl(x86-64)
Provides:      rocm-opencl-runtime
Provides:      rocm-opencl-runtime(x86-64)

Obsoletes:  	rocm-opencl

Summary:       Radeon Open Compute - OpenCL runtime

%description runtime
Radeon Open Compute - OpenCL runtime

%package devel
Requires:      rocm-comgr-devel
Requires:      rocm-core
Requires:      rocminfo
Requires:      rocm-opencl-runtime

Provides:      rocm-opencl-sdk
Provides:      rocm-opencl-devel
Provides:      rocm-opencl-sdk(x86-64)
Provides:      rocm-opencl-devel(x86-64)
Provides:      rocm-opencl-runtime-devel
Provides:      rocm-opencl-runtime-devel(x86-64)

Summary:       Radeon Open Compute - OpenCL runtime development kit

%description devel
Radeon Open Compute - OpenCL runtime development kit

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : Get sources

# URL 1 

cd %{_sourcedir}

ls %{SRC0} || echo "SRC 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_1}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz -O %{SRC0}

cd  %{ROCM_GIT_DIR}

rm -rf ./*

tar -xf %{_sourcedir}/%{SRC0} -C ./

# URL 2 

cd %{_sourcedir}

ls %{SRC1} || echo "SRC 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_2}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz -O %{SRC1}

cd  %{ROCM_GIT_DIR}

tar -xf %{_sourcedir}/%{SRC1} -C ./

# Level 2 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}

CC=clang CXX=clang++ \
cmake -Wno-dev -GNinja -S "%{ROCM_GIT_DIR}/ROCm-OpenCL-Runtime-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}" \
-DROCCLR_PATH="%{ROCM_GIT_DIR}/ROCclr-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}" \
-DAMD_OPENCL_PATH="%{ROCM_GIT_DIR}/ROCm-OpenCL-Runtime-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}" \
-DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
-DCMAKE_BUILD_TYPE=Release
    
ninja -j$(nproc)

# Level 4 : Package

DESTDIR=%{buildroot} ninja install

mkdir -p %{buildroot}/etc/OpenCL/vendors

touch %{buildroot}/etc/OpenCL/vendors/amdocl64.icd

echo libamdocl64.so > %{buildroot}/etc/OpenCL/vendors/amdocl64.icd

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-opencl.conf

echo %{ROCM_GLOBAL_DIR}/opencl/lib > %{buildroot}/etc/ld.so.conf.d/10-rocm-opencl.conf

mkdir -p %{buildroot}%{ROCM_INSTALL_DIR}/.info

touch %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-oclrt

echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-oclrt

mkdir -p %{buildroot}%{ROCM_INSTALL_DIR}/.info

touch %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-ocl-sdk

echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-ocl-sdk

%files runtime
# rocm-opencl
%{ROCM_INSTALL_DIR}/share/doc/opencl/LICENSE*
%{ROCM_INSTALL_DIR}/opencl/lib/lib*
%{ROCM_INSTALL_DIR}/opencl/bin/clinfo
%{ROCM_INSTALL_DIR}/lib/lib*
%{ROCM_INSTALL_DIR}/bin/clinfo
# rocm-ocl-icd
%{ROCM_INSTALL_DIR}/share/doc/rocm-ocl-icd/LICENSE*
%{ROCM_INSTALL_DIR}/opencl/lib/libOpen*
%{ROCM_INSTALL_DIR}/lib/libOpen*
# rocm-opencl-runtime
%{ROCM_INSTALL_DIR}/.info/version-oclrt
# system
/etc/ld.so.conf.d/10-rocm-opencl.conf
/etc/OpenCL/vendors/amdocl64.icd

%files devel
# rocm-opencl-devel
%{ROCM_INSTALL_DIR}/include/CL/cl.h
%{ROCM_INSTALL_DIR}/include/CL/cl.hpp
%{ROCM_INSTALL_DIR}/include/CL/cl2.hpp
%{ROCM_INSTALL_DIR}/include/CL/cl_dx9_media_sharing_intel.h
%{ROCM_INSTALL_DIR}/include/CL/cl_ext.h
%{ROCM_INSTALL_DIR}/include/CL/cl_ext_intel.h
%{ROCM_INSTALL_DIR}/include/CL/cl_gl.h
%{ROCM_INSTALL_DIR}/include/CL/cl_gl_ext.h
%{ROCM_INSTALL_DIR}/include/CL/cl_icd.h
%{ROCM_INSTALL_DIR}/include/CL/cl_platform.h
%{ROCM_INSTALL_DIR}/include/CL/cl_va_api_media_sharing_intel.h
%{ROCM_INSTALL_DIR}/include/CL/cl_version.h
%{ROCM_INSTALL_DIR}/include/CL/opencl.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl.hpp
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl2.hpp
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_dx9_media_sharing_intel.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_ext.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_ext_intel.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_gl.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_gl_ext.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_icd.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_platform.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_va_api_media_sharing_intel.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/cl_version.h
%{ROCM_INSTALL_DIR}/opencl/include/CL/opencl.h
# rocm-opencl-sdk
%{ROCM_INSTALL_DIR}/.info/version-ocl-sdk

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
