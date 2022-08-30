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
%global ROCM_ROCRAND_GIT https://github.com/ROCmSoftwarePlatform/rocRAND
%global ROCM_HIPRAND_GIT https://github.com/ROCmSoftwarePlatform/hipRAND

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
BuildRequires: python3-pyyaml
BuildRequires: python3-virtualenv
BuildRequires: libcxx-devel
BuildRequires: openssl-devel
BuildRequires: msgpack-devel
BuildRequires: gcc-gfortran
BuildRequires: libgomp


Provides:      rocrand-devel(x86-64)
Provides:      hiprand-devel
Provides:      hiprand-devel(x86-64)
Requires:      rocm-hip-runtime
Requires:      rocrand

Recommends: gcc-gfortran

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocrand-devel
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - Pseudo-random and quasi-random number generator development kit

%description
Radeon Open Compute - Pseudo-random and quasi-random number generator development kit

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_REL_TAG}" "%{ROCM_ROCRAND_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocrand
cd %{ROCM_BUILD_DIR}/rocrand
pushd .

cd "%{ROCM_GIT_DIR}/rocRAND"

git clone "%{ROCM_HIPRAND_GIT}"

# Level 2 : Build

cd %{ROCM_BUILD_DIR}/rocrand

  HIP_ENV_CXX_FLAGS=' -D_GNU_SOURCE -stdlib=libstdc++ -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
  CXX=/opt/rocm/bin/hipcc \
  cmake -Wno-dev  -GNinja -S "%{ROCM_GIT_DIR}/rocRAND" \
  -DCMAKE_INSTALL_PREFIX=/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION} \
  -DBUILD_TEST=OFF \


    ninja -j$(nproc)



# Level 4 : Package

#DESTDIR=%{buildroot} make install

DESTDIR="%{buildroot}" ninja -j$(nproc) install

ln -s "/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hiprand/include/" "%{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hiprand"

ln -s "/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/rocrand/include/" "%{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocrand"

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/cmake/hiprand/hiprand*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/cmake/rocrand/rocrand*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hiprand/lib/libhiprand*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/rocrand/lib/librocrand*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hiprand/lib/cmake/hiprand*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/rocrand/lib/cmake/rocrand*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hiprand/include/hiprand*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/rocrand/include/rocrand*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hiprand*
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocrand*
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
