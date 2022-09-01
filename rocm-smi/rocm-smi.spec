%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-smi
%global pkgver %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
%global builddir %{_builddir}/%{pkgname}-%{pkgver}
%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 3
%global GIT_MAJOR_VERSION 5
%global GIT_MINOR_VERSION 2
%global GIT_PATCH_VERSION 3
%global ROCM_MAGIC_VERSION 109
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_GLOBAL_DIR /opt/rocm
%global ROCM_LIBPATCH_VERSION 50203
%global ROCM_GIT_DIR %{builddir}/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{builddir}/rocm-build/build
%global ROCM_PATCH_DIR %{builddir}/rocm-build/patch
%global ROCM_GIT_URL_1 https://github.com/RadeonOpenCompute/rocm_smi_lib
%global ROCM_PATCH_1 rocm-smi-string_header.patch

%global toolchain clang

Source0: %{ROCM_GIT_URL_1}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz

BuildRequires:	binutils-devel
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	gnupg2
BuildRequires:	libedit-devel
BuildRequires:	libffi-devel
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
BuildRequires: doxygen
BuildRequires: gcc-plugin-devel
BuildRequires: git
BuildRequires: libdrm
BuildRequires: libdrm-devel
BuildRequires: libglvnd-devel
BuildRequires: ninja-build
BuildRequires: numactl
BuildRequires: numactl-devel
BuildRequires: perl
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: rocm-cmake
BuildRequires: rocm-comgr-devel
BuildRequires: rocm-core
BuildRequires: rocm-device-libs
BuildRequires: rocm-hip-runtime
BuildRequires: rocm-hip-runtime-devel
BuildRequires: rocm-hsakmt-roct-devel
BuildRequires: rocm-llvm
BuildRequires: rocminfo
BuildRequires: texlive-pdftex
BuildRequires: wget


Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - System Management Interface Library

%description
Radeon Open Compute - System Management Interface Library


%package lib
Provides:      rocm-smi-lib
Provides:      rocm-smi-lib(x86-64)
Provides:      rocm-smi
Provides:      rocm-smi(x86-64)
Provides:      rocm-smi-lib64
Provides:      rocm-smi-lib64(x86-64)
Requires:      rocm-hsa-rocr

Obsoletes:	rocm-smi
Obsoletes:	rocm-smi-lib64

Summary:       Radeon Open Compute - System Management Interface Library

%description lib
Radeon Open Compute - System Management Interface Library

%package devel
Provides:      rocm-smi-devel
Provides:      rocm-smi-devel(x86-64)
Provides:      rocm-smi-lib-devel
Provides:      rocm-smi-lib-devel(x86-64)
Provides:      rocm-smi-lib64-devel
Provides:      rocm-smi-lib64-devel(x86-64)
Requires:      rocm-smi-lib

Obsoletes:	rocm-smi-devel
Obsoletes:	rocm-smi-lib64-devel

Summary:       Radeon Open Compute - System Management Interface Library Development Kit

%description devel
Radeon Open Compute - System Management Interface Library Development Kit

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# Level 1 :  Extract

cd  %{ROCM_GIT_DIR}

tar -xf %{SOURCE0} -C ./

# Level 2 : Patch

cd %{ROCM_PATCH_DIR}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-smi/%{ROCM_PATCH_1}

cd %{ROCM_GIT_DIR}/rocm_smi_lib-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_1}"

# Level 3 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}

 
  CC=clang CXX=clang++ \
  cmake -GNinja -S "%{ROCM_GIT_DIR}/rocm_smi_lib-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}" \
  -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
  -DCMAKE_BUILD_TYPE=Release 
    
    

ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install


%files lib
%{ROCM_INSTALL_DIR}/share/*
%{ROCM_INSTALL_DIR}/rocm_smi/lib/*
%{ROCM_INSTALL_DIR}/oam/lib/*
%{ROCM_INSTALL_DIR}/libexec/rocm_smi/*
%{ROCM_INSTALL_DIR}/lib/lib*
%{ROCM_INSTALL_DIR}/bin/rocm-smi

%files devel 
%{ROCM_INSTALL_DIR}/rocm_smi/include/*
%{ROCM_INSTALL_DIR}/oam/include/*
%{ROCM_INSTALL_DIR}/lib/lib/cmake/*
%{ROCM_INSTALL_DIR}/include/*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
