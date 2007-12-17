%define	realname Teng
%define	modname	teng
%define	dirname	%{modname}
%define soname	%{modname}.so
%define inifile	22_%{modname}.ini

Summary:	The %{realname} module for PHP
Name:		php-%{modname}
Version:	1.0.0
Release:	%mkrel 8
Group:		Development/PHP
License:	LGPL
URL:		http://teng.sourceforge.net/
Source0:	php4-%{modname}-%{version}.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libteng-devel

%description
This is a dynamic shared object (DSO) that adds Teng support to PHP.

%prep

%setup -q -n php4-%{modname}-%{version}

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=%{_prefix}

%make
mv modules/*.so .
chrpath -d %{soname}

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP.
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CREDITS README.%{modname}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
