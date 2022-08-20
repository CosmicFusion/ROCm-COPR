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
%global ROCM_SMI_LIB_GIT https://github.com/RadeonOpenCompute/rocm_smi_lib
%global ROCM_PATCH_1 rocm-smi-string_header.patch

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
BuildRequires:	binutils-devel
BuildRequires:	valgrind-devel
BuildRequires:	libedit-devel
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	gnupg2
BuildRequires: hsa-rocr-devel 
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
BuildRequires: texlive-pdftex

Provides:      rocm-smi-lib
Provides:      rocm-smi-lib(x86-64)
Provides:      rocm-smi
Provides:      rocm-smi(x86-64)
Provides:      rocm-smi-lib64
Provides:      rocm-smi-lib64(x86-64)
Requires:      hsa-rocr

Obsoletes:	rocm-smi
Obsoletes:	rocm-smi-lib64

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-smi-lib
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - System Management Interface Library

%description
Radeon Open Compute - System Management Interface Library

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_SMI_LIB_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocm-smi-lib
cd %{ROCM_BUILD_DIR}/rocm-smi-lib
pushd .

# Level 2 : Patch

cd %{ROCM_PATCH_DIR}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-smi-lib/%{ROCM_PATCH_1}

cd %{ROCM_GIT_DIR}/rocm_smi_lib

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_1}"



# Level 3 : Build

cd %{ROCM_BUILD_DIR}/rocm-smi-lib

     
    
 
  CC=clang CXX=clang++ \
  cmake -GNinja -S "%{ROCM_GIT_DIR}/rocm_smi_lib" \
  -DCMAKE_INSTALL_PREFIX=/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION} \
  -DCMAKE_BUILD_TYPE=Release 
    
    
   ninja -j$(nproc)



# Level 4 : Package

#DESTDIR=%{buildroot} make install

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
