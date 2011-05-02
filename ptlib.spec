%define	fname	pt

%define version		2.8.3
%define major		%version
%define libname		%mklibname %{fname} %{major}
%define develname	%mklibname %{fname} -d

Summary:	Portable Tool Library
Name:		ptlib
Version:	%version
Release:	%mkrel 2
License:	MPL
Group:		System/Libraries
URL:		http://www.opalvoip.org
# Always use the GNOME.org version, not the opalvoip.org version. The
# major user of ptlib and opal is Ekiga, and Ekiga is designed to work
# with the GNOME.org versions of these libraries, not the opalvoip.org
# versions. - AdamW 2008/09
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/ptlib/%{name}-%{version}.tar.bz2
BuildRequires:	alsa-lib-devel
BuildRequires:	esound-devel
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:  expat-devel
BuildRequires:	flex
BuildRequires:	gcc-c++
BuildRequires:	libavc1394-devel
BuildRequires:  libdc1394_12-devel >= 0.9.5
BuildRequires:	libdv-devel
BuildRequires:	libraw1394_8-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	SDL-devel
BuildRequires:	libv4l-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	unixODBC-devel
BuildRequires:	sed
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildConflicts: libdc1394-devel >= 2.0.0

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
Obsoletes:	%{mklibname pt 2} < 2.4.1-2mdv

%description -n	%{libname}
PTLib is a C++ multi-platform abstraction library that has its genesis
many years ago as a method to produce applications to run on both
Microsoft Windows and Unix systems. It also was to have a Macintosh
port but this never eventuated.

This is the GNOME.org version of ptlib.

%package -n	%{develname}
Summary:	Portable Windows Libary development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{mklibname pwlib -d}

%description -n	%{develname}
Header files and libraries for developing applications that use ptlib.

%package -n	%{libname}-plugins
Summary:	Main plugins for ptlib
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-plugins = %{version}-%{release}
Provides:	%{name}-plugins-alsa = %{version}-%{release}
Provides:	%{name}-plugins-oss = %{version}-%{release}
Provides:	%{name}-plugins-v4l = %{version}-%{release}
Provides:	%{name}-plugins-v4l2 = %{version}-%{release}
Obsoletes:	%{mklibname pt 2}-plugins < 2.4.1-2mdv

%description -n	%{libname}-plugins
This package contains the oss, alsa, v4l1 and v4l2 plugins for ptlib.

%package -n	%{libname}-plugins-dc
Summary:	Dc plugin for ptlib
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-plugins-dc = %{version}-%{release}
Obsoletes:	%{mklibname pt 2}-plugins-dc < 2.4.1-2mdv

%description -n	%{libname}-plugins-dc
This package contains the dc plugin for ptlib.

%package -n	%{libname}-plugins-avc
Summary:	AVC plugin for ptlib
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-plugins-avc = %{version}-%{release}
Obsoletes:	%{mklibname pt 2}-plugins-avc < 2.4.1-2mdv

%description -n	%{libname}-plugins-avc
This package contains the AVC plugin for ptlib.

%prep
%setup -q

%build
%configure2_5x \
    --enable-v4l2 \
    --disable-v4l \
    --enable-plugins \
    --enable-oss \
    --enable-esd \
    --enable-avc \
    --enable-dc

%make RPM_OPT_FLAGS="%{optflags}"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc *.txt
%attr(0755,root,root) %{_bindir}/ptlib-config
%attr(0755,root,root) %{_libdir}/*.so
%{_libdir}/*.*a
%{_includedir}/*
%{multiarch_includedir}/ptbuildopts.h
%dir %{multiarch_includedir}/ptlib
%{multiarch_includedir}/ptlib/pluginmgr.h
%{_datadir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%files -n %{libname}-plugins
%defattr(-,root,root)
%dir %{_libdir}/%{name}-%{version}
%dir %{_libdir}/%{name}-%{version}/devices
%dir %{_libdir}/%{name}-%{version}/devices/sound
%dir %{_libdir}/%{name}-%{version}/devices/videoinput
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/alsa_pwplugin.so
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/oss_pwplugin.so
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/esd_pwplugin.so
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/pulse_pwplugin.so
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/videoinput/v4l2_pwplugin.so

%files -n %{libname}-plugins-dc
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/videoinput/dc_pwplugin.so

%files -n %{libname}-plugins-avc
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/%{name}-%{version}/devices/videoinput/avc_pwplugin.so
