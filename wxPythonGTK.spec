Summary:   Cross platform GUI toolkit for Python using wxGTK
Name:      wxPythonGTK
Version:   2.8.12.0
Release:   2
Epoch:     1
Source0:   http://prdownloads.sourceforge.net/wxpython/wxPython-src-%{version}.tar.bz2
# Fix a string literal error - AdamW 2008/12
Patch0:    wxPythonGTK/SOURCES/wxPython-2.8.9.1-literal.patch
Patch1:		wxPython-2.8.12.0-link.patch
Patch2:		wxPython-2.8.12.0-aui.patch
License:   LGPL/wxWindows Library Licence, Version 3
URL:       http://wxPython.org/
Group:     Development/Python
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: python-devel
BuildRequires: wxgtku2.8-devel >= 2.8.12
Provides: wxwin
Provides: wxPython  = %{version}
# old wxPython packages
Obsoletes: wxPython
Obsoletes: wxpython2.6 <= 2.6.3.3-4
Obsoletes: %{_lib}wxPythonGTK2.8 < %epoch:%{version}
Requires: %name-wxversion = %{EVRD}
 
%description
wxPython is a GUI toolkit for Python that is a wrapper around the
wxWindows C++ GUI library.  wxPython provides a large variety of
window types and controls, all implemented with a native look and feel
(and native runtime speed) on the platforms it is supported on.

This package is implemented using the GTK port of wxWindows.

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
Requires: %name = %{EVRD}

%description tools
wxPython is a GUI toolkit for Python that is a wrapper around the
wxWindows C++ GUI library.  wxPython provides a large variety of
window types and controls, all implemented with a native look and feel
(and native runtime speed) on the platforms it is supported on.

This contains the example applications that come with wxPython like
PyShell and XRCed.

%package devel
Summary: Development files of wxPythonGTK
Group: Development/Python
Provides: libwxPythonGTK-devel = %epoch:%version-%release
Requires: %{name} = %{EVRD}
Obsoletes: %{_lib}wxPythonGTK2.8-devel < %epoch:%{version}

%description devel
This packages contains the headers and etc. for building apps or
Python extension modules that use the same wxGTK shared libraries
that wxPython uses.

%prep
%setup -qn wxPython-src-%{version}/wxPython
%patch0 -p2 -b .literal
%patch1 -p1 -b .link
%patch2 -p2 -b .aui

%build
python setup.py \
	WXPORT='gtk2'\
	UNICODE=1 \
	EP_ADD_OPTS=1 \
	NO_SCRIPTS=1 \
	build

%install
rm -rf %buildroot %name.lang
python setup.py \
	WXPORT='gtk2'\
	UNICODE=1 \
	EP_ADD_OPTS=1 \
	NO_SCRIPTS=1 \
	install \
	--root=$RPM_BUILD_ROOT

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
Categories=GNOME;GTK;Development;
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
Categories=GNOME;GTK;Development;
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
Categories=GNOME;GTK;Development;
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
Categories=GNOME;GTK;Development;
EOF

#gw fix paths
%if %_lib != lib
mv %buildroot%py_puresitedir/* %buildroot%py_platsitedir
%endif

mkdir -p %buildroot%_miconsdir
install -m 644 wx/py/PyCrust_16.png $RPM_BUILD_ROOT%_miconsdir/PyCrust.png
install -m 644 wx/py/PyCrust_32.png $RPM_BUILD_ROOT%_iconsdir/PyCrust.png
install -m 644 wx/tools/XRCed/XRCed_16.png $RPM_BUILD_ROOT%{_miconsdir}/XRCed.png
install -m 644 wx/tools/XRCed/XRCed_32.png $RPM_BUILD_ROOT%{_iconsdir}/XRCed.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ../docs/*.txt
%doc docs/*
%py_platsitedir/wx.pth
%py_platsitedir/wx*-*

%files tools
%defattr(-,root,root)
%_datadir/applications/mandriva-*
%_iconsdir/*.png
%_miconsdir/*.png

%files wxversion
%defattr(-,root,root)
%py_platsitedir/wxversion*

%files devel
%defattr(-,root,root)
%{_includedir}/wx-2.8/wx/wxPython
