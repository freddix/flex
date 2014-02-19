Summary:	GNU fast lexical analyzer generator
Name:		flex
Version:	2.5.38
Release:	2
License:	BSD-like
Group:		Development/Tools
Source0:	http://downloads.sourceforge.net/sourceforge/flex/%{name}-%{version}.tar.bz2
# Source0-md5:	b230c88e65996ff74994d08a2a2e0f27
Patch0:		%{name}-locale.patch
URL:		http://flex.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
# m4-quotes* patches require rebuilding *.c from scan.l
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	help2man
BuildRequires:	texinfo
BuildRequires:	util-linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fPIC

%description
This is the GNU fast lexical analyzer generator. It generates lexical
tokenizing code based on a lexical (regular expression based)
description of the input. It is designed to work with both yacc and
bison, and is used by many programs as part of their build process.

%prep
%setup -q
%patch0 -p1

# diable pdf build
%{__sed} -i "/dist_doc_DATA/d" doc/Makefile.am

# diable test failing with bison 2.6.x
%{__sed} -i -e "/test-bison-yylloc/d" -e "/test-bison-yylval/d" tests/Makefile.am

# force regeneration
%{__rm} skel.c

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
    --disable-shared
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{zh_tw,zh_TW}

ln -sf flex $RPM_BUILD_ROOT%{_bindir}/lex
ln -sf flex $RPM_BUILD_ROOT%{_bindir}/flex++

echo .so flex.1 > $RPM_BUILD_ROOT%{_mandir}/man1/flex++.1
echo .so flex.1 > $RPM_BUILD_ROOT%{_mandir}/man1/lex.1

%find_lang %{name}

%check
%{__make} check

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/flex*
%{_libdir}/*.a
%{_includedir}/*.h

