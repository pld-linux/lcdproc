Summary:	LCDproc displays real-time system information on a 20x4 backlit LCD
Summary(pl.UTF-8):	LCDproc wyświetla aktualne informacje o systemie na wyświetlaczu LCD 20x4
Name:		lcdproc
Version:	0.4.5
Release:	3
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/lcdproc/%{name}-%{version}.tar.bz2
# Source0-md5:	2d342eb87c550a46629ec3efb1d70f49
Source1:	LCDd.init
# Extracted from tweaked lcdproc source
# http://venky.ws/projects/imon/
Patch0:		%{name}-imon.patch
URL:		http://lcdproc.omnipotent.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LCDproc is a client/server suite inclduding drivers for all kinds of
nifty LCD displays. The server supports several serial devices: Matrix
Orbital, Crystal Fontz, Bayrad, LB216, LCDM001 (kernelconcepts.de),
Wirz-SLI and PIC-an-LCD; and some devices connected to the LPT port:
HD44780, STV5730, T6963, SED1520 and SED1330. Various clients are
available that display things like CPU load, system load, memory
usage, uptime, and a lot more.

%description -l pl.UTF-8
LCDproc jest narzędziem w architekturze klient/serwer zawierającym
sterowniki do wyświetlaczy LCD takich jak podłączane przez port
szeregowy: Matrix Orbital, Crystal Fontz, Bayrad, LB216, LCDM001
(kernelconcepts.de), Wirz-SLI i PIC-an-LCD; oraz przez port
równoległy: HD44780, STV5730, T6963, SED1520 i SED1330. Dostępne są
programy klienckie monitorujące m.in. obciążenie procesora, systemu,
zajętość pamięci, czas pracy i wiele innych.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
CPPFLAGS="-I/usr/include/ncurses"; export CPPFLAGS

%configure \
	--enable-stat-nfs \
	--enable-stat-smbfs \
	--enable-drivers="mtxorb,cfontz,curses,text,lb216,hd44780,joy,irman,bayrad,glk,stv5730,sed1330,sed1520,lcdm001,t6963,imon"

%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir}/lcdproc}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/LCDd

# conf files
install LCDd.conf scripts/lcdproc.conf $RPM_BUILD_ROOT%{_sysconfdir}/lcdproc

echo "-s localhost -p 13666 C M X U P S" > \
			$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc/lcdproc.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* INSTALL TODO ChangeLog
%dir %{_sysconfdir}/lcdproc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lcdproc/*
%attr(754,root,root) /etc/rc.d/init.d/LCDd
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
