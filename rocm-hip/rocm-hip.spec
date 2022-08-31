%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-hip
%global pkgver %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
%global builddir %{_builddir}/%{pkgname}-%{pkgver}
%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 3
%global GIT_MAJOR_VERSION 5
%global GIT_MINOR_VERSION 2
%global GIT_PATCH_VERSION 1
%global ROCM_MAGIC_VERSION 109
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_GLOBAL_DIR /opt/rocm
%global ROCM_LIBPATCH_VERSION 50203
%global ROCM_GIT_DIR %{builddir}/rocm-build/git
%global ROCM_GIT_TAG rocm-5.2.x
%global ROCM_BUILD_DIR %{builddir}/rocm-build/build
%global ROCM_PATCH_DIR %{builddir}/rocm-build/patch
%global ROCM_GIT_URL_1 https://github.com/ROCm-Developer-Tools/ROCclr
%global ROCM_GIT_URL_2 https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime
%global ROCM_GIT_URL_3 https://github.com/ROCm-Developer-Tools/HIP
%global ROCM_GIT_URL_4 https://github.com/ROCm-Developer-Tools/hipamd
%global ROCM_PATCH_1 hip-gnu12-inline.patch
%global ROCM_PATCH_2 hipcc-vars.patch

%global toolchain clang

%global SRC0 rocclr-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz
%global SRC1 rocm-opencl-runtime-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz
%global SRC2 hip-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz
%global SRC3 hipamd-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz


BuildRequires:	binutils-devel
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	gnupg2
BuildRequires:	libedit-devel
BuildRequires:	libffi-devel
BuildRequires:	llvm-devel
BuildRequires:	multilib-rpm-config
BuildRequires:	ncurses-devel
BuildRequires:	ninja-build
BuildRequires:	python3-devel
BuildRequires:	python3-psutil
BuildRequires:	python3-recommonmark
BuildRequires:	python3-setuptools
BuildRequires:	python3-sphinx
BuildRequires:	valgrind-devel
BuildRequires:	zlib-devel
BuildRequires: rocm-comgr-devel
BuildRequires: clang
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: gcc-plugin-devel
BuildRequires: git
BuildRequires: rocm-hsa-devel
BuildRequires: rocm-hsakmt-roct-devel
BuildRequires: libdrm
BuildRequires: libdrm-devel
BuildRequires: libglvnd-devel
BuildRequires: libstdc++-devel
BuildRequires: ncurses-devel
BuildRequires: ninja-build
BuildRequires: numactl
BuildRequires: numactl-devel
BuildRequires: pciutils-devel
BuildRequires: perl
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: rocm-cmake
BuildRequires: rocm-device-libs
BuildRequires: rocm-llvm
BuildRequires: wget

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          %{pkgname}
Version:       %{pkgver}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute (ROCm) runtime for running HIP applications on the AMD platform

%description
Radeon Open Compute (ROCm) runtime for running HIP applications on the AMD platform

%package runtime
Requires:      elfutils-libelf
Requires:      rocm-comgr-devel
Requires:      rocm-core
Requires:      rocm-llvm
Requires:      rocminfo
Requires:      rocm-language-runtime

Provides:      hip-runtime-amd
Provides:      hip-runtime-nvidia
Provides:      hip-runtime-amd(x86-64)
Provides:      hip-runtime-nvidia(x86-64)
Provides:      rocm-hip-runtime
Provides:      rocm-hip-runtime(x86-64)
Summary:       Radeon Open Compute (ROCm) runtime for running HIP applications on the AMD platform

%description runtime
Radeon Open Compute (ROCm) runtime for running HIP applications on the AMD platform

%package devel
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

Summary:       Radeon Open Compute (ROCm) HIP development kit and libraries for AMD platforms

%description devel
Radeon Open Compute (ROCm) HIP development kit and libraries for AMD platforms

%build

# Level 1 : Create versioning from official packaging

## file N1 from official repos (rocm-hip-runtime) :

mkdir -p %{buildroot}%{ROCM_INSTALL_DIR}/.info

touch %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-hiprt

echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-hiprt

#

## file N2 from official repos (rocm-hip-sdk) :

mkdir -p %{buildroot}%{ROCM_INSTALL_DIR}/.info

touch %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-hip-sdk

echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}%{ROCM_INSTALL_DIR}/.info/version-hip-sdk


# Stage 2

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : Get sources

# URL 1 

cd %{_sourcedir}

ls %{SRC0} || echo "SRC 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_1}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz -O %{SRC0}

cd  %{ROCM_GIT_DIR}

rm -rf ./*

tar -xf %{_sourcedir}/%{SRC0} -C ./

# URL 2 

cd %{_sourcedir}

ls %{SRC1} || echo "SRC 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_2}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz -O %{SRC1}

cd  %{ROCM_GIT_DIR}

tar -xf %{_sourcedir}/%{SRC1} -C ./

# URL 3

cd %{_sourcedir}

ls %{SRC2} || echo "SRC 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_3}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz -O %{SRC2}

cd  %{ROCM_GIT_DIR}

tar -xf %{_sourcedir}/%{SRC2} -C ./

# URL 4 

cd %{_sourcedir}

ls %{SRC3} || echo "SRC 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_4}/archive/rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}.tar.gz -O %{SRC3}

cd  %{ROCM_GIT_DIR}

tar -xf %{_sourcedir}/%{SRC3} -C ./

# Level 2 : Patch

cd %{ROCM_PATCH_DIR}

wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-hip/%{ROCM_PATCH_1}

cd %{ROCM_GIT_DIR}/hipamd-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION}

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_1}"

# Level 3 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}

CC=clang CXX=clang++ \
CXXFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' CFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
cmake -GNinja -S %{ROCM_GIT_DIR}/hipamd-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION} \
-DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
-DHIP_COMMON_DIR=%{ROCM_GIT_DIR}/HIP-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION} \
-DAMD_OPENCL_PATH=%{ROCM_GIT_DIR}/ROCm-OpenCL-Runtime-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION} \
-DROCCLR_PATH=%{ROCM_GIT_DIR}/ROCclr-rocm-%{GIT_MAJOR_VERSION}.%{GIT_MINOR_VERSION}.%{GIT_PATCH_VERSION} \
-DHIP_PLATFORM=amd
#-DOFFLOAD_ARCH_STR="$AMDGPU_TARGETS" \

    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/profile.d

touch %{buildroot}/etc/profile.d/rocm-hip-devel.sh

echo  "export HIP_CXXFLAGS='-D_GNU_SOURCE -isystem /usr/include/c++/12 -isystem /usr/include/c++/12/x86_64-redhat-linux'"  >  %{buildroot}/etc/profile.d/rocm-hip-devel.sh

echo  'export PATH=$PATH:/opt/rocm/hip/bin' >>  %{buildroot}/etc/profile.d/rocm-hip-devel.sh

chmod +x %{buildroot}/etc/profile.d/rocm-hip-devel.sh

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-hip.conf

echo "%{ROCM_GLOBAL_DIR}/hip/lib" >> %{buildroot}/etc/ld.so.conf.d/10-rocm-hip.conf

#Level 5 : Include fix patch

cd %{ROCM_PATCH_DIR}

wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-hip/%{ROCM_PATCH_2}

cd %{buildroot}%{ROCM_INSTALL_DIR}

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_2}"

mv %{buildroot}%{ROCM_INSTALL_DIR}/lib %{buildroot}%{ROCM_INSTALL_DIR}/lib || echo "no such file or directory , moving on !"

%files runtime
/etc/ld.so.conf.d/10-rocm-hip.conf
%{ROCM_INSTALL_DIR}/.info/version-hiprt
%{ROCM_INSTALL_DIR}/hip/lib/libamd*
%{ROCM_INSTALL_DIR}/lib/libamd*
%{ROCM_INSTALL_DIR}/lib/libhip*
%{ROCM_INSTALL_DIR}/share/doc/hip
%{ROCM_INSTALL_DIR}/lib/.hipInfo

%files devel
%{ROCM_INSTALL_DIR}/bin/.hipVersion
%{ROCM_INSTALL_DIR}/bin/hipcc
%{ROCM_INSTALL_DIR}/bin/hipcc.pl
%{ROCM_INSTALL_DIR}/bin/hipcc_cmake_linker_helper
%{ROCM_INSTALL_DIR}/bin/hipconfig
%{ROCM_INSTALL_DIR}/bin/hipconfig.pl
%{ROCM_INSTALL_DIR}/bin/hipdemangleatp
%{ROCM_INSTALL_DIR}/bin/hip_embed_pch.sh
%{ROCM_INSTALL_DIR}/bin/hipvars.pm
%{ROCM_INSTALL_DIR}/bin/roc-obj
%{ROCM_INSTALL_DIR}/bin/roc-obj-extract
%{ROCM_INSTALL_DIR}/bin/roc-obj-ls
%{ROCM_INSTALL_DIR}/hip/bin/.hipVersion
%{ROCM_INSTALL_DIR}/hip/bin/hipcc
%{ROCM_INSTALL_DIR}/hip/bin/hipcc.pl
%{ROCM_INSTALL_DIR}/hip/bin/hipcc_cmake_linker_helper
%{ROCM_INSTALL_DIR}/hip/bin/hipconfig
%{ROCM_INSTALL_DIR}/hip/bin/hipconfig.pl
%{ROCM_INSTALL_DIR}/hip/bin/hipdemangleatp
%{ROCM_INSTALL_DIR}/hip/bin/hip_embed_pch.sh
%{ROCM_INSTALL_DIR}/hip/bin/hipvars.pm
%{ROCM_INSTALL_DIR}/hip/bin/roc-obj
%{ROCM_INSTALL_DIR}/hip/bin/roc-obj-extract
%{ROCM_INSTALL_DIR}/hip/bin/roc-obj-ls
%{ROCM_INSTALL_DIR}/lib/cmake/hip/FindHIP/run_make2cmake.cmake
%{ROCM_INSTALL_DIR}/lib/cmake/hip/FindHIP/run_hipcc.cmake
%{ROCM_INSTALL_DIR}/lib/cmake/hip/FindHIP.cmake
%{ROCM_INSTALL_DIR}/hip/cmake/FindHIP/run_make2cmake.cmake
%{ROCM_INSTALL_DIR}/hip/cmake/FindHIP/run_hipcc.cmake
%{ROCM_INSTALL_DIR}/hip/cmake/FindHIP.cmake
%{ROCM_INSTALL_DIR}/share/hip
%{ROCM_INSTALL_DIR}/hip/lib/cmake
%{ROCM_INSTALL_DIR}/include/*
%{ROCM_INSTALL_DIR}/lib/cmake
%{ROCM_INSTALL_DIR}/hip/cmake
%{ROCM_INSTALL_DIR}/hip/bin
%{ROCM_INSTALL_DIR}/hip/lib/.hipInfo
%{ROCM_INSTALL_DIR}/hip/include/*
%{ROCM_INSTALL_DIR}/.info/version-hip-sdk
/etc/profile.d/rocm-hip-devel.sh

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
