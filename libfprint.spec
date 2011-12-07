Name:           libfprint
Version:        0.1.0
Release:        19.pre2%{?dist}
Summary:        Tool kit for fingerprint scanner

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.reactivated.net/fprint/wiki/Main_Page 
Source0:        http://downloads.sourceforge.net/fprint/%{name}-0.1.0-pre2.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# http://thread.gmane.org/gmane.linux.fprint/1321
Patch1:		0001-Add-udev-rules-to-set-devices-to-autosuspend.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=472103
Patch2:		0001-Add-gdk-pixbuf-support.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=499732
Source1:	aes1610.c
Patch3:		libfprint-aes1610-driver.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=627316
Patch4:		0001-Port-OpenSSL-using-code-to-NSS.patch
ExcludeArch:    s390 s390x

BuildRequires:  libusb1-devel glib2-devel gtk2-devel nss-devel
BuildRequires:  doxygen autoconf automake libtool
Requires:       ConsoleKit

%description
libfprint offers support for consumer fingerprint reader devices.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-0.1.0-pre2
%patch1 -p1
%patch2 -p1
cp -a %{SOURCE1} libfprint/drivers
%patch3 -p1 -b .aes1610
%patch4 -p1 -b .nss

%build
autoreconf -f -i
%configure --disable-static 
make %{?_smp_mflags}
pushd doc
make docs
popd

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING INSTALL NEWS TODO THANKS AUTHORS README
%{_libdir}/*.so.*
%{_datadir}/hal/fdi/information/20thirdparty/10-fingerprint-reader-fprint.fdi
%{_sysconfdir}/udev/rules.d/60-fprint-autosuspend.rules

%files devel
%defattr(-,root,root,-)
%doc HACKING doc/html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Aug 25 2010 Bastien Nocera <bnocera@redhat.com> 0.1.0-19.pre2
- Build against NSS, not OpenSSL
Resolves: rhbz#627316

* Thu Jul 29 2010 Matthew Garrett <mjg@redhat.com> 0.1.0-18.pre2
- Fix the udev rule generation properly
Resolves: rhbz#573019

* Tue Jun 30 2010 Matthew Garrett <mjg@redhat.com> 0.1.0-16.pre3
- Fix udev rules generation to avoid error on boot
Resolves: rhbz#573019

* Mon Jun 21 2010 Bastien Nocera <bnocera@redhat.com> 0.1.0-16.pre2
- Fix aes1610 patch to apply
Resolves: rhbz#605072

* Tue Jun 01 2010 Bastien Nocera <bnocera@redhat.com> 0.1.0-15.pre2
- Add README to package
Related: rhbz#595769

* Thu Jan 07 2010 Bastien Nocera <bnocera@redhat.com> 0.1.0-14.pre2
- Rebuild for new OpenSSL
Related: rhbz#543948

* Mon Nov 30 2009 Bastien Nocera <bnocera@redhat.com> 0.1.0-13.pre2
- Add aes1610 driver (#499732)

* Thu Oct 01 2009 Bastien Nocera <bnocera@redhat.com> 0.1.0-12.pre2
- Update udev autosuspend rules and disable SGS Thomson reader

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.1.0-11.pre2
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-10.pre2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Bastien Nocera <bnocera@redhat.com> 0.1.0-9.pre2
- Use gdk-pixbuf for image manipulation instead of ImageMagick (#472103)

* Sat Jun 20 2009 Bastien Nocera <bnocera@redhat.com> 0.1.0-8.pre2
- Update to 0.1.0-pre2

* Tue Jun 09 2009 Matthew Garrett <mjg@redhat.com> 0.1.0-7.pre1
- fprint-add-udev-rules.patch - build udev rules for autosuspend
- move hal fdi into the main package rather than -devel
- add autoreconf as a build depend while carrying the udev diff

* Tue Apr 21 2009 Karsten Hopp <karsten@redhat.com> 0.1.0-6.pre1.1
- Excludearch s390 s390x, we don't have USB devices there and this package
  doesn't build without USB support

* Mon Mar 09 2009 pingou <pingou@pingoured.fr> - 0.1.0-6.pre1
- Rebuilt for rawhide

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-5.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.1.0-4.pre1
- rebuild with new openssl

* Tue Nov 25 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1.0-3.pre1
- Fix possible crasher in libfprint when setting up the fds for polling

* Mon Nov 24 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1.0-2.pre1
- And add some API docs

* Tue Nov 18 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1.0-1.pre1
- Fix build

* Tue Nov 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1.0-0.pre1
- Update to 0.1.0-pre1

* Tue May 13 2008  Pingou <pingoufc4@yahoo.fr> 0.0.5-6
- Correction on the Build Requires

* Tue May 13 2008  Pingou <pingoufc4@yahoo.fr> 0.0.5-5
- Correction on the Build Requires

* Tue May 13 2008  Pingou <pingoufc4@yahoo.fr> 0.0.5-4
- Update the Build Requires due to the change on ImageMagick

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.0.5-3
- Autorebuild for GCC 4.3

* Sat Jan 05 2008 Pingou <pingoufc4@yahoo.fr> 0.0.5-2
- Change on the BuildRequires

* Sat Jan 05 2008 Pingou <pingoufc4@yahoo.fr> 0.0.5-1
- Update to version 0.0.5

* Sat Dec 01 2007 Pingou <pingoufc4@yahoo.fr> 0.0.4-3
- Changes on the Requires

* Sun Nov 25 2007 Pingou <pingoufc4@yahoo.fr> 0.0.4-2
- Changes on the Requires

* Sat Nov 24 2007 Pingou <pingoufc4@yahoo.fr> 0.0.4-1
- First release
