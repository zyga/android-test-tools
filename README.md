About
=====

Tools for documenting and discovering tests that exist in Android (AOSP).

Android has a lot of tests but it's easy to get lost in the maze. As
Linaro's android team strives to run more tests automatically with LAVA
we need a checklist to track our progress.

This repository will contain simple database of tests, what they are for, 
how to run them, what they may require from the hardware and lastly,
if we support them via LAVA.

Usage
=====

The basic use case is to compare a non-test build to a test build. The test
build can be obtained by building with TARGET_BUILD_VARIANT=tests. The next
step is to run a script on both builds, like this:

```
$ git clone git://github.com/zyga/android-test-tools.git
$ cd android-test-tools
$ ./compare-builds.py /path/to/base/build /path/to/other/build
```

