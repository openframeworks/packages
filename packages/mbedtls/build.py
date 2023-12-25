from scripts.tools import LibraryBuilder

class Builder(LibraryBuilder):
    name = "mbedtls"
    version = "3.4.0"

    def source(self):
        self.source_git_repo("https://github.com/Mbed-TLS/mbedtls.git", "v3.4.0")

    def build(self):
        self.build_generic_cmake_project(["-DENABLE_TESTING=OFF", "-DENABLE_PROGRAMS=OFF", "-DGEN_FILES=ON"])
        
    def package(self):
        self.archive_generic_package()
