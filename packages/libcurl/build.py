from scripts import tools
import os

tools.install_build_requirements(extra_unix_dependencies = ["python3", "python3-pip"])
tools.cmd("pip3 install jsonschema jinja2")

tools.clone_git_repository(git_repository = "https://github.com/Mbed-TLS/mbedtls.git",
                           git_tag = "v3.4.0",
                           working_dir = "/mbedtls")

tools.insert_before_file(file = "/mbedtls/source/CMakeLists.txt", insert = "set(CMAKE_C_COMPILER_ID MSVC)\n") # Patching so it thinks it's MSVC

tools.build_generic_cmake_project(working_dir = "/mbedtls",
                                  cmake_args = ["-DENABLE_TESTING=OFF",
                                                "-DENABLE_PROGRAMS=OFF",
                                                "-DBUILD_SHARED_LIBS=OFF",
                                                "-DGEN_FILES=ON"])

tools.clone_git_repository(git_repository = "https://github.com/curl/curl.git",
                           git_tag = "curl-8_1_2")

tools.build_generic_cmake_project(cmake_args = ["-DBUILD_SHARED_LIBS=OFF", 
                                                "-DBUILD_CURL_EXE=OFF",
                                                "-DENABLE_UNICODE=ON",
                                                "-DCURL_USE_MBEDTLS=ON"])

tools.archive_generic_package(files = [
    [tools.SOURCE_DIR + "/include/openssl", "include/openssl"],
    [tools.SOURCE_DIR + "/include/crypto", "include/crypto"],
    [tools.INSTALL_DIR_DEBUG + f"/lib64/{tools.release_lib_name('crypto')}", f"lib-debug/{tools.release_lib_name('crypto')}"],
    [tools.INSTALL_DIR_DEBUG + f"/lib64/{tools.release_lib_name('ssl')}", f"lib-debug/{tools.release_lib_name('ssl')}"],
    [tools.INSTALL_DIR_RELEASE + f"/lib64/{tools.release_lib_name('crypto')}", f"lib-release/{tools.release_lib_name('crypto')}"],
    [tools.INSTALL_DIR_RELEASE + f"/lib64/{tools.release_lib_name('ssl')}", f"lib-release/{tools.release_lib_name('ssl')}"],
])