from conan import ConanFile
from conan.tools.build import cross_building
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import load
import re


class CLI11Conan(ConanFile):
    name = "cli11"
    description = "Command Line Interface toolkit for C++11"
    topics = ("cli", "c++11", "parser", "cli11")
    url = "https://github.com/CLIUtils/CLI11"
    homepage = "https://github.com/CLIUtils/CLI11"
    author = "Henry Schreiner <hschrein@cern.ch>"
    license = "BSD-3-Clause"

    settings = "os", "compiler", "arch", "build_type"
    exports_sources = (
        "LICENSE",
        "README.md",
        "include/*",
        "src/*",
        "extern/*",
        "cmake/*",
        "CMakeLists.txt",
        "CLI11.CPack.Description.txt",
        "tests/*",
    )

    def set_version(self):
        try:
            content = load(self, "include/CLI/Version.hpp")
            version = re.search(r'#define CLI11_VERSION "(.*)"', content).group(1)
            self.version = version
        except Exception:
            self.version = None

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CLI11_BUILD_EXAMPLES"] = "OFF"
        tc.variables["CLI11_SINGLE_FILE"] = "OFF"
        tc.generate()

    def build(self):  # this is not building a library, just tests
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if not cross_building(self):
            cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "CLI11")
        self.cpp_info.set_property("cmake_target_name", "CLI11::CLI11")

    def package_id(self):
        self.info.clear()
