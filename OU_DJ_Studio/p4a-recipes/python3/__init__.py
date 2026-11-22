from pythonforandroid.recipes.python3 import Python3Recipe as UpstreamPython3Recipe


class AndroidPython3Recipe(UpstreamPython3Recipe):
    # The upstream reproducible-buildinfo patch targets an older CPython
    # Makefile.pre.in context and fails against the pinned Python 3.12.8.
    # Exclude only that obsolete patch; keep all other upstream patches.
    patches = [
        patch
        for patch in UpstreamPython3Recipe.patches
        if "reproducible-buildinfo.diff" not in str(patch)
    ] + [
        "android-disable-grp-enumeration.patch",
    ]


recipe = AndroidPython3Recipe()
