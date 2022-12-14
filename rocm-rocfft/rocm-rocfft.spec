%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-rocfft
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
%global ROCM_GIT_URL_1  https://github.com/ROCmSoftwarePlatform/rocFFT
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
BuildRequires: doxygen
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: gcc-plugin-devel
BuildRequires: git
BuildRequires: rocm-hsa-devel
BuildRequires: rocm-hsakmt-roct-devel
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
BuildRequires: rocm-hip-devel
BuildRequires: rocm-llvm
#BuildRequires: rocminfo
BuildRequires: wget




BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - FFT implementation

%description
Radeon Open Compute - FFT implementation

%package runtime
Provides:      rocfft
Provides:      rocfft(x86-64)
Requires:      rocm-hip-runtime

Summary:       Radeon Open Compute - FFT implementation

%package devel
Provides:      rocfft-devel
Provides:      rocfft-devel(x86-64)
Requires:      rocm-hip-runtime
Requires:      rocfft

Summary:       Radeon Open Compute - FFT development kit

%description runtime
Radeon Open Compute - FFT implementation


%description devel
Radeon Open Compute - FFT development kit

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# Level 1 :  Sources

cd  %{ROCM_GIT_DIR}

git clone -b %{ROCM_GIT_REL_TAG} %{ROCM_GIT_URL_1}

# Level 2 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}

     
   export  HIP_CXXFLAGS='-D_GNU_SOURCE -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux'
     
   export  HIP_CFLAGS='-D_GNU_SOURCE -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux'
 
   export CXX=%{ROCM_GLOBAL_DIR}/bin/hipcc
   
   export CC=%{ROCM_GLOBAL_DIR}/bin/hipcc
   
   export AMDGPU_TARGETS=gfx803
   
     cmake -GNinja -S "%{ROCM_GIT_DIR}/rocFFT-rocm" \
     -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
     -DAMDGPU_TARGETS="$AMDGPU_TARGETS" \
     -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON

     


ninja -j$(nproc)

# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-rocfft.conf

echo "%{ROCM_GLOBAL_DIR}/rocfft/lib" > %{buildroot}/etc/ld.so.conf.d/10-rocm-rocfft.conf

%files runtime
/etc/ld.so.conf.d/*
%{ROCM_INSTALL_DIR}/share/doc/rocfft/LICENSE*
%{ROCM_INSTALL_DIR}/lib/librocfft*
%{ROCM_INSTALL_DIR}/bin/rocfft_rtc_helper

%files devel
%{ROCM_INSTALL_DIR}/rocfft/lib/cmake/rocfft*
%{ROCM_INSTALL_DIR}/rocfft/lib/librocfft*
%{ROCM_INSTALL_DIR}/lib/cmake/rocfft/rocfft*
%{ROCM_INSTALL_DIR}}/include/rocfft/rocfft*
%{ROCM_INSTALL_DIR}/include/rocfft*
