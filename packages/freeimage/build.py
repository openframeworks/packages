from scripts.tools import LibraryBuilder

class Builder(LibraryBuilder):
    name = "freeimage"
    version = "3.19.0"

    def source(self):
        # self.source_git_repo("https://github.com/danoli3/FreeImage.git", "test3.19.0")
        self.source_git_repo("https://github.com/danoli3/FreeImage.git", "master")

    def build(self):
        self.build_generic_cmake_project()
        
    def package(self):
        self.archive_generic_package()
