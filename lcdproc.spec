Summary:	LCDproc displays real-time system information on a 20x4 backlit LCD
Summary(pl):	LCDproc wy¶wietla aktualne informacje o systemie na wy¶wietlaczu LCD 20x4
Name:		lcdproc
Version:	0.4.3
Release:	3
License:	GPL
Group:		Applications/System
Source0:	http://lcdproc.omnipotent.net.net/%{name}-%{version}.tar.bz2
Source1:	LCDd.init
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

%description -l pl
LCDproc jest narzêdziem w architekturze klient/serwer zawieraj±cym
sterowniki do wy¶wietlaczy LCD takich jak pod³±czane przez port
szeregowy: Matrix Orbital, Crystal Fontz, Bayrad, LB216, LCDM001
(kernelconcepts.de), Wirz-SLI i PIC-an-LCD; oraz przez port
równoleg³y: HD44780, STV5730, T6963, SED1520 i SED1330. Dostêpne s±
programy klienckie monitoruj±ce m.in. obci±¿enie procesora, systemu,
zajêto¶æ pamiêci, czas pracy i wiele innych.

%prep
%setup -q

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
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
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir}/lcdproc}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/lcdproc/*
%attr(754,root,root) /etc/rc.d/init.d/LCDd
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
