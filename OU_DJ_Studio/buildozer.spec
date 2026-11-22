[app]
title = OU DJ Studio
package.name = oudjstudio
package.domain = com.oubuilder
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0.0
requirements = python3==3.12.8,hostpython3==3.12.8,kivy==2.3.1
orientation = landscape
fullscreen = 1
android.permissions = READ_MEDIA_AUDIO,READ_EXTERNAL_STORAGE
android.api = 35
android.minapi = 24
android.archs = arm64-v8a
android.ndk = 25b
android.allow_backup = True
android.accept_sdk_license = True
p4a.bootstrap = sdl2
p4a.branch = master
p4a.local_recipes = p4a-recipes
[buildozer]
log_level = 2
warn_on_root = 1
