%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-hsa
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
%global ROCM_GIT_URL_1 https://github.com/RadeonOpenCompute/ROCR-Runtime

%global toolchain clang

Source0: %{ROCM_GIT_URL_1}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz

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
BuildRequires: rocm-hsakmt-roct-devel
BuildRequires:  rocm-device-libs
BuildRequires: libdrm-devel
BuildRequires: libdrm




BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       ROCm Platform Runtime: ROCr a HPC market enhanced HSA based runtime


%description
ROCm Platform Runtime: ROCr a HPC market enhanced HSA based runtime

%package rocr
Summary:       ROCm Platform Runtime: ROCr a HPC market enhanced HSA based runtime
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

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Obsoletes:  	rocr-runtime
Obsoletes:  	rocm-runtime


%package devel
Summary:       ROCm Platform Runtime development kit
Provides:      rocr-runtime-devel
Provides:      rocr-runtime-devel(x86-64)
Provides:      rocm-runtime-devel
Provides:      rocm-runtime-devel(x86-64)
Provides:      rocm-hsa-devel
Provides:      rocm-hsa-devel(x86-64)
Requires:      elfutils-libelf
Requires:      hsa-rocr

Obsoletes:  	rocr-runtime-devel
Obsoletes:  	rocm-runtime-devel

%description rocr
ROCm Platform Runtime: ROCr a HPC market enhanced HSA based runtime


%description devel
ROCm Platform Runtime development kit

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

    CC=/usr/bin/clang CXX=/usr/bin/clang++ \
    cmake -GNinja -S "%{ROCM_GIT_DIR}/ROCR-Runtime-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}/src" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_CXX_FLAGS='-DNDEBUG' 
    
    
ninja -j$(nproc)


# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-hsa-rocr.conf

echo "%{ROCM_GLOBAL_DIR}/hsa/lib" >> %{buildroot}/etc/ld.so.conf.d/10-rocm-hsa-rocr.conf

%files rocr
/etc/ld.so.conf.d/*
%{ROCM_INSTALL_DIR}/hsa/lib/libhsa-runtime*
%{ROCM_INSTALL_DIR}/lib/libhsa-runtime*
%{ROCM_INSTALL_DIR}/share/doc/hsa-runtime64/LICENSE.md

%files devel
%{ROCM_INSTALL_DIR}/hsa/include/hsa
%{ROCM_INSTALL_DIR}/include/hsa/Brig.h
%{ROCM_INSTALL_DIR}/include/hsa/amd_hsa_common.h
%{ROCM_INSTALL_DIR}/include/hsa/amd_hsa_elf.h
%{ROCM_INSTALL_DIR}/include/hsa/amd_hsa_kernel_code.h
%{ROCM_INSTALL_DIR}/include/hsa/amd_hsa_queue.h
%{ROCM_INSTALL_DIR}/include/hsa/amd_hsa_signal.h
%{ROCM_INSTALL_DIR}/include/hsa/hsa.h
%{ROCM_INSTALL_DIR}/include/hsa/hsa_api_trace.h
%{ROCM_INSTALL_DIR}/include/hsa/hsa_ext_amd.h
%{ROCM_INSTALL_DIR}/include/hsa/hsa_ext_finalize.h
%{ROCM_INSTALL_DIR}/include/hsa/hsa_ext_image.h
%{ROCM_INSTALL_DIR}/include/hsa/hsa_ven_amd_aqlprofile.h
%{ROCM_INSTALL_DIR}/include/hsa/hsa_ven_amd_loader.h
%{ROCM_INSTALL_DIR}/lib/cmake/hsa-runtime64/hsa-runtime64*
