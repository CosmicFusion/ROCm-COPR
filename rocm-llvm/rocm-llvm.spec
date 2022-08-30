%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-llvm
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
%global ROCM_GIT_URL_1 https://github.com/RadeonOpenCompute/llvm-project
%global ROCM_GIT_PKG_1 rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.tar.gz
%global ROCM_PATCH_1 llvm-gnu12-inline.patch

%global toolchain clang

Source0: %{ROCM_GIT_URL_1}/archive/%{pkgname}-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.tar.gz



BuildRequires:	binutils-devel
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	gnupg2
BuildRequires:	libedit-devel
BuildRequires:	libffi-devel
BuildRequires:	multilib-rpm-config
BuildRequires:	ncurses-devel
BuildRequires:	ninja-build
BuildRequires:	python3-devel
BuildRequires:	python3-psutil
BuildRequires:	python3-recommonmark
BuildRequires:	python3-setuptools
BuildRequires:	python3-sphinx
BuildRequires:	valgrind-devel
BuildRequires:	zlib-devel
BuildRequires: clang
BuildRequires: cmake
BuildRequires: gcc-plugin-devel
BuildRequires: git
BuildRequires: libglvnd-devel
BuildRequires: ninja-build
BuildRequires: numactl
BuildRequires: numactl-devel
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: wget

Provides:      rocm-llvm
Provides:      rocm-llvm(x86-64)
Provides:      llvm-amdgpu
Provides:      llvm-amdgpu(x86-64)
Requires:      rocm-core

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
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

# level 1 : Get Sources

cd %{_sourcedir}

ls %{SOURCE0} || echo "Source 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_1}/archive/%{ROCM_GIT_PKG_1} -O %{SOURCE0}

cd  %{ROCM_GIT_DIR}

rm -rf ./*

tar -xf %{SOURCE0} -C ./

# Level 2 : Patch

cd %{ROCM_PATCH_DIR}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-llvm/%{ROCM_PATCH_1}

cd %{ROCM_GIT_DIR}/llvm-project-rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_1}"

# Level 3 : Build

cd %{ROCM_BUILD_DIR}/rocm-llvm

cmake -GNinja -S "%{ROCM_GIT_DIR}/llvm-project-rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/llvm" \
-DCMAKE_BUILD_TYPE=Release \
-DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}/llvm" \
-DCMAKE_INSTALL_LIBDIR="%{ROCM_INSTALL_DIR}/llvm/%{_lib}" \
-DLLVM_HOST_TRIPLE=x86_64 \
-DLLVM_BUILD_UTILS=ON \
-DLLVM_ENABLE_BINDINGS=OFF \
-DOCAMLFIND=NO \
-DLLVM_ENABLE_OCAMLDOC=OFF \
-DLLVM_INCLUDE_BENCHMARKS=OFF \
-DLLVM_BUILD_TESTS=OFF \
-DLLVM_ENABLE_PROJECTS='llvm;clang;compiler-rt;lld' \
-DLLVM_TARGETS_TO_BUILD='AMDGPU;X86'
    
    
ninja -j$(nproc)



# Level 4 : Package


DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-llvm.conf

echo %{ROCM_GLOBAL_DIR}/llvm/%{_lib}> %{buildroot}/etc/ld.so.conf.d/10-rocm-llvm.conf

%files
/etc/ld.so.conf.d/*
%{ROCM_INSTALL_DIR}/llvm/*


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
