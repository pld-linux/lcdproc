Summary:	LCDproc displays real-time system information on a 20x4 backlit LCD.
Summary(pl):	LCDproc wy¶wietla aktualne informacje o systemie na 20x4 wy¶wietlaczu LCD.
Name:		lcdproc
Version:	0.4.3
Release:	2
License:	GPL
URL:		http://lcdproc.omnipotent.net/
Group:		Applications/System
Source0:	http://lcdproc.omnipotent.net.net/%{name}-%{version}.tar.bz2
Source1:	LCDd.init
BuildRequires:	ncurses-devel
BuildRequires:	libtool
BuildRequires:	automake
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LCDproc is a client/server suite inclduding drivers for all kinds of
nifty LCD displays. The server supports several serial devices: Matrix
Orbital, Crystal Fontz, Bayrad, LB216, LCDM001 (kernelconcepts.de),
Wirz-SLI and PIC-an-LCD; and some devices connected to the LPT port:
HD44780, STV5730, T6963, SED1520 and SED1330. Various clients are
available that display things like CPU load, system load, memory
usage, uptime, and a lot more.

%description -l pl
LCDproc jest narzêdziem w architekturze klient/serwer zawieraj±cym
sterowniki do wy¶wietlaczy LCD takiech jak pod³±czane przez port
szeregowy: Matrix Orbital, Crystal Fontz, Bayrad, LB216, 
LCDM001 (kernelconcepts.de), Wirz-SLI and PIC-an-LCD; oraz przez
port równoleg³y: HD44780, STV5730, T6963, SED1520 and SED1330.
i klientów monitoruj±cych m.in. obci±zenie procesora, systemu,
zajêto¶æ pamiêci, czas pracy i wiele innych.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q

%build
rm -f missing
%{__libtoolize}
aclocal
%{__autoconf}
%{__automake}
CPPFLAGS="-I%{_includedir}/ncurses"; export CPPFLAGS

%configure \
	--enable-stat-nfs \
	--enable-stat-smbfs \
	--enable-drivers="mtxorb,cfontz,curses,text,lb216,hd44780,joy,irman,bayrad,glk,stv5730,sed1330,sed1520,lcdm001,t6963"

%{__make} CFLAGS="%{rpmcflags}" 

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

# init
install -d 		$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install %SOURCE1	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/LCDd

# conf files
install -d		$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc
install LCDd.conf 	$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc/LCDd.conf
touch scripts/lcdproc.conf  	$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc/lcdproc.conf
echo "-s localhost -p 13666 C M X U P S" > \
			$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc/lcdproc.conf

%post

%preun


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%dir %{_sysconfdir}/lcdproc
%config(noreplace) %{_sysconfdir}/lcdproc/*
%doc README* INSTALL COPYING TODO ChangeLog
%defattr(-, root, root, 0700)
%config(noreplace) %{_sysconfdir}/rc.d/init.d/LCDd
