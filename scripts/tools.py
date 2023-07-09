import os
import shutil

LLVM_NATIVE_TOOLCHAIN = '/usr/lib/llvm-15'
MSVC_TOOLCHAIN_FILE = '/llvm/llvm/cmake/platforms/WinMsvc.cmake'
MSVC_HOST_ARCH = 'x86_64'
LLVM_WINSYSROOT = '/msvc'
MSVC_VER = '14.36.32532'
WINSDK_VER = '10.0.22000.0'

WORKING_DIR = '/temp'
SOURCE_DIR = WORKING_DIR + '/source'
BUILD_DIR_DEBUG = WORKING_DIR + '/build-debug'
BUILD_DIR_RELEASE = WORKING_DIR + '/build-release'
INSTALL_DIR_DEBUG = WORKING_DIR + '/install-debug'
INSTALL_DIR_RELEASE = WORKING_DIR + '/install-release'

def cmd(command):
    if os.system(command) != 0:
        raise Exception(f'Failed to execute command: {command}')
    
def native_lib_name(name):
    if (os.environ['CXX_COMPILER'] == 'msvc'):
        return f'{name}.lib'
    else:
        return f'lib{name}.a'
    
def native_pdb_name(name):
    return f'{name}.pdb'

def clone_git_repository(git_repository, git_tag):
    if (os.path.exists(WORKING_DIR)):
        shutil.rmtree(WORKING_DIR)

    cmd('git config --global advice.detachedHead false')
    cmd(f'git clone {git_repository} {SOURCE_DIR} --depth=1 --single-branch --branch={git_tag}')

def install_build_requirements(extra_unix_dependencies = []):
    if (os.environ['CXX_COMPILER'] != 'msvc'):
        cc = os.environ['CC_COMPILER_PACKAGE']
        cxx = os.environ['CXX_COMPILER_PACKAGE']
        deps = ' '.join(extra_unix_dependencies)
        cmd(f'apt-get install -y {cc} {cxx} {deps}')
    else:
        pass

def build_generic_cmake_project(cmake_args = []):
    if (os.environ['CXX_COMPILER'] == 'msvc'):
        cmake_args.append(f'-DCMAKE_SYSTEM_NAME=Windows')
        cmake_args.append(f'-DCMAKE_TOOLCHAIN_FILE={MSVC_TOOLCHAIN_FILE}')
        cmake_args.append(f'-DHOST_ARCH={MSVC_HOST_ARCH}')
        cmake_args.append(f'-DLLVM_NATIVE_TOOLCHAIN={LLVM_NATIVE_TOOLCHAIN}')
        cmake_args.append(f'-DLLVM_WINSYSROOT={LLVM_WINSYSROOT}')
        cmake_args.append(f'-DMSVC_VER={MSVC_VER}')
        cmake_args.append(f'-DWINSDK_VER={WINSDK_VER}')
    else:
        cmake_args.append(f'-DCMAKE_C_COMPILER={os.environ["CC_COMPILER"]}')
        cmake_args.append(f'-DCMAKE_CXX_COMPILER={os.environ["CXX_COMPILER"]}')
        if (os.environ["TOOLCHAIN_FILE"] != ''):
            cmake_args.append(f'-DCMAKE_TOOLCHAIN_FILE={os.environ["TOOLCHAIN_FILE"]}')

    cmake_args.append(f'-DBUILD_SHARED_LIBS=OFF')

    os.makedirs(BUILD_DIR_DEBUG, exist_ok=True)
    os.makedirs(BUILD_DIR_RELEASE, exist_ok=True)

    cmd(f'cmake -G Ninja {SOURCE_DIR} -B {BUILD_DIR_DEBUG} {" ".join(cmake_args)} -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX={INSTALL_DIR_DEBUG}')
    cmd(f'cmake -G Ninja {SOURCE_DIR} -B {BUILD_DIR_RELEASE} {" ".join(cmake_args)} -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX={INSTALL_DIR_RELEASE}')

    cmd(f'cmake --build {BUILD_DIR_DEBUG} -j $(nproc)')
    cmd(f'cmake --build {BUILD_DIR_DEBUG} --target install')

    cmd(f'cmake --build {BUILD_DIR_RELEASE} -j $(nproc)')
    cmd(f'cmake --build {BUILD_DIR_RELEASE} --target install')

def rename_debug_libfile(name, 
                         install_dir_debug = INSTALL_DIR_DEBUG, 
                         install_dir_release = INSTALL_DIR_RELEASE):
    if os.path.exists(install_dir_debug + f'/lib/{name}d.lib'):
        os.rename(install_dir_debug + f'/lib/{name}d.lib', install_dir_debug + f'/lib/{name}.lib')

    if os.path.exists(install_dir_release + f'/lib/{name}d.lib'):
        os.rename(install_dir_release + f'/lib/{name}d.lib', install_dir_release + f'/lib/{name}.lib')

def archive_generic_package(output_library_name, 
                            package_name, 
                            cmake_file = '/repo/cmake/generic/import.cmake'):
    os.makedirs(WORKING_DIR + '/archive/debug/lib', exist_ok=True)
    os.makedirs(WORKING_DIR + '/archive/release/lib', exist_ok=True)
    os.makedirs('/package/out', exist_ok=True)

    rename_debug_libfile(package_name)

    shutil.copy(cmake_file, WORKING_DIR + '/archive/')
    shutil.copy(INSTALL_DIR_DEBUG + f'/lib/{native_lib_name(output_library_name)}', WORKING_DIR + '/archive/debug/lib/')
    shutil.copy(INSTALL_DIR_RELEASE + f'/lib/{native_lib_name(output_library_name)}', WORKING_DIR + '/archive/release/lib/')

    if os.path.exists(INSTALL_DIR_DEBUG + f'/lib/{native_pdb_name(output_library_name)}'):
        shutil.copy(INSTALL_DIR_DEBUG + f'/lib/{native_pdb_name(output_library_name)}', WORKING_DIR + '/archive/debug/lib/')

    shutil.copytree(INSTALL_DIR_DEBUG + '/include', WORKING_DIR + '/archive/debug/include')
    shutil.copytree(INSTALL_DIR_RELEASE + '/include', WORKING_DIR + '/archive/release/include')

    cmd(f'cd {WORKING_DIR}/archive && tar -zcvf /package/out/{os.environ["FULL_PACKAGE_NAME"]}.tar.gz *')

def archive_manual_package(files):
    os.makedirs(WORKING_DIR + '/archive', exist_ok=True)
    os.makedirs('/package/out', exist_ok=True)

    for file in files:
        sourcefile = SOURCE_DIR + '/' + file[0]
        targetfile = WORKING_DIR + '/archive/' + file[1]

        if os.path.isdir(sourcefile):
            shutil.copytree(sourcefile, targetfile)
        else:
            shutil.copy(sourcefile, targetfile)

    cmd(f'cd {WORKING_DIR}/archive && tar -zcvf /package/out/{os.environ["FULL_PACKAGE_NAME"]}.tar.gz *')