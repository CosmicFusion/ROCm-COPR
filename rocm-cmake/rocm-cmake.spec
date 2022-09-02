%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-cmake
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
%global ROCM_GIT_URL_1 https://github.com/RadeonOpenCompute/rocm-cmake
%global ROCM_GIT_REL_TAG "release/rocm-rel-5.2"

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

Provides:      rocm-cmake
Provides:      rocm-cmake(x86-64)
Requires:      rocm-core

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       CMake modules for common build tasks needed for the ROCm software stack

%description
CMake modules for common build tasks needed for the ROCm software stack

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
    cmake -GNinja -S "%{ROCM_GIT_DIR}/rocm-cmake" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_BUILD_TYPE=Release

ninja -j$(nproc)

# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
%{ROCM_INSTALL_DIR}/share/doc/rocm-cmake/LICENSE
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMAnalyzers.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMCheckTargetIds.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMChecks.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMClangTidy.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMClients.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMConfig.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMConfigVersion.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMCppCheck.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMCreatePackage.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMDocs.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMDoxygenDoc.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMHeaderWrapper.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMInstallSymlinks.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMInstallTargets.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMPackageConfigHelpers.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMSetupVersion.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMSphinxDoc.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/ROCMUtilities.cmake
%{ROCM_INSTALL_DIR}/share/rocm/cmake/header_template.h.in

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
