%undefine _auto_set_build_flags
%define _build_id_links none

%global pkgname rocm-hip
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
%global ROCM_GIT_URL_1 https://github.com/ROCm-Developer-Tools/ROCclr
%global ROCM_GIT_URL_2 https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime
%global ROCM_GIT_URL_3 https://github.com/ROCm-Developer-Tools/HIP
%global ROCM_GIT_URL_4 https://github.com/ROCm-Developer-Tools/hipamd
%global ROCM_GIT_PKG_1 rocm-5.2.1.tar.gz
%global ROCM_PATCH_1 hip-gnu12-inline.patch
%global ROCM_PATCH_2 hipcc-vars.patch

%global toolchain clang

Source0: %{ROCM_GIT_URL_1}/archive/%{pkgname}-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.tar.gz

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
BuildRequires:      comgr
BuildRequires: clang
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: elfutils-libelf
BuildRequires: elfutils-libelf-devel
BuildRequires: gcc-plugin-devel
BuildRequires: git
BuildRequires: hsa-rocr-devel
BuildRequires: hsakmt-roct-devel
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
Requires:      comgr
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

# level 1 : Get Sources

# URL 1 

cd %{_sourcedir}

ls %{SOURCE0} || echo "Source 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_1}/archive/%{ROCM_GIT_PKG_1} -O %{SOURCE0}

cd  %{ROCM_GIT_DIR}

rm -rf ./*

tar -xf %{SOURCE0} -C ./

rm %{SOURCE0}

# URL 2 

cd %{_sourcedir}

ls %{SOURCE0} || echo "Source 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_2}/archive/%{ROCM_GIT_PKG_1} -O %{SOURCE0}

cd  %{ROCM_GIT_DIR}

rm -rf ./*

tar -xf %{SOURCE0} -C ./

rm %{SOURCE0}

# URL 3

cd %{_sourcedir}

ls %{SOURCE0} || echo "Source 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_3}/archive/%{ROCM_GIT_PKG_1} -O %{SOURCE0}

cd  %{ROCM_GIT_DIR}

rm -rf ./*

tar -xf %{SOURCE0} -C ./

rm %{SOURCE0}

# URL 4 

cd %{_sourcedir}

ls %{SOURCE0} || echo "Source 0 missing. Downloading NOW !" && wget %{ROCM_GIT_URL_4}/archive/%{ROCM_GIT_PKG_1} -O %{SOURCE0}

cd  %{ROCM_GIT_DIR}

rm -rf ./*

tar -xf %{SOURCE0} -C ./

rm %{SOURCE0}

# Level 2 : Patch

cd %{ROCM_PATCH_DIR}

wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-hip/%{ROCM_PATCH_1}

cd %{ROCM_GIT_DIR}/hipamd-rocm-5.2.1

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_1}"

# Level 3 : Build

mkdir -p %{ROCM_BUILD_DIR}/%{pkgname}

cd %{ROCM_BUILD_DIR}/%{pkgname}

CC=clang CXX=clang++ \
CXXFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' CFLAGS='-I/usr/include -I/usr/include/c++/12 -I/usr/include/c++/12/x86_64-redhat-linux' \
cmake -GNinja -S %{ROCM_GIT_DIR}/hipamd -B %{ROCM_BUILD_DIR}/rocm-hip-runtime-rocm-5.2.1 \
-DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}" \
-DHIP_COMMON_DIR=%{ROCM_GIT_DIR}/HIP-rocm-5.2.1 \
-DAMD_OPENCL_PATH=%{ROCM_GIT_DIR}/ROCm-OpenCL-Runtime-rocm-5.2.1 \
-DROCCLR_PATH=%{ROCM_GIT_DIR}/ROCclr-rocm-5.2.1 \
-DHIP_PLATFORM=amd \
-DCMAKE_INSTALL_LIBDIR="%{ROCM_INSTALL_DIR}/%{_lib}" \
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

echo "%{ROCM_GLOBAL_DIR}/lib" >> %{buildroot}/etc/ld.so.conf.d/10-rocm-hip.conf

#Level 5 : Include fix patch

cd %{ROCM_PATCH_DIR}

wget https://raw.githubusercontent.com/CosmicFusion/ROCm-COPR/main/rocm-hip/%{ROCM_PATCH_2}

cd %{buildroot}%{ROCM_INSTALL_DIR}

patch -Np1 -i "%{ROCM_PATCH_DIR}/%{ROCM_PATCH_2}"

%files runtime
/etc/ld.so.conf.d/10-rocm-hip.conf
%{ROCM_INSTALL_DIR}/.info/version-hiprt
%{ROCM_INSTALL_DIR}/hip
%{ROCM_INSTALL_DIR}/%{_lib}/libamd*
%{ROCM_INSTALL_DIR}/%{_lib}/libhip*
%{ROCM_INSTALL_DIR}/hip/%{_lib}/libamd*
%{ROCM_INSTALL_DIR}/share/doc/hip
%{ROCM_INSTALL_DIR}/%{_lib}/.hipInfo

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
%{ROCM_INSTALL_DIR}/%{_lib}/cmake/hip/FindHIP/run_make2cmake.cmake
%{ROCM_INSTALL_DIR}/%{_lib}/cmake/hip/FindHIP/run_hipcc.cmake
%{ROCM_INSTALL_DIR}/%{_lib}/cmake/hip/FindHIP.cmake
%{ROCM_INSTALL_DIR}/hip/cmake/FindHIP/run_make2cmake.cmake
%{ROCM_INSTALL_DIR}/hip/cmake/FindHIP/run_hipcc.cmake
%{ROCM_INSTALL_DIR}/hip/cmake/FindHIP.cmake
%{ROCM_INSTALL_DIR}/include/hip/channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/device_functions.h
%{ROCM_INSTALL_DIR}/include/hip/driver_types.h
%{ROCM_INSTALL_DIR}/include/hip/hip_bfloat16.h
%{ROCM_INSTALL_DIR}/include/hip/hip_common.h
%{ROCM_INSTALL_DIR}/include/hip/hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/hip_ext.h
%{ROCM_INSTALL_DIR}/include/hip/hip_fp16.h
%{ROCM_INSTALL_DIR}/include/hip/hip_hcc.h
%{ROCM_INSTALL_DIR}/include/hip/hip_profile.h
%{ROCM_INSTALL_DIR}/include/hip/hiprtc.h
%{ROCM_INSTALL_DIR}/include/hip/hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/hip_runtime_api.h
%{ROCM_INSTALL_DIR}/include/hip/hip_texture_types.h
%{ROCM_INSTALL_DIR}/include/hip/hip_vector_types.h
%{ROCM_INSTALL_DIR}/include/hip/hip_version.h
%{ROCM_INSTALL_DIR}/include/hip/library_types.h
%{ROCM_INSTALL_DIR}/include/hip/math_functions.h
%{ROCM_INSTALL_DIR}/include/hip/surface_types.h
%{ROCM_INSTALL_DIR}/include/hip/texture_types.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_device_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_atomic.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_common.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_fp16.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_runtime_pt_api.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_vector_types.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_math_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_surface_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_warp_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/concepts.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/device_library_decls.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/functional_grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/grid_launch.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/grid_launch_GGL.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/helpers.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_cooperative_groups_helper.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_fp16_gcc.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_fp16_math_fwd.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_ldg.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_prof_str.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_runtime_prof.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/host_defines.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hsa_helpers.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/llvm_intrinsics.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/macro_based_grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/math_fwd.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/ockl_image.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/program_state.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/texture_fetch_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/texture_indirect_functions.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hiprtc.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_runtime_api.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_texture_types.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_device_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_atomic.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_common.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_fp16.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_runtime_pt_api.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_vector_types.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_math_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_surface_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_warp_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/concepts.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/device_library_decls.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/functional_grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/grid_launch.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/grid_launch_GGL.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/helpers.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_cooperative_groups_helper.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_fp16_gcc.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_fp16_math_fwd.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_ldg.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_prof_str.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_runtime_prof.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/host_defines.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hsa_helpers.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/llvm_intrinsics.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/macro_based_grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/math_fwd.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/ockl_image.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/program_state.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/texture_fetch_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/texture_indirect_functions.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hiprtc.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_runtime_api.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_texture_types.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/include/hip/channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/device_functions.h
%{ROCM_INSTALL_DIR}/include/hip/driver_types.h
%{ROCM_INSTALL_DIR}/include/hip/hip_bfloat16.h
%{ROCM_INSTALL_DIR}/include/hip/hip_common.h
%{ROCM_INSTALL_DIR}/include/hip/hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/hip_ext.h
%{ROCM_INSTALL_DIR}/include/hip/hip_fp16.h
%{ROCM_INSTALL_DIR}/include/hip/hip_hcc.h
%{ROCM_INSTALL_DIR}/include/hip/hip_profile.h
%{ROCM_INSTALL_DIR}/include/hip/hiprtc.h
%{ROCM_INSTALL_DIR}/include/hip/hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/hip_runtime_api.h
%{ROCM_INSTALL_DIR}/include/hip/hip_texture_types.h
%{ROCM_INSTALL_DIR}/include/hip/hip_vector_types.h
%{ROCM_INSTALL_DIR}/include/hip/hip_version.h
%{ROCM_INSTALL_DIR}/include/hip/library_types.h
%{ROCM_INSTALL_DIR}/include/hip/math_functions.h
%{ROCM_INSTALL_DIR}/include/hip/surface_types.h
%{ROCM_INSTALL_DIR}/include/hip/texture_types.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_device_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_atomic.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_common.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_fp16.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_runtime_pt_api.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_hip_vector_types.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_math_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_surface_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/amd_warp_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/concepts.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/device_library_decls.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/functional_grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/grid_launch.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/grid_launch_GGL.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/helpers.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_cooperative_groups_helper.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_fp16_gcc.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_fp16_math_fwd.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_ldg.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_prof_str.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hip_runtime_prof.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/host_defines.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/hsa_helpers.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/llvm_intrinsics.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/macro_based_grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/math_fwd.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/ockl_image.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/program_state.hpp
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/texture_fetch_functions.h
%{ROCM_INSTALL_DIR}/include/hip/amd_detail/texture_indirect_functions.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hiprtc.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_runtime_api.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_texture_types.h
%{ROCM_INSTALL_DIR}/include/hip/nvidia_detail/nvidia_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_device_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_atomic.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_common.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_fp16.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_runtime_pt_api.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_hip_vector_types.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_math_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_surface_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/amd_warp_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/concepts.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/device_library_decls.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/functional_grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/grid_launch.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/grid_launch_GGL.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/helpers.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_cooperative_groups_helper.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_fp16_gcc.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_fp16_math_fwd.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_ldg.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_prof_str.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hip_runtime_prof.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/host_defines.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/hsa_helpers.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/llvm_intrinsics.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/macro_based_grid_launch.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/math_fwd.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/ockl_image.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/program_state.hpp
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/texture_fetch_functions.h
%{ROCM_INSTALL_DIR}/include/hip/hcc_detail/texture_indirect_functions.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_channel_descriptor.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_complex.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hiprtc.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_runtime.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_runtime_api.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_texture_types.h
%{ROCM_INSTALL_DIR}/include/hip/nvcc_detail/nvidia_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_channel_descriptor.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_device_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_atomic.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_common.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_complex.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_fp16.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_runtime.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_runtime_pt_api.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_vector_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_math_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_surface_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_warp_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/concepts.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/device_library_decls.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/functional_grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/grid_launch.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/grid_launch_GGL.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/helpers.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_cooperative_groups_helper.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_fp16_gcc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_fp16_math_fwd.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_ldg.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_prof_str.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_runtime_prof.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/host_defines.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hsa_helpers.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/llvm_intrinsics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/macro_based_grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/math_fwd.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/ockl_image.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/program_state.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/texture_fetch_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/texture_indirect_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_channel_descriptor.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_complex.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hiprtc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_runtime.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_runtime_api.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_texture_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_channel_descriptor.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_device_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_atomic.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_common.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_complex.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_fp16.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_runtime.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_runtime_pt_api.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_vector_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_math_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_surface_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_warp_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/concepts.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/device_library_decls.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/functional_grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/grid_launch.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/grid_launch_GGL.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/helpers.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_cooperative_groups_helper.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_fp16_gcc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_fp16_math_fwd.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_ldg.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_prof_str.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_runtime_prof.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/host_defines.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hsa_helpers.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/llvm_intrinsics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/macro_based_grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/math_fwd.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/ockl_image.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/program_state.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/texture_fetch_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/texture_indirect_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_channel_descriptor.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_complex.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hiprtc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_runtime.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_runtime_api.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_texture_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/channel_descriptor.h
%{ROCM_INSTALL_DIR}/hip/include/hip/device_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/driver_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_bfloat16.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_common.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_complex.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_ext.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_fp16.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_hcc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_profile.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hiprtc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_runtime.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_runtime_api.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_texture_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_vector_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hip_version.h
%{ROCM_INSTALL_DIR}/hip/include/hip/library_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/math_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/surface_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/texture_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_channel_descriptor.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_device_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_atomic.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_common.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_complex.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_fp16.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_runtime.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_runtime_pt_api.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_hip_vector_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_math_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_surface_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/amd_warp_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/concepts.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/device_library_decls.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/functional_grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/grid_launch.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/grid_launch_GGL.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/helpers.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_cooperative_groups_helper.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_fp16_gcc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_fp16_math_fwd.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_ldg.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_prof_str.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hip_runtime_prof.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/host_defines.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/hsa_helpers.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/llvm_intrinsics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/macro_based_grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/math_fwd.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/ockl_image.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/program_state.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/texture_fetch_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/amd_detail/texture_indirect_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_channel_descriptor.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_complex.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hiprtc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_runtime.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_runtime_api.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_texture_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvidia_detail/nvidia_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_channel_descriptor.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_device_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_atomic.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_common.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_complex.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_fp16.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_runtime.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_runtime_pt_api.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_hip_vector_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_math_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_surface_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/amd_warp_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/concepts.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/device_library_decls.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/functional_grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/grid_launch.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/grid_launch_GGL.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/helpers.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_cooperative_groups_helper.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_fp16_gcc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_fp16_math_fwd.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_ldg.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_prof_str.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hip_runtime_prof.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/host_defines.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/hsa_helpers.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/llvm_intrinsics.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/macro_based_grid_launch.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/math_fwd.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/ockl_image.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/program_state.hpp
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/texture_fetch_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/hcc_detail/texture_indirect_functions.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_channel_descriptor.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_complex.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_cooperative_groups.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hiprtc.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_runtime.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_runtime_api.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_texture_types.h
%{ROCM_INSTALL_DIR}/hip/include/hip/nvcc_detail/nvidia_hip_unsafe_atomics.h
%{ROCM_INSTALL_DIR}/share/hip
%{ROCM_INSTALL_DIR}/hip/%{_lib}/cmake
%{ROCM_INSTALL_DIR}/include
%{ROCM_INSTALL_DIR}/%{_lib}/cmake
%{ROCM_INSTALL_DIR}/hip/cmake
%{ROCM_INSTALL_DIR}/hip/bin
%{ROCM_INSTALL_DIR}/hip/include
%{ROCM_INSTALL_DIR}/.info/version-hip-sdk
/etc/profile.d/rocm-hip-devel.sh

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
