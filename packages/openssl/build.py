from scripts import tools
import os

def build_openssl():
    os.makedirs(tools.BUILD_DIR_DEBUG)
    os.makedirs(tools.BUILD_DIR_RELEASE)

    platform = ''
    if os.environ["CXX_COMPILER"] == 'msvc':
        tools.cmd('export CC=clang-cl')
        tools.cmd('export CXX=clang-cl++')
        tools.cmd('export AR=llvm-ar')
        tools.cmd('export RANLIB=llvm-ranlib')
        platform = 'VC-WIN64A'

    # https://aka.ms/vs/15/release/vs_BuildTools.exe
    perl = 'wine /strawberry-perl/perl/bin/perl.exe'
    os.chdir(tools.BUILD_DIR_DEBUG)
    tools.cmd(f'{perl} --version')
    tools.cmd(f'{perl} {tools.SOURCE_DIR}/Configure {platform} --prefix={tools.INSTALL_DIR_DEBUG} --debug no-tests no-shared no-asm')
    # tools.cmd(f'{perl} {tools.SOURCE_DIR}/Configure')
    tools.cmd(f'make -j $(nproc)')
    tools.cmd(f'make install_sw')

    os.chdir(tools.BUILD_DIR_RELEASE)
    tools.cmd(f'{perl} {tools.SOURCE_DIR}/Configure {platform} --prefix={tools.INSTALL_DIR_RELEASE} --release no-tests no-shared no-asm')
    tools.cmd(f'make -j $(nproc)')
    tools.cmd(f'make install_sw')

tools.install_build_requirements(extra_unix_dependencies = [])

tools.clone_git_repository(git_repository = "https://github.com/openssl/openssl.git",
                           git_tag = "openssl-3.1.1")

build_openssl()

tools.archive_generic_package(files = [
    [tools.SOURCE_DIR + "/include/openssl", "include/openssl"],
    [tools.SOURCE_DIR + "/include/crypto", "include/crypto"],
    [tools.INSTALL_DIR_DEBUG + f"/lib64/{tools.release_lib_name('crypto')}", f"lib-debug/{tools.release_lib_name('crypto')}"],
    [tools.INSTALL_DIR_DEBUG + f"/lib64/{tools.release_lib_name('ssl')}", f"lib-debug/{tools.release_lib_name('ssl')}"],
    [tools.INSTALL_DIR_RELEASE + f"/lib64/{tools.release_lib_name('crypto')}", f"lib-release/{tools.release_lib_name('crypto')}"],
    [tools.INSTALL_DIR_RELEASE + f"/lib64/{tools.release_lib_name('ssl')}", f"lib-release/{tools.release_lib_name('ssl')}"],
])