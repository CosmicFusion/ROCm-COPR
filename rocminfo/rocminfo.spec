%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocminfo
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
%global ROCM_GIT_URL_1 https://github.com/RadeonOpenCompute/rocminfo
%global ROCM_GIT_PKG_1 rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.tar.gz

%global toolchain clang

Source0: %{ROCM_GIT_URL_1}/archive/%{pkgname}-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.tar.gz

BuildRequires: clang
BuildRequires: rocm-cmake
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: libstdc++-devel
BuildRequires: numactl-devel
BuildRequires: pciutils-devel
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: hsa-rocr-devel

Provides:      rocminfo
Provides:      rocminfo(x86-64)
Provides:      rocm_agent_enumerator
Provides:      rocm_agent_enumerator(x86-64)
Requires:      pciutils
Requires:      hsa-rocr
Requires:      rocm-device-libs
Requires:      rocm-core
Requires:      python3
Requires:	kmod

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       ROCm info tools - rocm_agent_enumerator

%description
ROCm info tools - rocm_agent_enumerator

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd %{_sourcedir}

ls %{SOURCE0} || echo "Source 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_1}/archive/%{ROCM_GIT_PKG_1} -O %{SOURCE0}

cd  %{ROCM_GIT_DIR}

rm -rf ./*

tar -xf %{SOURCE0} -C ./

# Level 2 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}


    CC=/usr/bin/clang CXX=/usr/bin/clang++ \
    cmake -GNinja -S "%{ROCM_GIT_DIR}/rocminfo-rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_LIBDIR='%{ROCM_INSTALL_DIR}/%{_lib}"
    
 ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/rocm_agent_enumerator
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/rocminfo
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/rocminfo/License.txt
%exclude /src
