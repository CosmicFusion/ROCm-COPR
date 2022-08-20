%undefine _auto_set_build_flags
%define _build_id_links none
%define _unpackaged_files_terminate_build 0

%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 3
%global ROCM_MAGIC_VERSION 109
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50203
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_REL_TAG "release/rocm-rel-5.2"
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCM_RCCL_GIT https://github.com/ROCmSoftwarePlatform/rccl
%global ROCM_PATCH_1 include-stdlib.patch

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
BuildRequires: hsa-rocr-devel 
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: rocm-llvm
BuildRequires: rocm-core
BuildRequires: rocm-hip-runtime-devel
BuildRequires: rocm-hip-runtime
BuildRequires: hsakmt-roct-devel 
BuildRequires: rocm-device-libs
BuildRequires: libdrm-devel
BuildRequires: libdrm
BuildRequires: doxygen
BuildRequires: perl
BuildRequires: gcc-plugin-devel
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	clang
BuildRequires: rocminfo
BuildRequires: comgr
BuildRequires: python3-pyyaml
BuildRequires: python3-virtualenv
BuildRequires: libcxx-devel
BuildRequires: openssl-devel
BuildRequires: msgpack-devel
BuildRequires: gcc-gfortran
BuildRequires: libgomp
BuildRequires: rocm-smi-lib
BuildRequires: gtest
BuildRequires: gtest-devel

Provides:      rccl
Provides:      rccl(x86-64)
Requires:      rocm-hip-runtime
Requires:      rocm-smi-lib

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rccl
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       Apache 2.0
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - Communication Collectives Library

%description
Radeon Open Compute - Communication Collectives Library

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# Level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_REL_TAG}" "%{ROCM_RCCL_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rccl
cd %{ROCM_BUILD_DIR}/rccl
pushd .

# Level 2 : Patch

cd %{ROCM_PATCH_DIR}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rccl/%{ROCM_PATCH_1}

cd %{ROCM_GIT_DIR}/rccl

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_1}"


# Level 3 : Build

cd %{ROCM_BUILD_DIR}/rccl

     
    
  CXX=/opt/rocm/bin/hipcc \
  HIP_ENV_CXX_FLAGS='-Wl,--allow-undefined -D_GNU_SOURCE -stdlib=libstdc++ -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
  cmake -Wno-dev -GNinja -S %{ROCM_GIT_DIR}/rccl \
  -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
  -DBUILD_TESTS=OFF
    
  CXX=/opt/rocm/bin/hipcc \
  HIP_ENV_CXX_FLAGS='-Wl,--allow-undefined -D_GNU_SOURCE -stdlib=libstdc++ -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
  ninja



# Level 4 : Package

#DESTDIR=%{buildroot} make install

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-rccl.conf

echo "/opt/rocm/rccl/lib" > %{buildroot}/etc/ld.so.conf.d/10-rocm-rccl.conf

%files
/etc/ld.so.conf.d/*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/librccl*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/rccl/LICENSE*
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
