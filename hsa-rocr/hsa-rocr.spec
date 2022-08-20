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
%global ROCM_ROCR_GIT https://github.com/RadeonOpenCompute/ROCR-Runtime

%global toolchain clang

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
BuildRequires: vim-common
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: hsakmt-roct-devel
BuildRequires:  rocm-device-libs
BuildRequires: libdrm-devel
BuildRequires: libdrm

Provides:      hsa-rocr
Provides:      hsa-rocr(x86-64)
Provides:      rocr-runtime
Provides:      rocr-runtime(x86-64)
Provides:      rocm-runtime
Provides:      rocm-runtime(x86-64)
Requires:      elfutils-libelf
Requires:      hsakmt-roct
Requires:      rocm-device-libs
Requires:      rocm-core
Requires:      libdrm

Obsoletes:  	rocr-runtime
Obsoletes:  	rocm-runtime

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          hsa-rocr
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}.2
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       ROCm Platform Runtime: ROCr a HPC market enhanced HSA based runtime

%description
ROCm Platform Runtime: ROCr a HPC market enhanced HSA based runtime

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_ROCR_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/hsa-rocr
cd %{ROCM_BUILD_DIR}/hsa-rocr
pushd .


# Level 2 : Build

cd %{ROCM_BUILD_DIR}/hsa-rocr

    CC=/usr/bin/clang CXX=/usr/bin/clang++ \
    cmake -GNinja -S "%{ROCM_GIT_DIR}/ROCR-Runtime/src" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_CXX_FLAGS='-DNDEBUG' 
    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-hsa-rocr.conf

echo "/opt/rocm/hsa/lib" >> %{buildroot}/etc/ld.so.conf.d/10-rocm-hsa-rocr.conf


%files
   /etc/ld.so.conf.d/*
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hsa/lib/libhsa-runtime*
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/libhsa-runtime*
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/hsa-runtime64/LICENSE.md
%exclude /src
