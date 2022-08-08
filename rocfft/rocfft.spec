%undefine _auto_set_build_flags
%define _build_id_links none

%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_REL_TAG "release/rocm-rel-5.2"
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCM_ROCFFT_GIT https://github.com/ROCmSoftwarePlatform/rocFFT

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

Provides:      rocfft
Provides:      rocfft(x86-64)
Requires:      rocm-hip-runtime

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocfft
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - FFT implementation 

%description
Radeon Open Compute - FFT implementation 

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_REL_TAG}" "%{ROCM_ROCFFT_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocfft
cd %{ROCM_BUILD_DIR}/rocfft
pushd .


# Level 2 : Build

cd %{ROCM_BUILD_DIR}/rocfft

     CC=/opt/rocm/bin/hipcc CXX=/opt/rocm/bin/hipcc / 
     CXXFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' /
     CFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' /
     cmake -GNinja -S "%{ROCM_GIT_DIR}/rocFFT" \
     -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
     -DAMDGPU_TARGETS="$AMDGPU_TARGETS"

    ninja -j$(nproc)



# Level 4 : Package

#DESTDIR=%{buildroot} make install

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-rocfft.conf

echo "/opt/rocm/rocfft/lib" > %{buildroot}/etc/ld.so.conf.d/10-rocm-rocfft.conf

%files
/etc/ld.so.conf.d/*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
