%define url_ver %(echo %{version} | cut -d. -f1,2)
%define	fname	pt
%define major	%{version}
%define libname	%mklibname %{fname} %{major}
%define devname	%mklibname %{fname} -d


Summary:	Portable Tool Library
Name:		ptlib
Version:	2.10.11
Release:	2
License:	MPL
Group:		System/Libraries
Url:		https://www.opalvoip.org
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/ptlib/%{url_ver}/%{name}-%{version}.tar.xz
Patch1:		ptlib-2.10.10-mga-bison-parameter.patch
Patch2:		ptlib-gcc5.patch
Patch3:		ptlib-2.10.11-gcc6.patch
Patch4:		ptlib-2.10.11-gcc7.patch
Patch5:		ptlib-2.10.11-uio.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	sed
BuildRequires:	libdc1394_12-devel
BuildRequires:	openldap-devel
BuildRequires:	unixODBC-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libavc1394)
BuildRequires:	pkgconfig(libdv)
BuildRequires:	pkgconfig(libraw1394) < 2.0.0
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sdl)
# We are not ready for that yet
BuildConflicts:	pkgconfig(libdc1394-2)
BuildConflicts:	pkgconfig(libraw1394) >= 2.0.0

%description
PTLib is a C++ multi-platform abstraction library that has its genesis
many years ago as a method to produce applications to run on both
Microsoft Windows and Unix systems. It also was to have a Macintosh
port but this never eventuated.

This is the GNOME.org version of ptlib.

%package -n	%{libname}
Summary:	Portable Windows Libary
Group:		System/Libraries
Requires:	%{libname}-plugins >= %{version}-%{release}

%description -n	%{libname}
PTLib is a C++ multi-platform abstraction library that has its genesis
many years ago as a method to produce applications to run on both
Microsoft Windows and Unix systems. It also was to have a Macintosh
port but this never eventuated.

This is the GNOME.org version of ptlib.

%package -n	%{devname}
Summary:	Portable Windows Libary development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{mklibname pwlib -d}

%description -n	%{devname}
Header files and libraries for developing applications that use ptlib.

%package -n	%{libname}-plugins
Summary:	Main plugins for ptlib
Group:		System/Libraries
Provides:	%{name}-plugins = %{version}-%{release}
Provides:	%{name}-plugins-alsa = %{version}-%{release}
Provides:	%{name}-plugins-oss = %{version}-%{release}
Provides:	%{name}-plugins-pulseaudio = %{version}-%{release}
Provides:	%{name}-plugins-v4l2 = %{version}-%{release}

%description -n	%{libname}-plugins
This package contains the oss, alsa, pulseaudio and v4l2 plugins for ptlib.

%package -n	%{libname}-plugins-dc
Summary:	Dc plugin for ptlib
Group:		System/Libraries
Provides:	%{name}-plugins-dc = %{version}-%{release}

%description -n	%{libname}-plugins-dc
This package contains the dc plugin for ptlib.

%package -n	%{libname}-plugins-avc
Summary:	AVC plugin for ptlib
Group:		System/Libraries
Provides:	%{name}-plugins-avc = %{version}-%{release}

%description -n	%{libname}-plugins-avc
This package contains the AVC plugin for ptlib.

%prep
%setup -q
%autopatch -p1

%build
export CC=gcc
export CXX=g++
%configure \
	--enable-v4l2 \
	--enable-plugins \
	--enable-oss \
	--enable-avc \
	--enable-dc

%make RPM_OPT_FLAGS="%{optflags}"

%install
%makeinstall_std

%multiarch_includes %{buildroot}%{_includedir}/ptbuildopts.h

%multiarch_includes %{buildroot}%{_includedir}/ptlib/pluginmgr.h

#fix doc perms
chmod a+r *.txt

#remove unpackaged files
rm -f %{buildroot}%{_datadir}/ptlib/make/*.{pat,in,lib64,libname,ptlibdir,includesdir}

# fix ptlib-config
install -d %{buildroot}%{_bindir}
ln -snf %{_datadir}/ptlib/make/ptlib-config %{buildroot}%{_bindir}/ptlib-config

# fix strange perms
find %{buildroot} -type d -perm 0700 -exec chmod 755 {} \;
find %{buildroot} -type f -perm 0555 -exec chmod 755 {} \;
find %{buildroot} -type f -perm 0444 -exec chmod 644 {} \;
find %{buildroot}%{_libdir} -type f -name '*.so*' -exec chmod 755 {} \;

# it's not stable at major version level...
rm -f %{buildroot}%{_libdir}/libpt.so.?
rm -f %{buildroot}%{_libdir}/libpt.so.?.?

%files -n %{libname}
%{_libdir}/libpt.so.%{major}*

%files -n %{devname}
%doc *.txt
%{_bindir}/ptlib-config
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*
%{_datadir}/%{name}

%files -n %{libname}-plugins
%dir %{_libdir}/%{name}-%{version}
%dir %{_libdir}/%{name}-%{version}/devices
%dir %{_libdir}/%{name}-%{version}/devices/sound
%dir %{_libdir}/%{name}-%{version}/devices/videoinput
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/alsa_pwplugin.so
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/oss_pwplugin.so
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/pulse_pwplugin.so
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/videoinput/v4l2_pwplugin.so

%files -n %{libname}-plugins-dc
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/videoinput/dc_pwplugin.so

%files -n %{libname}-plugins-avc
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/videoinput/avc_pwplugin.so

