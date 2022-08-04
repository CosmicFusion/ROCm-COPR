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
mkdir -p %{buildroot}/opt/rocm/llvm/include/clang/Basic
touch %{buildroot}/opt/rocm/llvm/include/clang/Basic/.cxx-links
echo "link successful ." > %{buildroot}/opt/rocm/llvm/include/clang/Basic/.cxx-links

mkdir -p %{buildroot}/opt/rocm/llvm/include/llvm/Support
touch %{buildroot}/opt/rocm/llvm/include/llvm/Support/.cxx-links
echo "link successful ." > %{buildroot}/opt/rocm/llvm/include/llvm/Support/.cxx-links


%files
/opt/rocm/llvm/include/clang/Basic/.cxx-links
/opt/rocm/llvm/include/llvm/Support/.cxx-links

%post
echo "Linking"
ln -s /usr/include/c++/*/cstddef  /opt/rocm/llvm/include/clang/Basic/cstddef
ln -s /usr/include/c++/*/cstddef /opt/rocm/llvm/include/llvm/Support/cstddef

%postun
echo "Un-linking"
rm /opt/rocm/llvm/include/clang/Basic/cstddef
rm /opt/rocm/llvm/include/llvm/Support/cstddef
