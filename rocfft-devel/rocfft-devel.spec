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
BuildRequires: hsa-rocr-devel 
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: rocm-llvm
BuildRequires: rocm-core
BuildRequires: rocm-hip-runtime-devel
BuildRequires:      rocm-hip-runtime
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


Provides:      rocfft-devel
Provides:      rocfft-devel(x86-64)
Requires:      rocm-hip-runtime
Requires:      rocfft

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocfft-devel
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - FFT development kit

%description
Radeon Open Compute - FFT development kit

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

     
     CXXFLAGS='-D_GNU_SOURCE  -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
     CFLAGS='-D_GNU_SOURCE  -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
     HIP_ENV_CXX_FLAGS='-D_GNU_SOURCE -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
     HIP_ENV_CC_FLAGS='-DD_GNU_SOURCE -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
     cmake -GNinja -S "%{ROCM_GIT_DIR}/rocFFT" \
     -DCMAKE_CXX_COMPILER=/opt/rocm/bin/hipcc \
     -DCMAKE_C_COMPILER=/opt/rocm/bin/hipcc \
     -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
     -DAMDGPU_TARGETS="$AMDGPU_TARGETS" \
     -DCMAKE_BUILD_WITH_INSTALL_RPATH=1

     


     CXXFLAGS='-D_GNU_SOURCE  -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
     CFLAGS='-D_GNU_SOURCE  -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
     HIP_ENV_CXX_FLAGS='-D_GNU_SOURCE -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
     HIP_ENV_CC_FLAGS='-DD_GNU_SOURCE -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
     ninja -j$(nproc)



# Level 4 : Package

#DESTDIR=%{buildroot} make install

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/rocfft/lib/cmake/rocfft*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/rocfft/lib/librocfft*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/cmake/rocfft/rocfft*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocfft/rocfft*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocfft*
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig

