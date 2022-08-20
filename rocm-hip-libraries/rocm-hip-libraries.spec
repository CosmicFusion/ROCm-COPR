%define _build_id_links none

%global ROCM_MAJOR_VERSION 5
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 3
%global ROCM_MAGIC_VERSION 109
%global ROCM_INSTALL_DIR /opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
%global ROCM_LIBPATCH_VERSION 50203


Requires:      rocm-hip-runtime-devel

Provides:      rocm-hip-libraries
Provides:      rocm-hip-libraries(x86-64)

Requires:	rocsparse-devel
Requires:	rocprim-devel
Requires:	hipcub-devel
Requires:	rocfft-devel
Requires:	rocrand-devel
Requires:	hipblas-devel
Requires:	rocprim-devel
Requires: 	rccl-devel
Requires: 	hipfort-devel		
Requires: 	rocalution-devel
Requires:	rocthrust-devel
Requires: 	hipsparse-devel
Requires:	hipfft-devel

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildArch:     x86_64
Name:          rocm-hip-libraries
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}.%{ROCM_LIBPATCH_VERSION}
Release:       copr%{?dist}
License:       NCSA
Group:         System Environment/Libraries
Summary:       Radeon Open Compute (ROCm) HIP development libraries

%description
Radeon Open Compute (ROCm) HIP development libraries

%build

# Make basic structure

mkdir -p %{buildroot}/src

cd %{buildroot}/src


# Level 1 : Create versioning from official packaging

## file N2 from official repos (rocm-hip-libraries) :

mkdir -p %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info

touch %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-hip-libraries

echo "%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}-%{ROCM_MAGIC_VERSION}" > %{buildroot}/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-hip-libraries

#

%files
/opt/rocm-%{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}/.info/version-hip-libraries
%exclude /src


%post
/sbin/ldconfig

%postun
/sbin/ldconfig
