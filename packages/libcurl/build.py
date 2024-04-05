from scripts.tools import LibraryBuilder
import os

class Builder(LibraryBuilder):
    name = "libcurl"
    version = "8.7.1"

    def source(self):
        self.source_git_repo("https://github.com/curl/curl.git", "curl-8_7_1")

    def patch_sources(self):
        self.remove_file(file = os.path.join(self.source_dir, "CMake", "FindMbedTLS.cmake"))
        self.append_to_file(
            file = os.path.join(self.source_dir, "CMakeLists.txt"),
            append = "target_link_libraries(libcurl_static PUBLIC MbedTLS::mbedtls)\n",
        )

    def depends(self):
        self.pull_of_dependency("mbedtls", "3.4.0")

    def build(self):
        self.build_generic_cmake_project(
            [
                "-DBUILD_SHARED_LIBS=OFF", 
                "-DBUILD_CURL_EXE=OFF",
                "-DENABLE_UNICODE=ON",
                "-DCURL_USE_OPENSSL=OFF",
                "-DCURL_USE_MBEDTLS=ON",
                "-DSHARE_LIB_OBJECT=OFF",
                f'-DCMAKE_PREFIX_PATH="{self.get_dependency_dir("mbedtls")}"',
            ]
        )
        
    def package(self):
        self.archive_generic_package()