%undefine _auto_set_build_flags
%define _build_id_links none

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
%global ROCM_ROCBLAS_GIT https://github.com/ROCmSoftwarePlatform/rocBLAS
%global ROCM_PATCH_1 rocblas-include-path.patch
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
BuildRequires: hsa-rocr
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: rocm-llvm
BuildRequires: rocm-core
BuildRequires: rocm-hip-runtime-devel
BuildRequires:      rocm-hip-runtime
BuildRequires: hsakmt-roct
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

Provides:      rocblas
Provides:      rocblas(x86-64)
Provides:      rocblas-devel
Provides:      rocblas-devel(x86-64)
Requires:      rocm-hip-runtime
Recommends: 	openmp

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocblas
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - BLAS implementation

%description
Radeon Open Compute - BLAS implementation

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# Level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_REL_TAG}" "%{ROCM_ROCBLAS_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocblas
cd %{ROCM_BUILD_DIR}/rocblas
pushd .

# Level 2 : Patch

cd %{ROCM_PATCH_DIR}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocblas/%{ROCM_PATCH_1}

cd %{ROCM_GIT_DIR}/rocBLAS

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_1}"


# Level 3 : Build

cd %{ROCM_BUILD_DIR}/rocblas

     
    
  PATH="/opt/rocm/llvm/bin:${PATH}" \
  CXX=/opt/rocm/bin/hipcc \
  HIP_ENV_CXX_FLAGS='-D_GNU_SOURCE -stdlib=libstdc++ -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
  cmake -Wno-dev  -GNinja -S "%{ROCM_GIT_DIR}/rocBLAS" \
 -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
 -DCMAKE_PREFIX_PATH=/opt/rocm/llvm/lib/cmake/llvm \
 -Damd_comgr_DIR=/opt/rocm/lib/cmake/amd_comgr \
 -DBUILD_WITH_TENSILE=ON \
 -DTensile_LIBRARY_FORMAT=yaml \
 -DTensile_CPU_THREADS="$(nproc)" \
 -DTensile_CODE_OBJECT_VERSION=V3 \
 -DCMAKE_TOOLCHAIN_FILE=%{ROCM_GIT_DIR}/rocBLAS/toolchain-linux.cmake \
 -DBUILD_TESTING=OFF
    
    PATH="/opt/rocm/llvm/bin:${PATH}" \
  CXX=/opt/rocm/bin/hipcc \
  HIP_ENV_CXX_FLAGS='-D_GNU_SOURCE -stdlib=libstdc++ -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
  ninja -j$(nproc)



# Level 4 : Package

#DESTDIR=%{buildroot} make install

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-rocblas.conf

echo "/opt/rocm/rocblas/lib" > %{buildroot}/etc/ld.so.conf.d/10-rocm-rocblas.conf

%files
/etc/ld.so.conf.d/*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
