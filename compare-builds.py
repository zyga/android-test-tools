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
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "base_build", metavar="BASE",
        help="Base directory that we compare")
    parser.add_argument(
        "other_build", metavar="OTHER",
        help="The other directory that we compare")
    args = parser.parse_args()
    if not os.path.isdir(args.base_build):
        parser.error("Not a directory: %s" % args.base_build)
    if not os.path.isdir(args.other_build):
        parser.error("Not a directory: %s" % args.other_dir)
    # Build a list of APKs in the base build
    logging.debug("Looking for APKs in the base build...")
    base_apks = frozenset(find_all_apks(args.base_build))
    for apk in sorted(base_apks):
        logging.debug("%s", apk)
    logging.info("Found %s apks in the base build...", len(base_apks))
    # Build a list of APKs in the other build
    logging.debug("Looking for APKs in the other build...")
    other_apks = frozenset(find_all_apks(args.other_build))
    for apk in sorted(other_apks):
        logging.debug("%s", apk)
    logging.info("Found %s apks in the other build...", len(other_apks))
    # Compile a list of differences and save it
    logging.info("Found %d apks that are not in the base build",
                 len(other_apks - base_apks))
    # TODO: Build a list of binaries


if __name__ == "__main__":
    main()
