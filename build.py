import sys
import importlib
import scripts.tools as tools

# Usage: python build.py <package_name>

def main():
    if len(sys.argv) != 2:
        print('Usage: python build.py <package_name>')
        sys.exit(1)

    package_name = sys.argv[1]
    builder = getattr(importlib.import_module(f'packages.{package_name}.build'), 'Builder')()
    
    if hasattr(builder, 'source'):
        tools.log("Sourcing build files ...")
        builder.source()
        tools.log("Sourcing build files ... Done")

    if hasattr(builder, 'patch_sources'):
        tools.log("Patching source files ...")
        builder.patch_sources()
        tools.log("Patching source files ... Done")

    if hasattr(builder, 'depends'):
        tools.log("Fetching dependencies ...")
        builder.depends()
        tools.log("Fetching dependencies ... Done")

    if hasattr(builder, 'build'):
        tools.log("Building the package ...")
        builder.build()
        tools.log("Building the package ... Done")

    if hasattr(builder, 'package'):
        tools.log("Packaging build artifacts ...")
        builder.package()
        tools.log("Packaging build artifacts ... Done")
        
    tools.log("Build process is done")

if __name__ == '__main__':
    main()
