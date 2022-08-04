%undefine _auto_set_build_flags

%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCM_RDL_GIT https://github.com/RadeonOpenCompute/ROCm-Device-Libs

BuildRequires: boost-devel
BuildRequires: libstdc++-devel
BuildRequires: libcxx-devel
BuildRequires: clang
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: rocm-llvm
BuildRequires: rocm-cmake
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
BuildRequires: gcc-plugin-devel
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	ninja-build
BuildRequires:	zlib-devel
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	python3-psutil
BuildRequires:	python3-sphinx
BuildRequires:	python3-recommonmark
BuildRequires:	multilib-rpm-config
BuildRequires:	binutils-devel
BuildRequires:	valgrind-devel
BuildRequires:	libedit-devel
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	gnupg2

Provides:      rocm-device-libs
Provides:      rocm-device-libs(x86-64)
Requires:      rocm-core

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-device-libs
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       Apache 2.0 + LLVM
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - device libs

%description
Radeon Open Compute - device libs

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_RDL_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocm-device-libs
cd %{ROCM_BUILD_DIR}/rocm-device-libs
pushd .


# Level 2 : Build

cd %{ROCM_BUILD_DIR}/rocm-device-libs

    CC=/opt/rocm/llvm/bin/clang \
    cmake -GNinja -S "%{ROCM_GIT_DIR}/ROCm-Device-Libs" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_DIR=/opt/rocm/llvm/lib/cmake/llvm
    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install



#%exclude /src

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
