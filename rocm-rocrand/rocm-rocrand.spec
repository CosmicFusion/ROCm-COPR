%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-rocrand
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
%global ROCM_GIT_URL_1 https://github.com/ROCmSoftwarePlatform/rocRAND
%global ROCM_GIT_URL_2 https://github.com/ROCmSoftwarePlatform/hipRAND
%global ROCM_GIT_REL_TAG "release/rocm-rel-5.2"

%global toolchain clang

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
BuildRequires: comgr
BuildRequires: doxygen
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: gcc-gfortran
BuildRequires: gcc-plugin-devel
BuildRequires: git
BuildRequires: libcxx-devel
BuildRequires: libdrm
BuildRequires: libdrm-devel
BuildRequires: libglvnd-devel
BuildRequires: libgomp
BuildRequires: msgpack-devel
BuildRequires: ninja-build
BuildRequires: numactl
BuildRequires: numactl-devel
BuildRequires: openssl-devel
BuildRequires: perl
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pyyaml
BuildRequires: python3-virtualenv
BuildRequires: rocm-cmake
BuildRequires: rocm-core
BuildRequires: rocm-device-libs
BuildRequires: rocm-hip-runtime
BuildRequires: rocm-hip-runtime-devel
BuildRequires: rocm-hsa-devel
BuildRequires: rocm-hsakmt-roct-devel
BuildRequires: rocm-llvm
BuildRequires: rocminfo
BuildRequires: wget

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - Pseudo-random and quasi-random number generator

%description
Radeon Open Compute - Pseudo-random and quasi-random number generator

%package runtime 
Provides:      rocrand
Provides:      rocrand(x86-64)
Provides:      hiprand
Provides:      hiprand(x86-64)
Requires:      rocm-hip-runtime

Recommends: gcc-gfortran

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Summary:       Radeon Open Compute - Pseudo-random and quasi-random number generator

%description runtime
Radeon Open Compute - Pseudo-random and quasi-random number generator


%package devel
Provides:      rocrand-devel(x86-64)
Provides:      hiprand-devel
Provides:      hiprand-devel(x86-64)
Requires:      rocm-hip-runtime
Requires:      rocrand

Recommends: gcc-gfortran


Summary:       Radeon Open Compute - Pseudo-random and quasi-random number generator development kit

%description devel
Radeon Open Compute - Pseudo-random and quasi-random number generator development kit

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : Get sources

# URL 1 

# Level 1 :  Sources

cd  %{ROCM_GIT_DIR}

git clone -b %{ROCM_GIT_REL_TAG} %{ROCM_GIT_URL_1}

# 

cd  %{ROCM_GIT_DIR}

git clone -b %{ROCM_GIT_TAG} %{ROCM_GIT_URL_2}


# Level 2 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}

export  HIP_CXXFLAGS='-D_GNU_SOURCE -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux'
  
export  CXX=%{ROCM_GLOBAL_DIR}/bin/hipcc
  
  cmake -Wno-dev  -GNinja -S "%{ROCM_GIT_DIR}/rocRAND" \
  -DCMAKE_INSTALL_PREFIX=%{ROCM_INSTALL_DIR} \
  -DBUILD_TEST=OFF



ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocrand.conf

echo '/opt/rocm/hiprand/lib' > %{buildroot}/etc/ld.so.conf.d/10-rocrand.conf

echo '/opt/rocm/rocrand/lib' >> %{buildroot}/etc/ld.so.conf.d/10-rocrand.conf

ln -s "%{ROCM_INSTALL_DIR}/hiprand/include/" "%{buildroot}%{ROCM_INSTALL_DIR}/include/hiprand"

ln -s "%{ROCM_INSTALL_DIR}/rocrand/include/" "%{buildroot}%{ROCM_INSTALL_DIR}/include/rocrand"

%files runtime
/etc/ld.so.conf.d/*
%{ROCM_INSTALL_DIR}/lib/librocrand*
%{ROCM_INSTALL_DIR}/lib/libhiprand*
%{ROCM_INSTALL_DIR}/share/doc/rocrand/LICENSE*

%files devel
%{ROCM_INSTALL_DIR}/lib/cmake/hiprand/hiprand*
%{ROCM_INSTALL_DIR}/lib/cmake/rocrand/rocrand*
%{ROCM_INSTALL_DIR}/hiprand/lib/libhiprand*
%{ROCM_INSTALL_DIR}/rocrand/lib/librocrand*
%{ROCM_INSTALL_DIR}/hiprand/lib/cmake/hiprand*
%{ROCM_INSTALL_DIR}/rocrand/lib/cmake/rocrand*
%{ROCM_INSTALL_DIR}/hiprand/include/hiprand*
%{ROCM_INSTALL_DIR}/rocrand/include/rocrand*
%{ROCM_INSTALL_DIR}/include/hiprand*
%{ROCM_INSTALL_DIR}/include/rocrand*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
