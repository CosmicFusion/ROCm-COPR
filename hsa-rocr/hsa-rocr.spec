%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCM_ROCR_GIT https://github.com/RadeonOpenCompute/ROCR-Runtime

BuildRequires: rocm-llvm
BuildRequires: rocm-cmake
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: numactl-devel
BuildRequires: numactl
BuildRequires: pciutils-devel
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: vim-common
BuildRequires:      elfutils-libelf
BuildRequires:      elfutils-libelf-devel

Provides:      hsa-rocr
Provides:      hsa-rocr(x86-64)
Provides:      rocr-runtime
Provides:      rocr-runtime(x86-64)
Requires:      elfutils-libelf
Requires:      hsakmt-roct
Requires:      rocm-device-libs
Requires:      rocm-core
Requires:      hsa-amd-aqlprofile

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          hsa-rocr
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
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

    cmake -GNinja -S "%{ROCM_GIT_DIR}/ROCR-Runtime/src" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DCMAKE_BUILD_TYPE=Release
    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files
 /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hsa/include/hsa
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hsa/lib/libhsa-runtime64.so
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hsa/lib/libhsa-runtime64.so.1
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/Brig.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/amd_hsa_common.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/amd_hsa_elf.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/amd_hsa_kernel_code.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/amd_hsa_queue.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/amd_hsa_signal.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/hsa.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/hsa_api_trace.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/hsa_ext_amd.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/hsa_ext_finalize.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/hsa_ext_image.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/hsa_ven_amd_aqlprofile.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/hsa/hsa_ven_amd_loader.h
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/cmake/hsa-runtime64/hsa-runtime64-config-version.cmake
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/cmake/hsa-runtime64/hsa-runtime64-config.cmake
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/cmake/hsa-runtime64/hsa-runtime64Targets-release.cmake
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/cmake/hsa-runtime64/hsa-runtime64Targets.cmake
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/libhsa-runtime64.so
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/libhsa-runtime64.so.1
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/libhsa-runtime64.so.1.5.0
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/hsa-runtime64/LICENSE.md
%exclude /src
