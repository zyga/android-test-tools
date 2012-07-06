#!/usr/bin/env python3
# :vim: set sw=4 ts=4 expandtab
# Copyright (C) 2012 Zygmunt Krynicki
"""
Simple tool that compares two builds that differ by TARGET_BUILD_VARIANT
Ideally one is using 'eng' while the other is using 'tests'.
"""

import argparse
import logging.config
import os


class AndroidBuildTree:
    """
    Simple class wrapping an android build tree, built with default output
    directory (out)
    """

    def __init__(self, out_dir, product):
        """
        Initialize the build tree located at the specified out_dir.
        The build is done for the specified product.
        """
        if not os.path.isdir(out_dir):
            raise ValueError("not a directory: %s" % out_dir)
        # Check that we really point to the out directory.
        # Chomp any trailing slashes so that os.path.split() returns 'out'
        # instead of the empty string
        out_dir = out_dir.rstrip("/")
        if not os.path.split(out_dir)[1] == 'out':
            raise ValueError("not pointing to 'out' directory: %s" % out_dir)
        if not os.path.isdir(
            os.path.join(out_dir, 'target', 'product', product)):
            raise ValueError("not a build tree for product: %s" % product)
        self._out_dir = out_dir
        self._product = product

    def _without_out(self, pathname):
        """
        Return the pathname without the 'out' directory
        """
        if not pathname.startswith(self._out_dir):
            raise ValueError("%s does is not in the out directory" % pathname)
        return pathname[len(self._out_dir):]

    def find_all_apks(self):
        """
        Generator returning all *.apk files in the build tree
        """
        for dirpath, dirnames, filenames in os.walk(self._out_dir):
            for filename in filenames:
                if filename.endswith(".apk"):
                    pathname = os.path.join(dirpath, filename)
                    yield self._without_out(pathname)
    
    def find_all_executables_in(self, root):
        """
        Generator returning all the executables in the specified root
        directory. The root must be a subdirectory of the out_dir
        """
        if not root.startswith(self._out_dir):
            raise ValueError(root)
        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                pathname = os.path.join(dirpath, filename)
                if os.access(pathname, os.X_OK):
                    yield self._without_out(pathname)

    def find_all_executables(self):
        """
        Generator returning all the executable files in the build tree
        """
        for executable in self.find_all_executables_in(self.system_bin_path):
            yield executable
        for executable in self.find_all_executables_in(self.system_xbin_path):
            yield executable

    @property
    def system_bin_path(self):
        "The system/bin path"
        return os.path.join(self._out_dir, 'target', 'product',
                            self._product, 'system', 'bin')

    @property
    def system_xbin_path(self):
        "The system/xbin path"
        return os.path.join(self._out_dir, 'target', 'product',
                            self._product, 'system', 'xbin')

def setup_logging():
    logging.config.dictConfig({
        'version': 1,
        "formatters": {
            "brief": {
                "format": "%(levelname)-8s: %(name)-15s: %(message)s"
            },
            "full": {
                "format": "%(asctime)s %(name)-15s %(levelname)-8s %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "brief",
                "level": "INFO",
                "stream": "ext://sys.stdout"
            },
            "console_priority": {
                "class": "logging.StreamHandler",
                "formatter": "full",
                "level": "ERROR",
                "stream": "ext://sys.stderr"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "console_priority"]
        }
    })


def main():
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "base_build", metavar="BASE",
        help="Base directory that we compare")
    parser.add_argument(
        "other_build", metavar="OTHER",
        help="The other directory that we compare")
    parser.add_argument(
        "--extra-apks", metavar="FILE",
        type=argparse.FileType(mode="wt"),
        help="Save a list of APKs that are only in the other build",
        default="extra-apks.txt")
    parser.add_argument(
        "--extra-execs", metavar="FILE",
        type=argparse.FileType(mode="wt"),
        help="Save a list of executables that are only in the other build",
        default="extra-execs.txt")
    parser.add_argument(
        "-p", "--product",
        required=True,
        help="The product name (for example, pandaboard)")
    args = parser.parse_args()
    try:
        base_build = AndroidBuildTree(args.base_build, args.product)
        other_build = AndroidBuildTree(args.other_build, args.product)
    except ValueError as exc:
        parser.error(exc.message)
    # Build a list of APKs in the base build
    logging.debug("Looking for APKs in the base build...")
    base_apks = frozenset(base_build.find_all_apks())
    for apk in sorted(base_apks):
        logging.debug("%s", apk)
    logging.info("Found %s apks in the base build...", len(base_apks))
    # Build a list of APKs in the other build
    logging.debug("Looking for APKs in the other build...")
    other_apks = frozenset(other_build.find_all_apks())
    for apk in sorted(other_apks):
        logging.debug("%s", apk)
    logging.info("Found %s apks in the other build...", len(other_apks))
    # Compile a list of differences and save it
    logging.info("Found %d apks that are not in the base build",
                 len(other_apks - base_apks))
    logging.info("Writing apks that are not in the base build to %s",
                 args.extra_apks.name)
    for apk in sorted(other_apks - base_apks):
        print(apk, file=args.extra_apks)
    # Build a list of executables in the base build
    base_execs = frozenset(base_build.find_all_executables())
    logging.info("Found %s executables in the base build",
                 len(base_execs))
    # Build a list of executables in the other build
    other_execs = frozenset(other_build.find_all_executables())
    logging.info("Found %s executables in the other build",
                 len(other_execs))
    # Compile a list of differences and save it
    logging.info("Found %d executables that ar not in the base build",
                 len(other_execs - base_execs))
    logging.info("Writing executables that are not in the base build to %s",
                 args.extra_execs.name)
    for executable in sorted(other_execs - base_execs):
        print(executable, file=args.extra_execs)

if __name__ == "__main__":
    main()
