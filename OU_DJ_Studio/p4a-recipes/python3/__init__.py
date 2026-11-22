from pythonforandroid.recipes.python3 import Python3Recipe as UpstreamPython3Recipe


class AndroidPython3Recipe(UpstreamPython3Recipe):
    patches = UpstreamPython3Recipe.patches + [
        "android-disable-grp-enumeration.patch",
    ]


recipe = AndroidPython3Recipe()
