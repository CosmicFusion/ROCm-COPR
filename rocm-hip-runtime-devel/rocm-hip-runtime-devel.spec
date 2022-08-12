%undefine _auto_set_build_flags

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
%global ROCM_HIP_GIT https://github.com/ROCm-Developer-Tools/HIP
%global ROCM_HAMD_GIT https://github.com/ROCm-Developer-Tools/hipamd.git
%global ROCM_PATCH_1 hipconfig-flags.patch
%global ROCM_PATCH_2 hipcc-flags.patch
%global ROCM_PATCH_3 hipvars-flags.patch

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
BuildRequires: hsa-rocr
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: hsakmt-roct
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


Recommends:      rocsparse
Recommends:      rocprim
Recommends:      rocm-core
Recommends:      rocm-hip-runtime
Recommends:      hipcub
Recommends:      rocfft
Recommends:      rocrand
Recommends: 	hipblas
Recommends: 	rocprim
Recommends: 	rccl
Recommends: 	hipfort		
Recommends: 	rocalution
Recommends:	rocthrust
Recommends: 	hipsparse
Recommends:	hipfft
Requires:	clang
Requires:	llvm-libs
Requires:	libstdc++-devel

Provides:      hip-devel
Provides:      hip-samples
Provides:      hip-devel(x86-64)
Provides:      hip-samples(x86-64)
Provides:      rocm-hip-sdk
Provides:      rocm-hip-sdk(x86-64)
Provides:      rocm-hip-runtime-devel
Provides:      rocm-hip-runtime-devel(x86-64)
Provides:      rocm-hip-libraries
Provides:      rocm-hip-libraries(x86-64)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-hip-runtime-devel
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute (ROCm) HIP development kit and libraries for AMD platforms

%description
Radeon Open Compute (ROCm) HIP development kit and libraries for AMD platforms

%build

# Make basic structure

mkdir -p %{buildroot}/src

cd %{buildroot}/src


# Level 1 : Get deb

wget -r -nd --no-parent -A 'rocm-hip-sdk*.deb' http://repo.radeon.com/rocm/apt/%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/pool/main/r/rocm-hip-sdk/

mv ./rocm-hip-sdk* ./rocm-hip-sdk.deb

# Level 2 : Extract deb

ar -x "rocm-hip-sdk.deb"

mv ./data* ./data-archive.tar.gz

tar -xf data-archive.tar.gz

# Level 3 : Package

mv ./opt %{buildroot}

# Clean

rm -r %{buildroot}/src/

# Stage 2

# Make basic structure

mkdir -p %{buildroot}/src

cd %{buildroot}/src

# Level 1 : Get deb

wget -r -nd --no-parent -A 'rocm-hip-libraries*.deb' http://repo.radeon.com/rocm/apt/%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/pool/main/r/rocm-hip-libraries/

mv ./rocm-hip-libraries* ./rocm-hip-libraries.deb

# Level 2 : Extract deb

ar -x "rocm-hip-libraries.deb"

mv ./data* ./data-archive.tar.gz

tar -xf data-archive.tar.gz

# Level 3 : Package

cp -r ./opt/rocm* %{buildroot}/opt/

rm -r ./opt/rocm*
# Clean

rm -r %{buildroot}/src/

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


# Level 2 : Build

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

printf "# Auto-generated by cmake\nHIP_PACKAGING_VERSION_PATCH=21152.50201\nCPACK_DEBIAN_PACKAGE_RELEASE=79\nCPACK_RPM_PACKAGE_RELEASE=79\nHIP_VERSION_MAJOR=5\nHIP_VERSION_MINOR=2\nHIP_VERSION_PATCH=21152\nHIP_VERSION_GITHASH=4b155a06" >> %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/bin/.hipVersion

rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-hiprt
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/libamd*
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/libhip*
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/hip/lib/libamd*
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/share/doc/hip
rm -rf %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/lib/.hipInfo

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
