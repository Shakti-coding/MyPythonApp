[app]

# (str) Title of your application
title = MyApp

# (str) Package name
package.name = myapp

# (str) Package domain (unique identifier, e.g. org.example.myapp)
package.domain = org.myapp

# (str) Source code directory (where main.py is located)
source.dir = .

# (list) File extensions to include in the package
source.include_exts = py,txt,md

# (str) Application version
version = 0.1

# (list) Application requirements (comma-separated)
# include kivy + flask stack + networking
requirements = python3,kivy,flask,werkzeug,jinja2,markupsafe,itsdangerous,click,requests,certifi,charset-normalizer,idna,urllib3,pyjnius

# (str) Presplash image
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon image
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0

# (list) Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API (must match installed SDK platform)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version (tested with 25b)
android.ndk = 25b

# (bool) Use private app storage (default=True)
android.private_storage = True

# (str) Android archs to build for
android.archs = arm64-v8a,armeabi-v7a

# (bool) Skip Android SDK updates
android.skip_update = False

# (bool) Accept Android SDK licenses automatically
android.accept_sdk_license = True

# (str) Bootstrap to use (sdl2 is the default)
p4a.bootstrap = sdl2


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Warn if running as root (0 = False, 1 = True)
warn_on_root = 1
