%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCM_ROCMINFO_GIT https://github.com/RadeonOpenCompute/rocminfo

BuildRequires: clang
BuildRequires: rocm-cmake
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: numactl-devel
BuildRequires: pciutils-devel
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel

Provides:      rocminfo
Provides:      rocminfo(x86-64)
Provides:      rocm_agent_enumerator
Provides:      rocm_agent_enumerator(x86-64)
Requires:      pciutils
Requires:      hsa-rocr
Requires:      python3

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocminfo
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
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

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_ROCMINFO_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocminfo
cd %{ROCM_BUILD_DIR}/rocminfo
pushd .


# Level 2 : Build

cd %{ROCM_BUILD_DIR}/rocminfo

    cmake -GNinja -S "%{ROCM_GIT_DIR}/rocminfo" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_BUILD_TYPE=Release
    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

#%files
