%undefine _auto_set_build_flags

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
%global ROCCLR_GIT https://github.com/ROCm-Developer-Tools/ROCclr.git
%global ROCM_OCL_GIT https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime.git
%global ROCM_HIP_GIT https://github.com/ROCm-Developer-Tools/HIP
%global ROCM_HAMD_GIT https://github.com/ROCm-Developer-Tools/hipamd.git
%global ROCM_PATCH_1 hipconfig-flags.patch
%global ROCM_PATCH_2 hipcc-flags.patch
%global ROCM_PATCH_3 hipvars-flags.patch
%global ROCM_PATCH_4 hip-gnu12-inline.patch

%global toolchain clang

BuildRequires: wget
BuildRequires: libstdc++-devel
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
BuildRequires: hsa-rocr-devel
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: hsakmt-roct-devel
BuildRequires: rocm-device-libs
BuildRequires: libdrm-devel
BuildRequires: libdrm
BuildRequires: libglvnd-devel
BuildRequires: doxygen
BuildRequires: perl
BuildRequires: gcc-plugin-devel
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	clang
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
BuildRequires:      comgr
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
BuildRequires:	python3-sphinx
BuildRequires:	python3-recommonmark
BuildRequires:	multilib-rpm-config
BuildRequires:	binutils-devel
BuildRequires:	valgrind-devel
BuildRequires:	libedit-devel
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	llvm-devel


Suggests:    rocm-hip-libraries
Requires:	clang
Requires:	llvm-libs
Requires:	libstdc++-devel
Requires:   rocm-core
Requires:   rocm-hip-runtime

Provides:      hip-devel
Provides:      hip-samples
Provides:      hip-devel(x86-64)
Provides:      hip-samples(x86-64)
Provides:      rocm-hip-sdk
Provides:      rocm-hip-sdk(x86-64)
Provides:      rocm-hip-runtime-devel
Provides:      rocm-hip-runtime-devel(x86-64)


Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-hip-runtime-devel
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute (ROCm) HIP development kit and libraries for AMD platforms

%description
Radeon Open Compute (ROCm) HIP development kit and libraries for AMD platforms

%build

# Make basic structure

mkdir -p %{buildroot}/src

cd %{buildroot}/src


## file N1 from official repos (rocm-hip-sdk) :

mkdir -p %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info

touch %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-hip-sdk

echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-hip-sdk

# Stage 3

# Make basic structure

mkdir -p %{buildroot}/src

cd %{buildroot}/src

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCCLR_GIT}"

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_OCL_GIT}"

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_HIP_GIT}"

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_HAMD_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocm-hip-runtime
cd %{ROCM_BUILD_DIR}/rocm-hip-runtime
pushd .

# Level 2 : Patch

cd %{ROCM_PATCH_DIR}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-hip-runtime/%{ROCM_PATCH_4}

cd %{ROCM_GIT_DIR}/hipamd

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_4}"


# Level 3 : Build

cd %{ROCM_BUILD_DIR}/rocm-hip-runtime

CC=clang CXX=clang++ \
CXXFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' CFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
cmake -GNinja -S %{ROCM_GIT_DIR}/hipamd \
-DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
-DHIP_COMMON_DIR=%{ROCM_GIT_DIR}/HIP \
-DAMD_OPENCL_PATH=%{ROCM_GIT_DIR}/ROCm-OpenCL-Runtime \
-DROCCLR_PATH=%{ROCM_GIT_DIR}/ROCclr \
-DHIP_PLATFORM=amd \
-DOFFLOAD_ARCH_STR="$AMDGPU_TARGETS" \
-B %{ROCM_BUILD_DIR}/rocm-hip-runtime

    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

#Level 5 : Include fix patch

cd %{ROCM_PATCH_DIR}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-hip-runtime-devel/%{ROCM_PATCH_1}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-hip-runtime-devel/%{ROCM_PATCH_2}
wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-hip-runtime-devel/%{ROCM_PATCH_3}

patch "%{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/hipconfig.pl" "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_1}"

patch "%{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/hipcc.pl" "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_2}"

patch "%{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/hipvars.pm" "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_3}"

cd %{buildroot}

rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-hiprt
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/libamd*
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/libhip*
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hip/lib/libamd*
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/hip
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/.hipInfo

mkdir -p %{buildroot}/etc/profile.d
touch %{buildroot}/etc/profile.d/rocm-hip-devel.sh
echo  "export HIP_ENV_CXX_FLAGS='-D_GNU_SOURCE -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux'"  >  %{buildroot}/etc/profile.d/rocm-hip-devel.sh
echo  'export PATH=$PATH:/opt/rocm/hip/bin' >>  %{buildroot}/etc/profile.d/rocm-hip-devel.sh
chmod +x %{buildroot}/etc/profile.d/rocm-hip-devel.sh

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
/etc/profile.d/rocm-hip-devel.sh
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
