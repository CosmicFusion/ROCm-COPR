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

# TEMP DEV ENTRY #
BuildRequires: tree
##################

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

Provides:      rocm-llvm
Provides:      rocm-llvm(x86-64)
Provides:      llvm-amdgpu
Provides:      llvm-amdgpu(x86-64)
Requires:      rocm-core

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-llvm
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr.%{fedora}
License:       Apache 2.0 + LLVM
Group:         System Environment/Libraries
Summary:       ROCm Compiler Support

%description
ROCm Compiler Support

%build

# Make basic structure

mkdir -p %{ROCM_GIT_DIR}

mkdir -p %{ROCM_BUILD_DIR}

mkdir -p %{ROCM_PATCH_DIR}

# level 1 : GIT Clone

cd  %{ROCM_GIT_DIR}

git clone -b "%{ROCM_GIT_TAG}" "%{ROCM_LLVM_GIT}"

mkdir -p %{ROCM_BUILD_DIR}/rocm-llvm
cd %{ROCM_BUILD_DIR}/rocm-llvm
pushd .


# Level 2 : Build

cd %{ROCM_BUILD_DIR}/rocm-llvm

    cmake -S "%{ROCM_GIT_DIR}/llvm-project/llvm"  \
    -DCMAKE_PREFIX_PATH="%{ROCM_INSTALL_DIR}/llvm" \
    -DCMAKE_INSTALL_PREFIX="%{ROCM_INSTALL_DIR}/llvm" \
    -DLLVM_INCLUDE_BENCHMARKS=OFF \
    -DLLVM_ENABLE_PROJECTS='llvm;clang;compiler-rt;lld' \
    -DLLVM_TARGETS_TO_BUILD='AMDGPU;X86' \
    -DLLVM_ENABLE_ASSERTIONS=1 \
    -DLLVM_BINUTILS_INCDIR=/usr/include

    make -j$(nproc)

# Level 4 : Package

DESTDIR=%{buildroot} make install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-rocm-opencl.conf

echo /opt/rocm/llvm/lib > %{buildroot}/etc/ld.so.conf.d/10-rocm-llvm.conf

# TEMP DEV ENTRY #
tree %{buildroot}
##################


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
