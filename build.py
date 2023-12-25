import sys
import importlib

# Usage: python build.py <package_name>

def main():
    if len(sys.argv) != 2:
        print('Usage: python build.py <package_name>')
        sys.exit(1)

    package_name = sys.argv[1]
    builder = getattr(importlib.import_module(f'packages.{package_name}.build'), 'Builder')()

    builder.install_build_dependencies()
    
    if hasattr(builder, 'source'):
        builder.source()

    if hasattr(builder, 'patch_sources'):
        builder.patch_sources()

    if hasattr(builder, 'depends'):
        builder.depends()

    if hasattr(builder, 'build'):
        builder.build()

    if hasattr(builder, 'package'):
        builder.package()

if __name__ == '__main__':
    main()
