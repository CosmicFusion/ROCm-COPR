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
mkdir -p %{buildroot}/opt/rocm
touch %{buildroot}/opt/rocm/.cxx-links
echo "link successful ." > %{buildroot}/opt/rocm/.cxx-links

%files
/opt/rocm/.cxx-links

%post
ln -s /usr/include/c++/*/cstddef  /opt/rocm/llvm/include/clang/Basic/cstddef
ln -s /usr/include/c++/*/cstddef /opt/rocm/llvm/include/llvm/Support/cstddef

%postun
rm /opt/rocm/llvm/include/clang/Basic/cstddef
rm /opt/rocm/llvm/include/llvm/Support/cstddef
