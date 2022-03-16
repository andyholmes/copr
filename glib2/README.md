# glib2

This a build of GLib with a patch necessary for some utilities to run in
GitHub Actions.

More specifically it handles `EPERM` for instances of Docker and libseccomp
which don’t recognise `close_range()` so block calls to it under a default
security policy which returns `EPERM` rather than `ENOSYS`.

See: https://gitlab.gnome.org/Infrastructure/GitLab/-/issues/545
