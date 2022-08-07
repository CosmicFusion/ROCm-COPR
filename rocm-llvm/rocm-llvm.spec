%undefine _auto_set_build_flags
%define _build_id_links none

%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCM_LLVM_GIT https://github.com/RadeonOpenCompute/llvm-project

%global toolchain clang

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

Provides:      rocm-llvm
Provides:      rocm-llvm(x86-64)
Provides:      llvm-amdgpu
Provides:      llvm-amdgpu(x86-64)
Requires:      rocm-core

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-llvm
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       Apache 2.0 + LLVM
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - LLVM toolchain (llvm, clang, lld)

%description
Radeon Open Compute - LLVM toolchain (llvm, clang, lld)

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_LLVM_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocm-llvm
cd %{ROCM_BUILD_DIR}/rocm-llvm
pushd .


# Level 2 : Build

cd %{ROCM_BUILD_DIR}/rocm-llvm

    cmake -GNinja -S "%{ROCM_GIT_DIR}/llvm-project/llvm" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}/llvm" \
    -DLLVM_HOST_TRIPLE=x86_64 \
    -DLLVM_BUILD_UTILS=ON \
    -DLLVM_ENABLE_BINDINGS=OFF \
    -DOCAMLFIND=NO \
    -DLLVM_ENABLE_OCAMLDOC=OFF \
    -DLLVM_INCLUDE_BENCHMARKS=OFF \
    -DLLVM_BUILD_TESTS=OFF \
    -DLLVM_ENABLE_PROJECTS='llvm;clang;compiler-rt;lld' \
    -DLLVM_TARGETS_TO_BUILD='AMDGPU;X86' \
    -DLLVM_BINUTILS_INCDIR=/usr/include
    ninja -j$(nproc)



# Level 4 : Package

#DESTDIR=%{buildroot} make install

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-llvm.conf

echo /opt/rocm/llvm/lib > %{buildroot}/etc/ld.so.conf.d/10-rocm-llvm.conf

%files
/etc/ld.so.conf.d/*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/llvm/*
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
