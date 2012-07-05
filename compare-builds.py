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


def find_all_apks(root):
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".apk"):
                yield os.path.join(dirpath, filename)[len(root):]


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
