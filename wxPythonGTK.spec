%define pref 	%{_prefix}
%define python 	%{_bindir}/python
%define pythonver 	2.3
%define debug 	0
%define port  	GTK
%define lcport 	gtk2u
%define tarname wxPython-src
%define version 2.8.12.0
%define ver2    2.8
%define release %mkrel 2
%define wxpref  %{pref}/lib/wxPython

# Should --enable-debug_flag be used in release builds?
%define debug_flag 0
%define name      wxPython%{port}
%define major %ver2
%define libname %mklibname %{name} %{major}

%define wxconfigname %{wxpref}/lib/wx/config/gtk2-unicode-release-%ver2

%{?!py_puresitedir:%define py_puresitedir %_libdir/python%pyver/site-packages}
#----------------------------------------------------------------
Summary:   Cross platform GUI toolkit for Python using wx%{port}
Name:      %{name}
Version:   %{version}
Release:   %{release}
Epoch:1
Source0:   http://prdownloads.sourceforge.net/wxpython/%{tarname}-%{version}.tar.bz2
# Fix a string literal error - AdamW 2008/12
Patch0:    wxPythonGTK/SOURCES/wxPython-2.8.9.1-literal.patch

License:   LGPL/wxWindows Library Licence, Version 3
URL:       http://wxPython.org/
Group:     Development/Python
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: libmesaglu-devel
BuildRequires: libpython-devel >= %pythonver
BuildRequires: gtk2-devel
BuildRequires: SDL-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libgnomeprintui-devel
BuildRequires: expat-devel

Provides: wxwin
Provides: wxPython  = %{version}
# old wxPython packages
Obsoletes: wxPython
Obsoletes: wxpython2.6 <= 2.6.3.3-4
Requires: %libname = %epoch:%version-%release
Requires: %name-wxversion = %epoch:%version-%release
%define _requires_exceptions libwx_gtk2u_gizmos-%{ver2}\\|libwx_gtk2u_gizmos_xrc-%{ver2}\\|libwx_gtk2u_stc-%{ver2}.so\\|libwx_gtk2u_gl-%{ver2}.so
%define _provides_exceptions libwx_gtk2u_gizmos-%{ver2}\\|libwx_gtk2u_gizmos_xrc-%{ver2}\\|libwx_gtk2u_stc-%{ver2}.so\\|libwx_gtk2u_gl-%{ver2}.so
 
%description
wxPython is a GUI toolkit for Python that is a wrapper around the
wxWindows C++ GUI library.  wxPython provides a large variety of
window types and controls, all implemented with a native look and feel
(and native runtime speed) on the platforms it is supported on.

This package is implemented using the %{port} port of wxWindows.

%package wxversion
Summary: Select a specific version of wxPython
Group: Development/Python
Conflicts: wxPythonGTK < 1:2.8.3.0-2

%description wxversion
wxPython is a GUI toolkit for Python that is a wrapper around the
wxWindows C++ GUI library.  wxPython provides a large variety of
window types and controls, all implemented with a native look and feel
(and native runtime speed) on the platforms it is supported on.

This package contains the wxversion python module needed if several versions of
wxPython are installed.

%package tools
Summary: Example applications from wxPythonGTK
Group: Development/Python
Requires: %name = %epoch:%version-%release

%description tools
wxPython is a GUI toolkit for Python that is a wrapper around the
wxWindows C++ GUI library.  wxPython provides a large variety of
window types and controls, all implemented with a native look and feel
(and native runtime speed) on the platforms it is supported on.

This contains the example applications that come with wxPython like
PyShell and XRCed.

%package -n %libname
Summary: Shared library of wxGTK for wxPythonGTK
Group: System/Libraries

%description -n %libname
This is the internal version of the wxGTK shared library included 
in wxPythonGTK.

%package -n %libname-devel
Summary: Development files of wxPython%{port}
Group: Development/Python
Provides: libwxPythonGTK-devel = %epoch:%version-%release
Requires: wxPython%{port} = %epoch:%{version}-%release
Requires: %libname = %epoch:%{version}-%release

%description -n %libname-devel
This packages contains the headers and etc. for building apps or
Python extension modules that use the same wx%{port} shared libraries
that wxPython uses.

%prep
%setup -q -n %{tarname}-%{version}
%patch0 -p1 -b .literal

mkdir bld

%build
WXDIR=`pwd`

# Configure and build wxWidgets
cd bld
# Configure, trying to reduce dependencies
../configure --with-%{lcport} \
	--prefix=%{wxpref} \
	--enable-monolithic \
	--disable-rpath \
	--with-opengl \
	--enable-geometry \
	--enable-optimise \
	--enable-sound 	--with-sdl \
	--enable-display \
%if %{debug}
	--enable-debug \
%else
	--enable-optimise \
%if %{debug_flag}
	--enable-debug_flag \
%endif
%endif
	--with-libjpeg=sys \
	--with-libpng=sys \
	--with-libtiff=sys \
	--with-zlib=sys \
	--with-expat=sys \
        --enable-gtk2 \
        --enable-unicode \
	--enable-exceptions \
	--enable-catch_segvs \
	--enable-graphics_ctx
##	--enable-debug_flag \
##	--with-odbc \


# Build wxWindows
make
#%make -C contrib/src/animate 
%make -C contrib/src/gizmos 
%make -C contrib/src/stc


cd ../locale
make allmo

# Now build wxPython
cd $WXDIR/wxPython
%{python} setup.py \
	WXPORT='gtk2'\
	UNICODE=1 \
	EP_ADD_OPTS=1 \
	NO_SCRIPTS=1 \
	WX_CONFIG="$WXDIR/bld/wx-config --no_rpath" \
       	build_ext --rpath=%{wxpref}/lib \
	build

%install
rm -rf %buildroot %name.lang
WXDIR=`pwd`

# Install wxGTK and contribs
cd bld
make prefix=$RPM_BUILD_ROOT%{wxpref} install
#make -C contrib/src/animate prefix=$RPM_BUILD_ROOT%{wxpref} install
make -C contrib/src/gizmos prefix=$RPM_BUILD_ROOT%{wxpref} install
make -C contrib/src/stc prefix=$RPM_BUILD_ROOT%{wxpref} install

cd $WXDIR/wxPython
%{python} setup.py \
	WXPORT='gtk2'\
	UNICODE=1 \
	EP_ADD_OPTS=1 \
	NO_SCRIPTS=1 \
	WX_CONFIG="$RPM_BUILD_ROOT%{wxpref}/bin/wx-config --prefix=$RPM_BUILD_ROOT%{wxpref} --no_rpath" \
       	build_ext --rpath=%{wxpref}/lib \
	install \
	--root=$RPM_BUILD_ROOT

# Since I want this RPM to be as generic as possible I won't let
# distutils copy the scripts, since it will mangle the #! line
# to use the real python pathname.  Since some distros install
# python 2.2 as python2 and others as python, then I can't let
# it do that otherwise the dependencies will be fouled up.  Copy
# them manually instead:

mkdir -p $RPM_BUILD_ROOT%{_bindir}
for s in \
	helpviewer \
	img2png \
	img2py \
	img2xpm \
	pyalacarte \
	pyalamode \
	pycrust \
	pywrap \
	pyshell \
	pywxrc \
	xrced; do
    cp scripts/$s $RPM_BUILD_ROOT%{_bindir}
done

cd ..
for subdir in %buildroot%{wxpref}/share/locale/*;do
echo "%lang($(basename $subdir)) $(echo $subdir|sed s!%buildroot!!)" >> %name.lang
done

#gw fix wx-config symlink
ln -sf %{wxconfigname} %buildroot%wxpref/bin/wx-config

#gw hmm, let's remove this:
rm -rf %buildroot/include

#menu
# install Mandriva menu items

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-pyshell.desktop << EOF
[Desktop Entry]
Name=PyShell
Comment=GUI Python Shell
Exec=%{_bindir}/pyshell %U
Icon=PyCrust
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Development;X-MandrivaLinux-Development-Tools;
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-pycrust.desktop << EOF
[Desktop Entry]
Name=PyCrust
Comment=GUI Python Shell with Filling
Exec=%{_bindir}/pycrust %U
Icon=PyCrust
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Development;X-MandrivaLinux-Development-Tools;
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-pyalamode.desktop << EOF
[Desktop Entry]
Name=PyAlaMode
Comment=GUI Python Shell with Filling and Editor Windows
Exec=%{_bindir}/pyalamode %U
Icon=PyCrust
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Development;X-MandrivaLinux-Development-Tools;
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-xrced.desktop << EOF
[Desktop Entry]
Name=XRCed
Comment=XRC resource editor for wxPython
Exec=%{_bindir}/xrced %U
Icon=XRCed
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Development;X-MandrivaLinux-Development-Tools;
EOF



#icons
cd wxPython
mkdir -p %buildroot%_miconsdir
install -m 644 wx/py/PyCrust_16.png $RPM_BUILD_ROOT%_miconsdir/PyCrust.png
install -m 644 wx/py/PyCrust_32.png $RPM_BUILD_ROOT%_iconsdir/PyCrust.png
install -m 644 wx/tools/XRCed/XRCed_16.png $RPM_BUILD_ROOT%{_miconsdir}/XRCed.png
install -m 644 wx/tools/XRCed/XRCed_32.png $RPM_BUILD_ROOT%{_iconsdir}/XRCed.png

#gw fix paths
%if %_lib != lib
mv %buildroot%py_puresitedir/* %buildroot%py_platsitedir
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post tools
%update_menus
%endif
%if %mdkversion < 200900
%postun tools
%clean_menus
%endif

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif


%files -f %name.lang
%defattr(-,root,root)
%doc docs/preamble.txt
%doc docs/licence.txt
%doc docs/readme.txt
%doc docs/changes.txt
%doc wxPython/docs/*.*
%doc wxPython/docs/screenshots
%py_platsitedir/wx.pth
%py_platsitedir/wx*-*
%dir %{wxpref}
%dir %{wxpref}/share/
%dir %{wxpref}/share/locale
%{wxpref}/share/bakefile

%files tools
%defattr(-,root,root)
%{pref}/bin/*
%_datadir/applications/mandriva-*
%_iconsdir/*.png
%_miconsdir/*.png

%files wxversion
%defattr(-,root,root)
%py_platsitedir/wxversion*

%files -n %libname
%defattr(-,root,root)
%dir %{wxpref}/lib
%{wxpref}/lib/libwx*.so.*


%files -n %libname-devel
%defattr(-,root,root)
%dir %{wxpref}/include/
%{wxpref}/include/wx-%ver2/
%{wxpref}/lib/*.so
%{wxpref}/lib/wx
%dir %{wxpref}/share/aclocal
%{wxpref}/share/aclocal/wxwin.m4
%dir %{wxpref}/bin
%{wxpref}/bin/wx-config
%{wxpref}/bin/wxrc*
