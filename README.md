# ROCm for Fedora Linux
This repository hosts a collection of [Fedora](https://getfedora.org/)
RPM SPEC Sheets for the
[AMD ROCm Platform](https://www.amd.com/en/graphics/servers-solutions-rocm).
These SPEC Sheets implement a great portion of the stack, ranging from low-level
interfaces, over compilers to high-level application libraries.

## Installation
The Fedora Linux packages for ROCm are available on the
[My COPR Repo](https://copr.fedorainfracloud.org/coprs/cosmicfusion/ROCm-GFX8P).

More instructions can be found there.

## Recommendations for building from source

ROCm stack comprises around 50 packages including a fork of LLVM.
Therefore, building all packages from source can take a long time .

To speed up compilation of application libraries like `rocblas` or `rocfft` export `AMDGPU_TARGETS`
and set it to the architecture name of your GPU. To find out this name, install `rocminfo`,
```bash
sudo dnf install rocminfo
```
and call
```bash
rocminfo | grep gfx
```
for VEGA 56/64 the output is
```bash
  Name:                    gfx900
        Name:                    amdgcn-amd-amdhsa--gfx900:xnack-
```
Hence, you have to set `AMDGPU_TARGETS` to `gfx900`,
```bash
export AMDGPU_TARGETS="gfx900"
```

Some commonly used compiler flags are unsupported by `clang` (and thus `hipcc`) from `rocm-llvm`,
including stack protection,
```bash
-fstack-protector-all
-fstack-protector-strong
-fstack-protector
```

We have patched in an ability for hipcc to allow to change it's C & CXX flags :
this ability can be leveraged by these 2 env vars

for CXX

```
HIP_ENV_CXX_FLAGS
```

for C

```
HIP_ENV_CC_FLAGS
```

Use the the same way you use regular C & CXX flags.

See the [official documentation](https://docs.amd.com/bundle/ROCm-Compiler-Reference-Guide-v5.2/page/Appendix_A.html) for a full list.

For additional installation configuration, such as adding a user to the `video`
group, we refer to AMD's
[installation guide](https://docs.amd.com/bundle/ROCm-Installation-Guide-v5.2/page/Prerequisite_Actions.html).


## Contributing
Your contribution is always welcome. Before making a pull request, please open
an issue at the [issue tracker](https://github.com/CosmicFusion/ROCm-COPR/issues)
to report the problem with build/error logs.

and add it to your commit.
As we want to bring ROCm into COPR we would greatly appreciate if you test that the package builds in a clean chroot such as mock.

## Thanks [rocm-arch](https://github.com/rocm-arch/rocm-arch)
for putting your README.md file out there so i can steal it .
