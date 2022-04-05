#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	A minimalistic user-space library oriented to Netlink developers
Summary(pl.UTF-8):	Minimalistyczna biblioteka przestrzeni użytkownika dla programistów Netlinka
Name:		libmnl
Version:	1.0.5
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.netfilter.org/projects/libmnl/files/%{name}-%{version}.tar.bz2
# Source0-md5:	0bbb70573119ec5d49435114583e7a49
URL:		http://www.netfilter.org/projects/libmnl/index.html
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.6
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libtool >= 2:2
BuildRequires:	rpm-build >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmnl is a minimalistic user-space library oriented to Netlink
developers. There are a lot of common tasks in parsing, validating,
constructing of both the Netlink header and TLVs that are repetitive
and easy to get wrong. This library aims to provide simple helpers
that allows you to re-use code and to avoid re-inventing the wheel.
The main features of this library are:

- Small: the shared library requires around 30kB for an x86-based
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

%description -l pl.UTF-8
libmnl to minimalistyczna biblioteka przestrzeni użytkownika
przeznaczona dla programistów interfejsu Netlink. Wiele wspólnych
zadań, takich jak analiza, sprawdzanie poprawności i tworzenie zarówno
nagłówka Netlink, jak i TLV jest powtarzalnych i łatwo w nich o błędy.
Ta biblioteka ma na celu dostarczenie prostych funkcji pomocniczych,
pozwalających wykorzystywać ten sam kod i zapobiegająca wynajdowaniu
koła na nowo. Główne cechy tej biblioteki to:
 - mały rozmiar: biblioteka współdzielona dla x86 wymaga ok. 30kB
 - prostota: biblioteka unika złożoności i szczegółowych abstrakcji,
   które kryją się w szczegółach Netlinka
 - łatwość użycia: biblioteka upraszcza pracę programistów interfejsu
   Netlink; dostarcza funkcje ułatwiające obsługę gniazd, tworzenie
   komunikatów, sprawdzanie poprawności, analizę i śledzenie sekwencji
 - łatwość ponownego wykorzystania: biblioteki można użyć do stworzenia
   własnej warstwy abstrakcji poziom wyżej
 - niezależność: zależności między poszczególnymi elementami biblioteki
   są ograniczone, tzn. biblioteka udostępnia wiele funkcji pomocniczych,
   ale programista nie musi używać ich wszystkich.

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
BuildArch:	noarch

%description apidocs
API and internal documentation for libmnl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmnl.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{!?with_apidocs:--without-doxygen}
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
%attr(755,root,root) %{_libdir}/libmnl.so
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
