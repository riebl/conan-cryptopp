from conans import ConanFile, ConfigureEnvironment
from conans import tools
import os
import shutil


class CryptoPPConan(ConanFile):
    name = "cryptopp"
    version = "5.6.3"
    url = "https://github.com/riebl/conan-cryptopp"
    settings = "os", "compiler", "build_type", "arch"
    license = "Boost Software License 1.0"
    options = {"static": [True, False], "shared": [True, False]}
    default_options = "static=False", "shared=True"

    def source(self):
        zipname = 'cryptopp563.zip'
        url = 'http://cryptopp.com/%s' % zipname
        sha256 = '9390670a14170dd0f48a6b6b06f74269ef4b056d4718a1a329f6f6069dc957c9'
        tools.download(url, zipname)
        tools.check_sha256(zipname, sha256)
        tools.unzip(zipname)
        os.unlink(zipname)
        shutil.move('config.h', 'config.orig')
        shutil.move('config.recommend', 'config.h')

    def build(self):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        if self.options.static:
            self.run('%s make static' % env.command_line)
        if self.options.shared:
            self.run('%s make dynamic' % env.command_line)

    def package(self):
        self.copy(pattern="*.h", dst="include/cryptopp", src=".")
        self.copy(pattern="*.so", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["cryptopp"]