%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCM_ROCT_GIT https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface

BuildRequires: clang
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: numactl-devel
BuildRequires: numactl
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: libdrm
BuildRequires: libdrm-devel
BuildRequires: pciutils
BuildRequires: pciutils-devel

Provides:      hsakmt-roct
Provides:      hsakmt-roct(x86-64)
Provides:      roct-thunk-interface
Provides:      roct-thunk-interface(x86-64)
Provides:      hsakmt-devel
Provides:      hsakmt-devel(x86-64)
Requires:      libdrm
Requires:      numactl
Requires:      pciutils
Requires:      rocm-core

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          hsakmt-roct
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute Thunk Interface

%description
Radeon Open Compute Thunk Development Interface

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_ROCT_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/hsakmt-roct
cd %{ROCM_BUILD_DIR}/hsakmt-roct
pushd .


# Level 2 : Build

cd %{ROCM_BUILD_DIR}/hsakmt-roct

    cmake -GNinja -S "%{ROCM_GIT_DIR}/ROCT-Thunk-Interface" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_BUILD_TYPE=Release
    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsakmt.h
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsakmttypes.h
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib64/cmake/hsakmt/hsakmt-config-version.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib64/cmake/hsakmt/hsakmt-config.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib64/cmake/hsakmt/hsakmtTargets-release.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib64/cmake/hsakmt/hsakmtTargets.cmake
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib64/libhsakmt.a
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/hsakmt/LICENSE.md
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/pkgconfig/libhsakmt.pc
%exclude /src

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
