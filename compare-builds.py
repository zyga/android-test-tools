#!/usr/bin/env python
# :vim: set sw=4 ts=4 expandtab
# Copyright (C) 2012 Zygmunt Krynicki
"""
Simple tool that compares two builds that differ by TARGET_BUILD_VARIANT
Ideally one is using 'eng' while the other is using 'tests'.
"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("base_build", metavar="BASE",
                       help="Base directory that we compare")
    parser.add_argument("other_build", metavar="OTHER",
                       help="The other directory that we compare")
    args = parser.parse_args()
    if not os.path.isdir(args.base_build):
        parser.error("Not a directory: %s" % args.base_build)
    if not os.path.isdir(args.other_build):
        parser.error("Not a directory: %s" % args.other_dir)
    # TODO: Build a list of APKs
    # TODO: Build a list of binaries


if __name__ == "__main__":
    main()
