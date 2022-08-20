%define _build_id_links none

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
%global ROCM_CMAKE_GIT https://github.com/RadeonOpenCompute/rocm-cmake

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
Name:          rocm-cmake
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
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

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_CMAKE_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocm-cmake
cd %{ROCM_BUILD_DIR}/rocm-cmake
pushd .


# Level 2 : Build

cd %{ROCM_BUILD_DIR}/rocm-cmake

    CC=/usr/bin/clang CXX=/usr/bin/clang++ \
    cmake -GNinja -S "%{ROCM_GIT_DIR}/rocm-cmake" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_BUILD_TYPE=Release
    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/rocm-cmake/LICENSE
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMAnalyzers.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMCheckTargetIds.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMChecks.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMClangTidy.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMClients.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMConfig.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMConfigVersion.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMCppCheck.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMCreatePackage.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMDocs.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMDoxygenDoc.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMHeaderWrapper.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMInstallSymlinks.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMInstallTargets.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMPackageConfigHelpers.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMSetupVersion.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMSphinxDoc.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/ROCMUtilities.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/rocm/cmake/header_template.h.in
%exclude /src

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
