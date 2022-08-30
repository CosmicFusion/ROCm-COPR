%undefine _auto_set_build_flags
%define _build_id_links none

%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 3
%global ROCM_MAGIC_VERSION 109
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50203
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch

%global toolchain clang
BuildRequires: clang
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: numactl
BuildRequires: python3
BuildRequires: git
BuildRequires: wget
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	ninja-build
BuildRequires:	zlib-devel
BuildRequires:	libffi-devel
BuildRequires:	python3-setuptools
BuildRequires:	gnupg2
BuildRequires: hsa-rocr
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: rocm-llvm
BuildRequires: rocm-core
BuildRequires: rocm-hip-runtime-devel
BuildRequires: hsakmt-roct
BuildRequires: rocm-device-libs
BuildRequires: libdrm
BuildRequires: doxygen
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	clang
BuildRequires: rocminfo
BuildRequires: comgr

Provides:      hipinfo
Provides:      hipinfo(x86-64)
Requires:      rocm-hip-runtime

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          hipinfo
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Simple HIP application that enumerates all available device properties

%description
Simple HIP application that enumerates all available device properties

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

mkdir -p %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin

mkdir -p %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hip/bin

# Level 1 : Build

cd %{ROCM_BUILD_DIR}

cp -r  "%{ROCM_INSTALL_DIR}/share/hip/samples/1_Utils/hipInfo" .

cd %{ROCM_BUILD_DIR}/hipInfo

# Remove root calls

sed -i 's#cp $(EXE) $(HIP_PATH)/bin#ls#' "./Makefile"

  HIP_ENV_CXX_FLAGS=' -D_GNU_SOURCE -stdlib=libstdc++ -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux' \
  make -j$(nproc)



# Level 4 : Package

mv ./hipInfo %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/hipInfo

ln -sf /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/hipInfo %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/hipinfo

ln -sf /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/hipInfo %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hip/bin/hipInfo

ln -sf /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/hipInfo %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hip/bin/hipinfo

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
