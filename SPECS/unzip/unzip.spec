Summary:	Unzip-6.0
Name:		unzip
Version:	6.0
Release:	5%{?dist}
License:	BSD
URL:		http://www.gnu.org/software/%{name}
Source0:	http://downloads.sourceforge.net/infozip/unzip60.tar.gz
%define sha1 unzip=abf7de8a4018a983590ed6f5cbd990d4740f8a22
Group:		System Environment/Utilities
Vendor:		VMware, Inc.
Distribution: Photon

Patch0: cve-2014-9636.patch

%description
The UnZip package contains ZIP extraction utilities. These are useful 
for extracting files from ZIP archives. ZIP archives are created 
with PKZIP or Info-ZIP utilities, primarily in a DOS environment.

%prep
%setup -qn unzip60
%patch0 -p1

%build
case `uname -m` in
  i?86)
    sed -i -e 's/DASM_CRC"/DASM_CRC -DNO_LCHMOD"/' unix/Makefile
    make -f unix/Makefile linux %{?_smp_mflags}
    ;;
  *)
    sed -i -e 's/CFLAGS="-O -Wall/& -DNO_LCHMOD/' unix/Makefile
    make -f unix/Makefile linux_noasm %{?_smp_mflags}
    ;;
esac

%install
install -v -m755 -d %{buildroot}%{_bindir}
make DESTDIR=%{buildroot} prefix=%{_prefix} install
cp %{_builddir}/unzip60/funzip %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unzip %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unzipsfx %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unix/zipgrep %{buildroot}%{_bindir}
ln -sf unzip %{buildroot}%{_bindir}/zipinfo

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0-5
-	GA - Bump release of all rpms
*	Tue May 10 2016 Nick Shi <nshi@vmware.com> 6.0-4
-	Added unzipsfx, zipgrep and zipinfo to unzip rpm
*	Sat Aug 15 2015 Sharath George <sharathg@vmware.com> 6.0-3
-	Added patch for CVE-2014-9636
*	Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 6.0-2
-	Updated group.
*	Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 6.0-1
-	Initial build. First version
