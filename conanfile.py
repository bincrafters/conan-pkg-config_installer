#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
from conans.errors import ConanInvalidConfiguration
import os


class PkgConfigConan(ConanFile):
    name = "pkg-config_installer"
    version = "0.29.2"
    description = "The pkg-config program is used to retrieve information about installed libraries in the system"
    topics = ("conan", "pkg-config", "package config")
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://github.com/original_author/original_lib"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-2.0-or-later"
    exports = ["LICENSE.md"]
    settings = "os_build", "arch_build", "compiler"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    @property
    def _is_mingw_windows(self):
        return self.settings.os_build == "Windows" and self.settings.compiler == "gcc" and os.name == "nt"

    def build_requirements(self):
        if self._is_mingw_windows:
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def source(self):
        source_url = "https://pkg-config.freedesktop.org/releases/pkg-config-%s.tar.gz" % self.version
        tools.get(source_url,
                  sha256="6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591")
        os.rename("pkg-config-" + self.version, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            # http://www.linuxfromscratch.org/lfs/view/systemd/chapter06/pkg-config.html
            args = ["--with-internal-glib", "--disable-host-tool"]
            env_build = AutoToolsBuildEnvironment(self, self._is_mingw_windows)
            env_build.configure(args=args)
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        if self._is_mingw_windows:
            mingw_bin = os.path.join(self.deps_cpp_info["mingw_installer"].rootpath, "bin")
            self.copy(pattern="libwinpthread-1.dll", dst="bin", src=mingw_bin)

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
