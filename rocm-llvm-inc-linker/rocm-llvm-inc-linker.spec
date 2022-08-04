%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}

Requires:      libstdc++-devel
Requires:      rocm-llvm

BuildArch:     noarch
Name:          rocm-llvm-inc-linker
Version:       1.0
Release:       0.%{fedora}
License:       MIT
Group:         System Environment/Libraries
Summary:       links required files from system path to rocm-llvm path

%description
links required files from system path to rocm-llvm path

%build
mkdir -p %{buildroot}/%{ROCM_INSTALL_DIR}/llvm/include/clang/Basic
touch %{buildroot}/%{ROCM_INSTALL_DIR}/llvm/include/clang/Basic/.cxx-links
echo "link successful ." > %{buildroot}/%{ROCM_INSTALL_DIR}/llvm/include/clang/Basic/.cxx-links

mkdir -p %{buildroot}/%{ROCM_INSTALL_DIR}/llvm/include/llvm/Support
touch %{buildroot}/%{ROCM_INSTALL_DIR}/llvm/include/llvm/Support/.cxx-links
echo "link successful ." > %{buildroot}/%{ROCM_INSTALL_DIR}/llvm/include/llvm/Support/.cxx-links


%files
%{ROCM_INSTALL_DIR}/llvm/include/clang/Basic/.cxx-links
%{ROCM_INSTALL_DIR}/llvm/include/llvm/Support/.cxx-links

%post
echo "Linking"
ln -s /usr/include/c++/*/cstddef  %{ROCM_INSTALL_DIR}/llvm/include/clang/Basic/cstddef
ln -s /usr/include/c++/*/cstddef %{ROCM_INSTALL_DIR}/llvm/include/llvm/Support/cstddef

%postun
echo "Un-linking"
rm %{ROCM_INSTALL_DIR}/llvm/include/clang/Basic/cstddef
rm %{ROCM_INSTALL_DIR}/llvm/include/llvm/Support/cstddef
