%define glib2_version 2.73.3

%global tarball_version %%(echo %{version} | tr '~' '.')

# Not yet sure whether to have libproxy in el10, but assume yes for now.
%global with_libproxy 1

Name:           glib-networking
Version:        2.78.0
Release:        1.tsan
Summary:        Networking support for GLib

License:        LGPLv2+
URL:            https://gitlab.gnome.org/GNOME/glib-networking
Source0:        https://download.gnome.org/sources/glib-networking/2.78/%{name}-%{tarball_version}.tar.xz

BuildRequires:  ca-certificates
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
%if 0%{?with_libproxy}
BuildRequires:  pkgconfig(libproxy-1.0)
%endif
BuildRequires:  pkgconfig(p11-kit-1)
BuildRequires:  systemd-rpm-macros

Requires:       ca-certificates
Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       gsettings-desktop-schemas

# For glib-pacrunner
Recommends:     libproxy-duktape

%description
This package contains modules that extend the networking support in
GIO. In particular, it contains libproxy- and GSettings-based
GProxyResolver implementations and a gnutls-based GTlsConnection
implementation.

%package tests
Summary: Tests for the glib-networking package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The glib-networking-tests package contains tests that can be used to verify
the functionality of the installed glib-networking package.

%prep
%autosetup -p1 -n %{name}-%{tarball_version}

%build
%meson \
%if !0%{?with_libproxy}
  -Dlibproxy=disabled \
  -Denvironment_proxy=enabled \
%endif
  -Dinstalled_tests=true \
  %nil
%meson_build

%install
%meson_install

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc NEWS README
%{_libdir}/gio/modules/libgiognomeproxy.so
%{_libdir}/gio/modules/libgiognutls.so
%if 0%{?with_libproxy}
%{_libdir}/gio/modules/libgiolibproxy.so
%{_libexecdir}/glib-pacrunner
%{_datadir}/dbus-1/services/org.gtk.GLib.PACRunner.service
%{_userunitdir}/glib-pacrunner.service
%else
%{_libdir}/gio/modules/libgioenvironmentproxy.so
%endif

%files tests
%{_libexecdir}/installed-tests/glib-networking
%{_datadir}/installed-tests

%changelog
%autochangelog
