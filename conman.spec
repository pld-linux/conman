Summary:	The Console Manager
Summary(pl.UTF-8):	Zarządca konsol
Name:		conman
Version:	0.1.9.2
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://download.gna.org/conman/0.1.9.2/%{name}-%{version}.tar.bz2
# Source0-md5:	8e737e64ae3dfac37bd93df38ac0f6cb
Source1:	%{name}d.init
Source2:	%{name}d.sysconfig
Source3:	%{name}.logrotate
URL:		http://home.gna.org/conman/
BuildRequires:	libwrap-devel
Requires(post,preun):	/sbin/ldconfig
Requires:	rc-scripts
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ConMan is a console management program designed to support a large
number of console devices and simultaneous users. It currently
supports local serial devices and remote terminal servers (via the
telnet protocol).

%description -l pl.UTF-8
ConMan to program do zarządzania konsolami zaprojektowany do obsługi
dużej liczby urządzeń konsolowych i jednoczesnych użytkowników.
Aktualnie obsługuje lokalne urządzenia szeregowe i zdalne serwery
terminali (poprzez protokół telnet).

%prep
%setup -q

%build
%configure \
	--with-tcp-wrappers

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d}
install -d $RPM_BUILD_ROOT/var/log/conman

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/conmand
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/conmand
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/conmand

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/examples

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add conmand
%service conmand restart

%preun
if [ "$1" = "0" ]; then
        %service conmand stop
        /sbin/chkconfig --del conmand
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ NEWS
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_libdir}/%{name}
%dir %{_var}/log/conman
%{_mandir}/man*/*

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(754,root,root) /etc/rc.d/init.d/conmand
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/conmand
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
