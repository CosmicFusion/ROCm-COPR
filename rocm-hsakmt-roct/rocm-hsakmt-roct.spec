%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-hsakmt-roct
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
%global ROCM_GIT_URL_1 https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface
%global ROCM_GIT_REL_TAG "release/rocm-rel-5.2"

%global toolchain clang

BuildRequires: clang
BuildRequires: cmake
BuildRequires: git
BuildRequires: libdrm
BuildRequires: libdrm-devel
BuildRequires: ninja-build
BuildRequires: numactl
BuildRequires: numactl-devel
BuildRequires: pciutils
BuildRequires: pciutils-devel
BuildRequires: python3
BuildRequires: python3-devel


BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute Thunk Interface

%description
Radeon Open Compute Thunk Interface

%package devel
Provides:      hsakmt-roct
Provides:      hsakmt-roct(x86-64)
Provides:      roct-thunk-interface
Provides:      roct-thunk-interface(x86-64)
Provides:      hsakmt-devel
Provides:      hsakmt-devel(x86-64)
Provides:      hsakmt
Provides:      hsakmt(x86-64)
Provides:      hsakmt-roct-devel
Provides:      hsakmt-roct-devel(x86-64)
Requires:      libdrm
Requires:      numactl
Requires:      pciutils
Requires:      rocm-core

Obsoletes: hsakmt
Obsoletes: hsakmt-devel

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Summary:       Radeon Open Compute Thunk Interface


%description devel
Radeon Open Compute Thunk Interface

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# Level 1 :  Sources

cd  %{ROCM_GIT_DIR}

git clone -b %{ROCM_GIT_TAG} %{ROCM_GIT_URL_1}

# Level 2 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}
    
    CC=/usr/bin/clang CXX=/usr/bin/clang++ \
    cmake -GNinja -S "%{ROCM_GIT_DIR}/ROCT-Thunk-Interface" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_BUILD_TYPE=Release

ninja -j$(nproc)



# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files devel
%{ROCM_INSTALL_DIR}/include/hsakmt.h
%{ROCM_INSTALL_DIR}/include/hsakmttypes.h
%{ROCM_INSTALL_DIR}/lib64/cmake/hsakmt/hsakmt-config-version.cmake
%{ROCM_INSTALL_DIR}/lib64/cmake/hsakmt/hsakmt-config.cmake
%{ROCM_INSTALL_DIR}/lib64/cmake/hsakmt/hsakmtTargets-release.cmake
%{ROCM_INSTALL_DIR}/lib64/cmake/hsakmt/hsakmtTargets.cmake
%{ROCM_INSTALL_DIR}/lib64/libhsakmt.a
%{ROCM_INSTALL_DIR}/share/doc/hsakmt/LICENSE.md
%{ROCM_INSTALL_DIR}/share/pkgconfig/libhsakmt.pc

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
