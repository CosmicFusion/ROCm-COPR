%define _build_id_links none


%global pkgname rocm-language-runtime
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
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute (ROCm) Language stack

%description
Radeon Open Compute (ROCm) Language stack

%build

# Level 1 : Create versioning from official packaging

## file N1 from official repos (rocm-language-runtime) :

mkdir -p %{buildroot}%{ROCM_INSTALL_DIR}/.info

touch %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-lrt

echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-lrt

#

%files
%{ROCM_INSTALL_DIR}/.info/version-lrt

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
