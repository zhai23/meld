
About Meld
==========

Meld is a visual diff and merge tool targeted at developers. Meld helps you
compare files, directories, and version controlled projects. It provides
two- and three-way comparison of both files and directories, and supports
many version control systems including Git, Mercurial, Bazaar, CVS and Subversion.

Meld helps you review code changes, understand patches, and makes enormous
merge conflicts slightly less painful.

Meld is licensed under the GPL v2 or later.


Requirements
------------

* Python 3.6
* pycairo (Python3 bindings for cairo without GObject layer)
* PyGObject 3.30 (Python3 bindings for GObject introspection)
* gsettings-desktop-schemas

And following packages with GObject introspection:

* GLib 2.36
* Pango
* PangoCairo
* GTK+ 3.20
* GtkSourceView 4.0


Build requirements
------------------

* Python 3.6
* Meson 0.48
* Ninja
* gettext
* GLib 2.36 and its development utilities such as `glib-compile-schemas`

For Windows build requirements, see `mingw-common` section `.gitlab-ci.yml`


Running
-------

You *do not* need to build Meld in order to run it. Meld can be run directly
from this source directory by running:

```sh
$ bin/meld
```

Unix users should get Meld from their distribution package manager, or from
[Flathub](https://flathub.org/).

Windows users should download the provided MSIs on the
[Meld home page](https://meld.app/).

OSX users can install Meld using Homebrew (or Macports, Fink, etc.), or there
are unofficial native builds available from the
[Meld for OSX](https://yousseb.github.io/meld/) project.



Developing
----------

## Setting up the Dev environment ##

First install PyGObject related packages:
```sh
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 python-gi-dev python3-cairo-dev
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
```

For other operating system, see https://pygobject.readthedocs.io/en/latest/getting_started.html#ubuntu-getting-started

Now install meld specific development tools
`sudo apt install intltool libgtksourceview-4-dev gtksourceview-4 meson ninja itstool appstream-util`

Finally install the python packages:

```sh
python3 -m pip install -r dev-requirements.txt
```

It's easy to get started developing Meld. From a git checkout, just run
`bin/meld`.

We also support development using Flatpak via GNOME Builder. At the Builder
"Clone..." dialog, enter https://gitlab.gnome.org/GNOME/meld.git, and the
default build + run development flow using Flatpak should work.

## Running the unit tests ##
To run the unit tests simply run:
`pytest`


Building
--------

Meld uses [meson](https://mesonbuild.com/) build system. Use the following
commands to build Meld from the source directory:

```sh
$ meson setup _build
$ cd _build
$ ninja
```

## Running locally build version ##
After building, assuming you are in the build directory,
you can run your modified version via:

```sh
./bin/meld
```

You can then install Meld system-wide by running:

```sh
$ ninja install
```

A Windows installer can be built with command

```powershell
C:\Python34\python.exe setup_win32.py bdist_msi
```

which will create the file `dist/Meld-VERSION-ARCH.msi`.


Contributing
------------

Meld uses GNOME's GitLab to track bugs, and user questions and development
discussions happen on the Meld mailing list. The development team is small,
and new contributors are always welcome!

List of issues: https://gitlab.gnome.org/GNOME/meld/issues

Support forum:  https://discourse.gnome.org/tag/meld



Links
-----

Home page:      https://meld.app/

Documentation:  https://meld.app/help/

Wiki:           https://wiki.gnome.org/Apps/Meld
