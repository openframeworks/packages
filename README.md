# openFrameworks packages

This repository is the successor to [apothecary](https://github.com/openframeworks/apothecary). It is the central place where all [openFrameworks](https://github.com/openframeworks/openframeworks) dependencies are built and managed, and downloaded on-demand by openFrameworks projects.

All packages are built and served completely automated with CI, so all you have to do is commit something and wait. The package is automatically built and uploaded into the latest Release.

# Overview about architectures

Following architectures are supported:

|Architecture|Description|
|-|-|
|x64|Your typical PC architecture, synonymous to `x86_64` or `amd64`|
|armv7|Typical 32-bit ARM architecture with Hardware-Float, synonymous to `aarch32`. Most RPI's use this, except for RPI Zero, which uses `armv6` and does not support Hardware-Float|
|aarch64|64-bit ARM architecture, synonymous to `armv8`. RPI 4 and onwards support this architecture (with the correct OS).|

Currently, `armv6` is not provided as it is unlikely that anyone would want to run OpenFrameworks on a Raspberry PI Zero, as it has very limited processing power and is unlikely to be enough for an OpenFrameworks application anyways.

## Hosted packages

All prebuilt binary packages can be found at:  
https://github.com/openframeworks/packages/releases/tag/latest

They are intended to be downloaded by scripts, not users.

## Building a package locally

You can build a single package locally, using the compiler that is being picked up by CMake.

```bash
python build.py <package_name>
# Example: python build.py freeimage
```

The selected package will be built locally using the compiler chosen by CMake. Thus, you can only test packages for the compiler and architecture you are running on. See the workflow files to see what environment variables to set, if you are on Linux and want to test cross-compilation locally.

When the package finished building, an archive package consisting of all binaries, headers and CMake files will be generated in an `out/` directory.

You need a working Ninja backend.

Some packages also include a `requirements.txt` file which contains pip dependencies. You might need to manually install these too.
