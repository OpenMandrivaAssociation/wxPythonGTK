Summary:	Cross platform GUI toolkit for Python using wxGTK
Name:		wxPythonGTK
Version:	2.8.12.0
Release:	11
Epoch:		1
Group:		Development/Python
License:	LGPL/wxWindows Library Licence, Version 3
URL:		http://wxPython.org/
Source0:	http://prdownloads.sourceforge.net/wxpython/wxPython-src-%{version}.tar.bz2
# Fix a string literal error - AdamW 2008/12
Patch0:		wxPythonGTK/SOURCES/wxPython-2.8.9.1-literal.patch
Patch1:		wxPython-2.8.12.0-link.patch
Patch2:		wxPython-2.8.12.0-aui.patch
Patch3:		wxPython-2.8.12-Bind-disconnect-event-handler.patch
BuildRequires:	python-devel
BuildRequires:	wxgtku2.8-devel >= 2.8.12
BuildRequires:	pkgconfig(glu)
Provides:	wxwin = %{version}
Provides:	wxPython = %{version}
Requires:	%{name}-wxversion = %{EVRD}
 
%description
wxPython is a GUI toolkit for Python that is a wrapper around the
wxWindows C++ GUI library.  wxPython provides a large variety of
window types and controls, all implemented with a native look and feel
(and native runtime speed) on the platforms it is supported on.

This package is implemented using the GTK port of wxWindows.

%package wxversion
Summary:	Select a specific version of wxPython
Group:		Development/Python
Conflicts:	wxPythonGTK < 1:2.8.3.0-2

%description wxversion
wxPython is a GUI toolkit for Python that is a wrapper around the
wxWindows C++ GUI library.  wxPython provides a large variety of
window types and controls, all implemented with a native look and feel
(and native runtime speed) on the platforms it is supported on.

This package contains the wxversion python module needed if several versions of
wxPython are installed.

%package tools
Summary:	Example applications from wxPythonGTK
Group:		Development/Python
Requires:	%{name} = %{EVRD}

%description tools
wxPython is a GUI toolkit for Python that is a wrapper around the
wxWindows C++ GUI library.  wxPython provides a large variety of
window types and controls, all implemented with a native look and feel
(and native runtime speed) on the platforms it is supported on.

This contains the example applications that come with wxPython like
PyShell and XRCed.

%package devel
Summary:	Development files of wxPythonGTK
Group:		Development/Python
Provides:	libwxPythonGTK-devel = %epoch:%version-%release
Requires:	%{name} = %{EVRD}

%description devel
This packages contains the headers and etc. for building apps or
Python extension modules that use the same wxGTK shared libraries
that wxPython uses.

%prep
%setup -qn wxPython-src-%{version}/wxPython
%patch0 -p2 -b .literal
%patch1 -p1 -b .link
%patch2 -p2 -b .aui
%patch3 -p2

%build
python setup.py \
	WXPORT='gtk2'\
	UNICODE=1 \
	EP_ADD_OPTS=0 \
	NO_SCRIPTS=1 \
	build

%install
python setup.py \
	WXPORT='gtk2'\
	UNICODE=1 \
	EP_ADD_OPTS=1 \
	NO_SCRIPTS=0 \
	install \
	--root=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-pyshell.desktop << EOF
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
cat > %{buildroot}%{_datadir}/applications/mandriva-pycrust.desktop << EOF
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
cat > %{buildroot}%{_datadir}/applications/mandriva-pyalamode.desktop << EOF
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
cat > %{buildroot}%{_datadir}/applications/mandriva-xrced.desktop << EOF
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
%if %{_lib} != lib
mv %{buildroot}%{py_puresitedir}/* %{buildroot}%{py_platsitedir}
%endif

mkdir -p %{buildroot}%{_miconsdir}
install -m 644 wx/py/PyCrust_16.png %{buildroot}%{_miconsdir}/PyCrust.png
install -m 644 wx/py/PyCrust_32.png %{buildroot}%{_iconsdir}/PyCrust.png
install -m 644 wx/tools/XRCed/XRCed_16.png %{buildroot}%{_miconsdir}/XRCed.png
install -m 644 wx/tools/XRCed/XRCed_32.png %{buildroot}%{_iconsdir}/XRCed.png

#(proyvind): We remove eggs for older python versions as we don't need them
#	     and to prevent dependencies to be generated against older python.
#            Should we carry eggs shipped from upstream at all though..?
find %{buildroot} -name \*.egg|grep -F -v py%{py_ver}.egg| xargs rm -f

%files
%doc ../docs/*.txt
%doc docs/*
%{py_platsitedir}/wx.pth
%{py_platsitedir}/wx*-*

%files tools
%{_bindir}/*
%{_datadir}/applications/mandriva-*
%{_iconsdir}/*.png
%{_miconsdir}/*.png

%files wxversion
%{py_platsitedir}/wxversion*

%files devel
%{_includedir}/wx-2.8/wx/wxPython


%changelog
* Thu Jun 23 2011 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 1:2.8.12.0-5
+ Revision: 686806
- don't ship eggs for other python versions (prevents python(abi) deps to be
  generated on those other versions)

* Tue Jun 21 2011 Funda Wang <fwang@mandriva.org> 1:2.8.12.0-4
+ Revision: 686470
- install binary

* Tue May 17 2011 Paulo Andrade <pcpa@mandriva.com.br> 1:2.8.12.0-3
+ Revision: 675929
- Correct assertion to allow handler as None, as it is a valid argument.

* Sat May 07 2011 Funda Wang <fwang@mandriva.org> 1:2.8.12.0-2
+ Revision: 672197
- add fedora patch to fix aui loading
- fix linkage
- build with system wxgtk

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

  + Lev Givon <lev@mandriva.org>
    - Update to 2.8.12.0.

* Sun Oct 31 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1:2.8.11.0-2mdv2011.0
+ Revision: 590914
- rebuild for python-2.7

* Mon Sep 13 2010 Lev Givon <lev@mandriva.org> 1:2.8.11.0-1mdv2011.0
+ Revision: 578036
- Update to 2.8.11.0.
  Remove patches that were merged upstream.

* Thu Apr 29 2010 Paulo Andrade <pcpa@mandriva.com.br> 1:2.8.10.1-4mdv2010.1
+ Revision: 541038
- Correct 64 bits crash in wx cairo interface

* Wed Mar 03 2010 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.10.1-3mdv2010.1
+ Revision: 513778
- build with system expat (bug #57960)

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.8.10.1-2mdv2010.1
+ Revision: 488811
- rebuilt against libjpeg v8

* Mon Dec 14 2009 Lev Givon <lev@mandriva.org> 1:2.8.10.1-1mdv2010.1
+ Revision: 478645
- Update to 2.8.10.1.

* Sat Oct 03 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.9.2-3mdv2010.0
+ Revision: 453180
- enable graphicx_ctx (bug #54129)

* Sun Aug 16 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.8.9.2-2mdv2010.0
+ Revision: 416902
- adapt the fedora patches from wxgtk2.8

* Thu Feb 19 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.9.2-1mdv2009.1
+ Revision: 342816
- new version
- update file list

* Tue Jan 27 2009 Funda Wang <fwang@mandriva.org> 1:2.8.9.1-6mdv2009.1
+ Revision: 334021
- add gl

* Tue Jan 27 2009 Funda Wang <fwang@mandriva.org> 1:2.8.9.1-5mdv2009.1
+ Revision: 334020
- spcify exception one by one

* Sun Dec 28 2008 Adam Williamson <awilliamson@mandriva.org> 1:2.8.9.1-4mdv2009.1
+ Revision: 320093
- bunch more string literal fixes
- another string literal fix
- add literal.patch: fix a string literal error
- obsolete wxpython2.6

  + Funda Wang <fwang@mandriva.org>
    - rebuild for new python

* Tue Oct 14 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.9.1-2mdv2009.1
+ Revision: 293665
- rebuild

* Sat Oct 11 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.9.1-1mdv2009.1
+ Revision: 292359
- new version

* Mon Jul 21 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.8.1-1mdv2009.0
+ Revision: 239366
- new version

* Thu Jun 26 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.8.0-1mdv2009.0
+ Revision: 229258
- fix buildrequires
- new version

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Apr 15 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.7.1-4mdv2009.0
+ Revision: 193697
- fix deps

* Wed Apr 09 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.7.1-3mdv2009.0
+ Revision: 192490
- split example programs to the tools package

* Fri Feb 08 2008 Thierry Vignaud <tv@mandriva.org> 1:2.8.7.1-2mdv2008.1
+ Revision: 163971
- drop old menu
- fix mesaglu-devel BR
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Dec 01 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.7.1-1mdv2008.1
+ Revision: 114276
- new version

* Mon Oct 29 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.6.1-1mdv2008.1
+ Revision: 102943
- new version

  + Thierry Vignaud <tv@mandriva.org>
    - kill hardcoded icon extension
    - s/Mandrake/Mandriva/

* Wed Sep 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.4.2-2mdv2008.0
+ Revision: 84620
- fix deps and provides (bug #33480)

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Thu Aug 09 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.4.2-1mdv2008.0
+ Revision: 60703
- new version
- drop the patch

* Tue Jul 10 2007 Anssi Hannula <anssi@mandriva.org> 1:2.8.4.0-3mdv2008.0
+ Revision: 51030
- add conflicts with old wxPythonGTK to ensure smooth upgrade

* Wed Jun 27 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.4.0-2mdv2008.0
+ Revision: 44891
- fix for new gslice

* Wed May 16 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.4.0-1mdv2008.0
+ Revision: 27164
- new version

* Thu May 10 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.3.0-2mdv2008.0
+ Revision: 25902
- split out wxversion

* Wed Apr 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:2.8.3.0-1mdv2008.0
+ Revision: 14733
- new version
- drop animate extension


* Thu Nov 30 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.3.3-1mdv2007.0
+ Revision: 88876
- back to wxpython 2.6, as required by bittorrent

* Tue Nov 28 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.7.2.0-2mdv2007.1
+ Revision: 88096
- add new files
- new version
- drop animate extension
- Import wxPythonGTK

* Wed Oct 04 2006 Götz Waschk <waschk@mandriva.org> 2.6.3.3-3mdv2007.0
- fix python path on lib64 architecture (bug #23427)

* Thu Jul 20 2006 Jerome Martin <jmartin@mandriva.org> 2.6.3.3-2mdv2007.0
- Fix BuildRequires for backport

* Mon Jul 17 2006 Götz Waschk <waschk@mandriva.org> 2.6.3.3-1mdv2007.0
- update file list
- New release 2.6.3.3

* Thu Jun 22 2006 Götz Waschk <waschk@mandriva.org> 2.6.3.2-4mdv2007.0
- fix deps of the devel package
- xdg menu

* Mon Jun 19 2006 Stefan van der Eijk <stefan@eijk.nu> 2.6.3.2-1mdv2007.0
- rebuild for png

* Sun Jun 18 2006 Götz Waschk <waschk@mandriva.org> 2.6.3.2-2mdv2007.0
- fix buildrequires

* Thu Apr 06 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.3.2-1mdk
- New release 2.6.3.2

* Wed Mar 29 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.3.0-1mdk
- New release 2.6.3.0

* Mon Jan 23 2006 Götz Waschk <waschk@mandriva.org> 2.6.2.1-2mdk
- fix build with new python

* Wed Jan 11 2006 Götz Waschk <waschk@mandriva.org> 2.6.2.1-1mdk
- update file list
- New release 2.6.2.1
- use mkrel

* Mon Jun 06 2005 Götz Waschk <waschk@mandriva.org> 2.6.1.0-1mdk
- New release 2.6.1.0

* Wed Jun 01 2005 Götz Waschk <waschk@mandriva.org> 2.6.0.1-1mdk
- New release 2.6.0.1

* Thu Apr 28 2005 Götz Waschk <waschk@mandriva.org> 2.6.0.0-1mdk
- add menu entries
- drop the patch
- New release 2.6.0.0

* Sat Apr 23 2005 Götz Waschk <waschk@mandriva.org> 2.5.5.1-3mdk
- patch to support G_FILENAME_ENCODING=@locale

* Wed Apr 20 2005 Götz Waschk <waschk@mandriva.org> 2.5.5.1-2mdk
- switch to system versions of the graphics libraries
- fix build, using the official spec as a template

* Tue Apr 19 2005 Götz Waschk <waschk@linux-mandrake.com> 2.5.5.1-1mdk
- bump major
- New release 2.5.5.1
- drop the patch

* Wed Feb 23 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.5.3.1-3mdk
- Patch1: fix va_copy configure check

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 2.5.3.1-2mdk
- Rebuild for new python

* Wed Nov 10 2004 Götz Waschk <waschk@linux-mandrake.com> 2.5.3.1-1mdk
- new major
- update file list
- drop obsolete patch
- New release 2.5.3.1

* Wed Nov 03 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.2.7-3mdk
- fix build on x86_64

* Sat Sep 18 2004 Frederic Lepied <flepied@mandrakesoft.com> 2.5.2.7-2mdk
- activate --enable-exceptions and --enable-catch_segvs to be able to
continue when an exception occurs

* Mon Aug 16 2004 Götz Waschk <waschk@linux-mandrake.com> 2.5.2.7-1mdk
- major 2.5_2
- update file list
- fix source URL
- New release 2.5.2.7

* Tue Jun 15 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 2.5.1.5-2mdk
- Rebuild

* Tue Apr 06 2004 Götz Waschk <waschk@linux-mandrake.com> 2.5.1.5-1mdk
- also build contrib part of wxGTK
- new major
- fix build
- new version

* Tue Dec 02 2003 Götz Waschk <waschk@linux-mandrake.com> 2.4.2.4-2mdk
- rebuild for missing package

