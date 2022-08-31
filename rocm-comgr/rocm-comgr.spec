%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-comgr-devel
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
%global ROCM_GIT_URL_1 https://github.com/RadeonOpenCompute/ROCm-CompilerSupport

%global toolchain clang

Source0: %{ROCM_GIT_URL_1}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz

BuildRequires: rocm-llvm
BuildRequires: rocm-cmake
BuildRequires: ninja-build
BuildRequires: clang
BuildRequires: cmake
BuildRequires: numactl-devel
BuildRequires: numactl
BuildRequires: ncurses-devel
BuildRequires: pciutils-devel
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: vim-common
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: zlib-devel
BuildRequires: rocm-device-libs

Provides:      comgr
Provides:      comgr(x86-64)
Provides:      rocm-comgr
Provides:      rocm-comgr(x86-64)
Requires:      elfutils-libelf
Requires:      zlib
Requires:      rocm-device-libs
Requires:      rocm-core

Obsoletes:  	rocm-comgr
Obsoletes:  	rocm-comgr-devel

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - compiler support

%description
Radeon Open Compute - compiler support

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# Level 1 :  Extract

cd  %{ROCM_GIT_DIR}

tar -xf %{SOURCE0} -C ./

# Level 2 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}

    CC=/opt/rocm/llvm/bin/clang CXX=/opt/rocm/llvm/bin/clang++ CXXFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' CFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
    cmake -GNinja -S "%{ROCM_GIT_DIR}/ROCm-CompilerSupport-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}/lib/comgr" \
    -Wno-dev \
    -DCMAKE_INSTALL_PREFIX=%{ROCM_INSTALL_DIR} \
    -DCMAKE_PREFIX_PATH="%{ROCM_INSTALL_DIR}/llvm;%{ROCM_INSTALL_DIR}" \
    -DCMAKE_BUILD_TYPE=Release

ninja -j$(nproc)



# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
%{ROCM_INSTALL_DIR}/include/amd_comgr.h
%{ROCM_INSTALL_DIR}/lib/cmake/amd_comgr/amd_comgr*
%{ROCM_INSTALL_DIR}/lib/libamd_comgr*
%{ROCM_INSTALL_DIR}/share/amd_comgr/LICENSE.txt
%{ROCM_INSTALL_DIR}/share/amd_comgr/NOTICES.txt
%{ROCM_INSTALL_DIR}/share/amd_comgr/README.md
%{ROCM_INSTALL_DIR}/share/doc/amd_comgr/comgr/LICENSE.txt
