#!/usr/bin/env python3
# :vim: set sw=4 ts=4 expandtab
# Copyright (C) 2012 Zygmunt Krynicki
"""
A tool to compare two lists of files from different Android builds.
It is intended to be used to compare Ice Cream Sandwitch with Jelly Bean
"""

import argparse
import os


def drop_target_product_foo(items):
    """
    Drops the initial /target/product/*/ from the list of strings.
    """
    for item in items:
        item_parts = item.split(os.path.sep)
        if item_parts[0:3] == ['', 'target', 'product']:
            yield os.path.sep.join(item_parts[4:])
        else:
            raise ValueError(
                "%r must start with /target/product/" % item_parts)


def load_list(pathname, chomp_target_product=True):
    with open(pathname) as stream:
        result = ((line.strip() for line in stream))
        if chomp_target_product:
            result = drop_target_product_foo(result)
        result = frozenset(result)
        return result


def main():
    parser = argparse.ArgumentParser(epilog=__doc__)
    parser.add_argument(
        "list_a", metavar="list-a",
        help="File with the first list")
    parser.add_argument(
        "list_b", metavar="list-b",
        help="File with the second list")
    args = parser.parse_args()
    list_a = load_list(args.list_a)
    list_b = load_list(args.list_b)
    print("# Not present in list-a but added to list-b")
    print("# (in {1} but not in {0})".format(args.list_a, args.list_b))
    for item in sorted(list_b - list_a):
        print("+{0}".format(item))
    print("# Present in list-a but removed from list-b")
    print("# (in {0} but not in {1})".format(args.list_a, args.list_b))
    for item in sorted(list_a - list_b):
        print("-{0}".format(item))


if __name__ == "__main__":
    main()
