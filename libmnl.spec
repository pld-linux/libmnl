#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	A minimalistic user-space library oriented to Netlink developers
Name:		libmnl
Version:	1.0.1
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://www.netfilter.org/projects/libmnl/files/%{name}-%{version}.tar.bz2
# Source0-md5:	e936236bb57a2375afa4e70e75dc3ba9
URL:		http://www.netfilter.org/projects/libmnl/index.html
%{?with_apidocs:BuildRequires:	doxygen}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmnl is a minimalistic user-space library oriented to Netlink
developers. There are a lot of common tasks in parsing, validating,
constructing of both the Netlink header and TLVs that are repetitive
and easy to get wrong. This library aims to provide simple helpers
that allows you to re-use code and to avoid re-inventing the wheel.
The main features of this library are:

- Small: the shared library requires around 30KB for an x86-based
  computer.
- Simple: this library avoids complexity and elaborated abstractions
  that tend to hide Netlink details.
- Easy to use: the library simplifies the work for Netlink-wise
  developers. It provides functions to make socket handling, message
  building, validating, parsing and sequence tracking, easier.
- Easy to re-use: you can use the library to build your own
  abstraction layer on top of this library.
- Decoupling: the interdependency of the main bricks that compose the
  library is reduced, i.e. the library provides many helpers, but the
  programmer is not forced to use them.

%package devel
Summary:	Header files for libmnl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmnl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libmnl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmnl.

%package static
Summary:	Static libmnl library
Summary(pl.UTF-8):	Statyczna biblioteka libmnl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmnl library.

%description static -l pl.UTF-8
Statyczna biblioteka libmnl.

%package apidocs
Summary:	libmnl API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmnl
Group:		Documentation

%description apidocs
API and internal documentation for libmnl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmnl.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static}
%{__make}
%{?with_apidocs:doxygen doxygen.cfg}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libmnl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmnl.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmnl.so
%{_libdir}/libmnl.la
%{_includedir}/libmnl
%{_pkgconfigdir}/libmnl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmnl.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxygen/html/*
%endif
