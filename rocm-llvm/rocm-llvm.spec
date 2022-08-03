%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50201
%global ROCM_GIT_DIR %{buildroot}/src/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{buildroot}/src/rocm-build/build
%global ROCM_PATCH_DIR %{buildroot}/src/rocm-build/patch
%global ROCM_LLVM_GIT https://github.com/RadeonOpenCompute/llvm-project




BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: libglvnd-devel
BuildRequires: numactl-devel
BuildRequires: numactl
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: wget

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-llvm
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       MIT and ASL 2.0
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - OpenCL runtime

%description
 Radeon Open Compute - OpenCL runtime

%build

# Make basic structure

mkdir -p %{buildroot}/src

cd %{buildroot}/src


# Level 1 : Get deb

wget -r -nd --no-parent -A 'rocm-core*.deb' http://repo.radeon.com/rocm/apt/%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/pool/main/r/rocm-core/

mv ./rocm-core* ./rocm-core.deb

# Level 2 : Extract deb

ar -x "rocm-core.deb"

mv ./data* ./data-archive.tar.gz

tar -xf data-archive.tar.gz

# Level 3 : Package

mv ./opt %{buildroot}

mkdir -p %{buildroot}/etc/ld.so.conf.d
touch %{buildroot}/etc/ld.so.conf.d/10-rocm-core.conf
echo /opt/rocm/lib > %{buildroot}/etc/ld.so.conf.d/10-rocm-core.conf
echo /opt/rocm/lib64 >> %{buildroot}/etc/ld.so.conf.d/10-rocm-core.conf

%files
/etc/ld.so.conf.d/10-rocm-core.conf
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm-core/rocm_version.h
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/include/rocm_version.h
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/CMakeFiles/rocm-core.dir
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/librocm-core.so
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/librocm-core.so.1
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/librocm-core.so.1.0.50201
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/rocmmod
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version
%exclude /src


%post
/sbin/ldconfig
ln -s /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION} /opt/rocm

%postun
/sbin/ldconfig
rm -r /opt/rocm
