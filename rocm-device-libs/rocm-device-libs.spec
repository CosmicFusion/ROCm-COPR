%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-device-libs
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
%global ROCM_GIT_URL_1 https://github.com/RadeonOpenCompute/ROCm-Device-Libs

%global toolchain clang

Source0: %{ROCM_GIT_URL_1}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz

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

Provides:      rocm-device-libs
Provides:      rocm-device-libs(x86-64)
Requires:      rocm-core

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - device libs

%description
Radeon Open Compute - device libs

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# Level 1 :  Extract

cd  %{ROCM_GIT_DIR}

tar -xf %{SOURCE0} -C ./

# Level 2 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}

    CC=/opt/rocm/llvm/bin/clang CXX=/opt/rocm/llvm/bin/clang++ CXXFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' CFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
    cmake -GNinja -S  "%{ROCM_GIT_DIR}/ROCm-Device-Libs-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DLLVM_DIR=%{ROCM_GLOBAL_DIR}/llvm/lib/cmake/llvm
    
ninja -j$(nproc)

# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/asanrtl.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/hip.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/ockl.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_abi_version_400.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_abi_version_500.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_correctly_rounded_sqrt_off.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_correctly_rounded_sqrt_on.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_daz_opt_off.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_daz_opt_on.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_finite_only_off.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_finite_only_on.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1010.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1011.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1012.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1013.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1030.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1031.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1032.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1033.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1034.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1035.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_1036.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_600.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_601.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_602.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_700.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_701.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_702.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_703.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_704.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_705.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_801.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_802.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_803.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_805.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_810.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_900.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_902.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_904.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_906.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_908.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_909.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_90a.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_90c.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_isa_version_940.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_unsafe_math_off.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_unsafe_math_on.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_wavefrontsize64_off.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/oclc_wavefrontsize64_on.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/ocml.bc
%{ROCM_INSTALL_DIR}/amdgcn/bitcode/opencl.bc
%{ROCM_INSTALL_DIR}/lib/cmake/AMDDeviceLibs/AMDDeviceLibsConfig.cmake
%{ROCM_INSTALL_DIR}/share/doc/ROCm-Device-Libs/rocm-device-libs/LICENSE.TXT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
