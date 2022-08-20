%define _build_id_links none

%undefine _auto_set_build_flags

%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 3
%global ROCM_MAGIC_VERSION 109
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50203
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCM_COMGR_GIT https://github.com/RadeonOpenCompute/ROCm-CompilerSupport

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
BuildRequires:      rocm-device-libs

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
Name:          comgr
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}.2
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

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_COMGR_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/comgr
cd %{ROCM_BUILD_DIR}/comgr
pushd .


# Level 2 : Build

cd %{ROCM_BUILD_DIR}/comgr

    CC=/opt/rocm/llvm/bin/clang CXX=/opt/rocm/llvm/bin/clang++ CXXFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' CFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
    cmake -GNinja -S "%{ROCM_GIT_DIR}/ROCm-CompilerSupport/lib/comgr" \
    -B build -Wno-dev \
    -DCMAKE_INSTALL_PREFIX=%{ROCM_INSTALL_DIR} \
    -DCMAKE_PREFIX_PATH="%{ROCM_INSTALL_DIR}/llvm;%{ROCM_INSTALL_DIR}"
    cd ./build
    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/amd_comgr.h
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib64/cmake/amd_comgr/amd_comgr*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib64/libamd_comgr*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/amd_comgr/LICENSE.txt
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/amd_comgr/NOTICES.txt
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/amd_comgr/README.md
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/amd_comgr/comgr/LICENSE.txt

%exclude /src
