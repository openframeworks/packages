from scripts import tools

tools.install_build_requirements(extra_unix_dependencies = [])

tools.clone_git_repository(git_repository = "https://github.com/g-truc/glm", 
                           git_tag = "0.9.9.8")

tools.archive_manual_package([
    ["CMakeLists.txt", "CMakeLists.txt"],
    ["glm", "include/glm"],
])