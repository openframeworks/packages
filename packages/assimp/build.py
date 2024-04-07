from scripts.tools import LibraryBuilder

class Builder(LibraryBuilder):
    name = "assimp"
    version = "5.3.1"

    def source(self):
        self.source_git_repo("https://github.com/assimp/assimp.git", "v5.3.1")

    def build(self):
        self.build_generic_cmake_project()
        
    def package(self):
        self.archive_generic_package()
