%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch





BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: libglvnd-devel
BuildRequires: numactl-devel
BuildRequires: numactl
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel

Provides:      rocm-opencl
Provides:      rocm-opencl(x86-64)
Provides:      rocm-ocl-icd
Provides:      rocm-ocl-icd
Requires:      comgr
Requires:      hsa-rocr

BuildArch:     x86_64
Name:          rocm-opencl-runtime
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       MIT and ASL 2.0
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - OpenCL runtime

%description
 Radeon Open Compute - OpenCL runtime


Source0: https://github.com/ROCm-Developer-Tools/ROCclr.git

Source1: https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime.git

Source2: rocclr-gfx803.patch

%build

#cp %{SOURCE2} .

ls

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

 ls
