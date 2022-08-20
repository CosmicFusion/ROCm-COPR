%undefine _auto_set_build_flags
%define _build_id_links none

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
%global ROCM_RDL_GIT https://github.com/RadeonOpenCompute/ROCm-Device-Libs
%global ROCM_PATCH_1 Use-defined-linux-inc-path.patch

BuildRequires: libstdc++-devel
BuildRequires: clang
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: rocm-llvm
BuildRequires: rocm-cmake
BuildRequires: clang
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: libglvnd-devel
BuildRequires: numactl-devel
BuildRequires: numactl
BuildRequires: python3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: wget
BuildRequires: gcc-plugin-devel
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	ninja-build
BuildRequires:	zlib-devel
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	python3-psutil
BuildRequires:	valgrind-devel
BuildRequires:	libedit-devel
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	gnupg2

Provides:      rocm-device-libs
Provides:      rocm-device-libs(x86-64)
Requires:      rocm-core

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-device-libs
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute - device libs

%description
Radeon Open Compute - device libs

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_RDL_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocm-device-libs
cd %{ROCM_BUILD_DIR}/rocm-device-libs
pushd .

# Level 2 : Apply redhat path patch

cd %{ROCM_PATCH_DIR}
#wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-device-libs/%{ROCM_PATCH_1}
cd %{ROCM_GIT_DIR}/ROCm-Device-Libs
git reset --hard
#git apply %{ROCM_PATCH_DIR}/%{ROCM_PATCH_1}

# Level 3 : Build

cd %{ROCM_BUILD_DIR}/rocm-device-libs

    CC=/opt/rocm/llvm/bin/clang CXXFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' CFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
    cmake -S "%{ROCM_GIT_DIR}/ROCm-Device-Libs" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
    -DLLVM_DIR=/opt/rocm/llvm/lib/cmake/llvm
    make -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" make -j$(nproc) install


%files
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/asanrtl.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/hip.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/ockl.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_abi_version_400.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_abi_version_500.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_correctly_rounded_sqrt_off.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_correctly_rounded_sqrt_on.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_daz_opt_off.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_daz_opt_on.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_finite_only_off.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_finite_only_on.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1010.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1011.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1012.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1013.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1030.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1031.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1032.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1033.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1034.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1035.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_1036.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_600.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_601.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_602.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_700.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_701.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_702.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_703.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_704.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_705.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_801.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_802.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_803.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_805.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_810.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_900.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_902.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_904.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_906.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_908.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_909.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_90a.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_90c.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_isa_version_940.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_unsafe_math_off.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_unsafe_math_on.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_wavefrontsize64_off.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/oclc_wavefrontsize64_on.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/ocml.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/amdgcn/bitcode/opencl.bc
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/cmake/AMDDeviceLibs/AMDDeviceLibsConfig.cmake
   /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/ROCm-Device-Libs/rocm-device-libs/LICENSE.TXT
%exclude /src

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
