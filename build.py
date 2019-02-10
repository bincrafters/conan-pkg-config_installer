#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_installer, build_shared
import os

if __name__ == "__main__":

    arch = os.environ["ARCH"]
    builder = build_template_installer.get_builder()
    settings = {"os": build_shared.get_os(), "arch_build": arch, "arch": arch}
    if "MINGW_CONFIGURATIONS" in os.environ:
        configs = os.environ["MINGW_CONFIGURATIONS"]
        for config in configs.split(","):
            tokens = config.strip().split('@')
            settings["compiler"] = "gcc"
            settings["compiler.version"] = tokens[0]
            settings["arch"] = tokens[1]
            settings["compiler.exception"] = tokens[2]
            settings["compiler.threads"] = tokens[3]
            settings["compiler.libcxx"] = "libstdc++11"
            build_requires = {"*": "mingw_installer/1.0@conan/stable"}
            builder.add(settings, {}, {}, build_requires)
    else:
        builder.add(settings, {}, {}, {})
    builder.run()
