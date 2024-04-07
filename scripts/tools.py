import os
import sys
import git
import shutil
import tarfile
import platform
import urllib.request

def log(msg):
    print(f'[OF] >> {msg}')

class LibraryBuilder:
    def __init__(self):
        self.compiler_id = os.environ.get('COMPILER_ID', "unknown")
        self.cc_compiler = os.environ.get('CC_COMPILER', "unknown")
        self.cxx_compiler = os.environ.get('CXX_COMPILER', "unknown")
        self.cc_compiler_package = os.environ.get('CC_COMPILER_PACKAGE', None)
        self.cxx_compiler_package = os.environ.get('CXX_COMPILER_PACKAGE', None)
        self.toolchain_file = os.environ.get('TOOLCHAIN_FILE', None)
        self.architecture = os.environ.get('ARCHITECTURE', 'unknown')

        self.repo_dir = os.getcwd()
        self.working_dir = os.path.join(self.repo_dir, 'temp', self.name)
        self.source_dir = os.path.join(self.working_dir, 'source')
        self.debug_build_dir = os.path.join(self.working_dir, 'build_debug')
        self.release_build_dir = os.path.join(self.working_dir, 'build_release')
        self.install_dir = os.path.join(self.working_dir, 'install')
        self.archive_dir = os.path.join(self.working_dir, 'archive')
        self.output_dir = os.path.join(self.repo_dir, 'out')

        self.package_suffix = f"-{self.version}-{platform.system().lower()}-{self.architecture}-{self.compiler_id}"
        self.archive_filename = f'{self.name}{self.package_suffix}.tar.gz'

        log(f'Building package {self.name}/{self.version}')
        log(f'Cleaning working directory {self.working_dir} ...')
        if os.path.exists(self.working_dir):
            git.rmtree(self.working_dir)
        log(f'Cleaning working directory {self.working_dir} ... Done')

    def cmd(self, command):
        log(f'Executing command: {command}')
        if os.system(command) != 0:
            raise Exception(f'Failed to execute command: {command}')

    def replace_in_file(self, file, find, replace):
        log(f"Replacing text '{find}' with '{replace}' in file {file}")
        with open(file, 'r') as f:
            content = f.read()
        content = content.replace(find, replace)
        with open(file, 'w') as f:
            f.write(content)

    def append_to_file(self, file, append):
        log(f"Appending text '{append}' to file {file}")
        with open(file, 'a') as f:
            f.write(append)

    def remove_file(self, file):
        log(f"Removing file {file}")
        os.remove(file)

    def insert_head_file(self, file, insert):
        log(f"Inserting '{insert}' at the front in file {file}")
        with open(file, 'r') as f:
            content = f.read()
        content = insert + content
        with open(file, 'w') as f:
            f.write(content)

    def source_git_repo(self, git_repository, git_tag):
        log(f"Sourcing git repository {git_repository}:{git_tag} ...")
        self.cmd('git config --global advice.detachedHead false')
        self.cmd(f'git clone {git_repository} {self.source_dir} --depth=1 --single-branch --branch={git_tag}')
        log(f"Sourcing git repository {git_repository}:{git_tag} ... Done")

    def install_build_dependencies(self, extra_unix_dependencies = []):
        if platform.system() == 'Linux':
            if self.compiler_id != "unknown" and self.compiler_id != 'msvc':
                extra_unix_dependencies.append(os.environ['CC_COMPILER_PACKAGE'])
                extra_unix_dependencies.append(os.environ['CXX_COMPILER_PACKAGE'])
            
            deps = ' '.join(extra_unix_dependencies)
            log(f"Installing extra unix dependencies ...")
            if os.system(f'apt-get update && apt-get install -y {deps}') != 0:
                self.cmd(f'sudo apt-get update && sudo apt-get install -y {deps}')
            log(f"Installing extra unix dependencies ... Done")

    def pull_of_dependency(self, package, version):
        depsdir = self.get_dependency_dir(package)
        log(f'Fetching package {package}/{version} ...')
        if not os.path.exists(depsdir):
            url = "https://github.com/openframeworks/packages/releases/download/latest/" + package + "-" + version + "-" + platform.system().lower() + "-" + self.architecture + "-" + self.compiler_id + ".tar.gz"
            log(f'Downloading {url} ...')
            archive = tarfile.open(fileobj=urllib.request.urlopen(url), mode="r|gz")
            archive.extractall(path=depsdir)
            archive.close()
            log(f'Downloading {url} ... Done')
        log(f'Fetching package {package}/{version} ... Done')

    def get_dependency_dir(self, package):
        return os.path.join(self.working_dir, 'deps', package).replace("\\", "/")

    def build_generic_cmake_project(self, 
                                    cmake_args = [], 
                                    cmake_module_paths = [], 
                                    cmake_args_debug = [], 
                                    cmake_args_release = []):

        if self.toolchain_file != None and self.toolchain_file != "":
            cmake_args.append(f'-DCMAKE_TOOLCHAIN_FILE={os.path.join(self.repo_dir, self.toolchain_file)}')
        else:
            if self.compiler_id != "unknown" and self.compiler_id != 'msvc':
                cmake_args.append(f'-DCMAKE_C_COMPILER={self.cc_compiler}')
                cmake_args.append(f'-DCMAKE_CXX_COMPILER={self.cxx_compiler}')

        cmake_args.append(f'-DBUILD_SHARED_LIBS=OFF')
        cmake_args.append(f'-DPython_ROOT_DIR={os.path.dirname(sys.executable)}')
        cmake_args.append(f'-DPython3_ROOT_DIR={os.path.dirname(sys.executable)}')

        if cmake_module_paths != []:
            cmake_args.append(f'-DCMAKE_MODULE_PATH={";".join(cmake_module_paths)}')

        os.makedirs(self.debug_build_dir, exist_ok=True)
        os.makedirs(self.release_build_dir, exist_ok=True)

        args_debug = []
        args_debug.append(f'-DCMAKE_BUILD_TYPE=Debug')
        args_debug.append(f'-DCMAKE_INSTALL_PREFIX={self.install_dir}')
        args_debug.append(' '.join(cmake_args))
        args_debug.append(' '.join(cmake_args_debug))
        args_debug.append('-DCMAKE_DEBUG_POSTFIX=-d')

        args_release = []
        args_release.append(f'-DCMAKE_BUILD_TYPE=Release')
        args_release.append(f'-DCMAKE_INSTALL_PREFIX={self.install_dir}')
        args_release.append(' '.join(cmake_args))
        args_release.append(' '.join(cmake_args_release))

        log(f'Building Debug configuration ...')
        self.cmd(f'cmake -G Ninja {self.source_dir} -B {self.debug_build_dir} {" ".join(args_debug)}')
        self.cmd(f'cmake --build {self.debug_build_dir} --config Debug --target install')
        log(f'Building Debug configuration ... Done')

        log(f'Building Release configuration ...')
        self.cmd(f'cmake -G Ninja {self.source_dir} -B {self.release_build_dir} {" ".join(args_release)}')
        self.cmd(f'cmake --build {self.release_build_dir} --config Release --target install')
        log(f'Building Release configuration ... Done')

    def archive_generic_package(self, files = None):
        log(f'Archiving as a generic package ...')
        os.makedirs(self.archive_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        if files != None:
            for file in files:
                sourcefile = ''
                targetfile = ''

                if len(file) == 2:
                    sourcefile = file[0]
                    targetfile = os.path.join(self.archive_dir, file[1])
                else:
                    sourcefile = os.path.join(file[0], file[1])
                    targetfile = os.path.join(self.archive_dir, file[2])

                if os.path.isdir(sourcefile):
                    shutil.copytree(sourcefile, targetfile, dirs_exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(targetfile), exist_ok=True)
                    shutil.copy(sourcefile, targetfile)
        else:
            shutil.copytree(self.install_dir, self.archive_dir, dirs_exist_ok=True)

        archive = os.path.join(self.output_dir, self.archive_filename)
        if os.path.exists(archive):
            os.remove(archive)

        with tarfile.open(archive, 'x:gz') as tar:
            for file in os.listdir(os.path.abspath(self.archive_dir)):
                filepath = os.path.join(self.archive_dir, file)
                tar.add(filepath, arcname = os.path.basename(filepath))
                
        log(f'Archiving as a generic package ... Done')
