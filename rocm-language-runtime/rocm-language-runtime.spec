%define _build_id_links none

%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCCLR_GIT https://github.com/ROCm-Developer-Tools/ROCclr.git
%global ROCM_OCL_GIT https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime.git
%global ROCM_PATCH_1 rocclr-gfx803.patch


BuildRequires: wget

Requires:      rocm-device-libs
Requires:      rocm-core
Requires:      hsakmt-roct
Requires:      comgr
Requires:      hsa-rocr

Provides:      rocm-language-runtime
Provides:      rocm-language-runtime(x86-64)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-language-runtime
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute (ROCm) Language stack

%description
Radeon Open Compute (ROCm) Language stack

%build

# Make basic structure

mkdir -p %{buildroot}/src

cd %{buildroot}/src


# Level 1 : Get deb

wget -r -nd --no-parent -A 'rocm-language-runtime*.deb' http://repo.radeon.com/rocm/apt/%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/pool/main/r/rocm-language-runtime/

mv ./rocm-language-runtime* ./rocm-language-runtime.deb

# Level 2 : Extract deb

ar -x "rocm-language-runtime.deb"

mv ./data* ./data-archive.tar.gz

tar -xf data-archive.tar.gz

# Level 3 : Package

mv ./opt %{buildroot}

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-lrt
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
