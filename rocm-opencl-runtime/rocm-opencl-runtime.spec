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
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCCLR_GIT https://github.com/ROCm-Developer-Tools/ROCclr.git
%global ROCM_OCL_GIT https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime.git
#%global ROCM_PATCH_1 rocclr-gfx803.patch

%global toolchain clang


BuildRequires: wget
BuildRequires: libstdc++-devel
BuildRequires: rocm-llvm
BuildRequires: rocm-cmake
BuildRequires: ninja-build
BuildRequires: clang
BuildRequires: cmake
BuildRequires: numactl-devel
BuildRequires: numactl
BuildRequires: ncurses-devel
BuildRequires: pciutils-devel
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: hsa-rocr-devel
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: hsakmt-roct-devel
BuildRequires: rocm-device-libs
BuildRequires: libdrm-devel
BuildRequires: libdrm
BuildRequires: libglvnd-devel
BuildRequires: doxygen
BuildRequires: perl
BuildRequires: gcc-plugin-devel
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	clang
BuildRequires: libstdc++-devel
BuildRequires: clang
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: rocm-llvm
BuildRequires: rocm-cmake
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
BuildRequires:	valgrind-devel
BuildRequires:	libedit-devel
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	gnupg2
BuildRequires:      comgr
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
BuildRequires:	llvm-devel

Requires:      comgr
Requires:      rocm-core
Requires:      rocminfo
Requires:      hsa-rocr

Provides:      rocm-ocl-icd
Provides:      rocm-opencl
Provides:      rocm-ocl-icd(x86-64)
Provides:      rocm-opencl(x86-64)
Provides:      rocm-opencl-runtime
Provides:      rocm-opencl-runtime(x86-64)

Obsoletes:  	rocm-opencl

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-opencl-runtime
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - OpenCL runtime

%description
 Radeon Open Compute - OpenCL runtime

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# Level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCCLR_GIT}"

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_OCL_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocm-opencl-runtime
cd %{ROCM_BUILD_DIR}/rocm-opencl-runtime
pushd .

# Level 2 : Build

cd %{ROCM_BUILD_DIR}/rocm-opencl-runtime

CC=clang CXX=clang++ \
cmake -Wno-dev -GNinja -S %{ROCM_GIT_DIR}/ROCm-OpenCL-Runtime \
-DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
-DCMAKE_BUILD_TYPE=Release
    
DESTDIR="%{buildroot}" ninja -j$(nproc) install

# Level 4 : Package

DESTDIR=%{buildroot} ninja install

mkdir -p %{buildroot}/etc/OpenCL/vendors
touch %{buildroot}/etc/OpenCL/vendors/amdocl64.icd
echo libamdocl64.so > %{buildroot}/etc/OpenCL/vendors/amdocl64.icd
mkdir -p %{buildroot}/etc/ld.so.conf.d
touch %{buildroot}/etc/ld.so.conf.d/10-rocm-opencl.conf
echo /opt/rocm/opencl/lib > %{buildroot}/etc/ld.so.conf.d/10-rocm-opencl.conf
mkdir -p %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info
touch %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-oclrt
echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-oclrt


%files
# rocm-opencl
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/opencl/LICENSE*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/opencl/lib/lib*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/opencl/bin/clinfo
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/lib*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/clinfo
# rocm-ocl-icd
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/rocm-ocl-icd/LICENSE*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/opencl/lib/libOpen*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/libOpen*
# rocm-opencl-runtime
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-oclrt
# system
/etc/ld.so.conf.d/10-rocm-opencl.conf
/etc/OpenCL/vendors/amdocl64.icd
%exclude /src

%post
/sbin/ldconfig

%postun
