%ifarch s390x
# https://bugzilla.redhat.com/show_bug.cgi?id=1861276 -> Disable LTO for now
%define _lto_cflags %{nil}
%endif

#global candidate RC0

Name:		tpm2-pkcs11
Version:	1.5.0
Release:	9%{?candidate:.%{candidate}}%{?dist}
Summary:	PKCS#11 interface for TPM 2.0 hardware

License:	BSD
URL:		https://github.com/tpm2-software/tpm2-pkcs11
Source0:	https://github.com/tpm2-software/%{name}/releases/download/%{version}%{?candidate:-%{candidate}}/%{name}-%{version}%{?candidate:-%{candidate}}.tar.gz
Source1:	https://github.com/tpm2-software/%{name}/releases/download/%{version}%{?candidate:-%{candidate}}/%{name}-%{version}%{?candidate:-%{candidate}}.tar.gz.asc
# William Roberts (Bill Roberts) key from pgp.mit.edu
Source2:	gpgkey-8E1F50C1.gpg
Patch0:         tpm2-pkcs11-gcc11.patch
# https://github.com/tpm2-software/tpm2-pkcs11/commit/78f4e2b47d02cb8215f252e77c68a81dfe4afa30
Patch1:         tpm2-pkcs11-s390x.patch
Patch2:         tpm2-pkcs11-1.5.0-openssl3.patch

BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	python3
BuildRequires:	libgcrypt-devel
BuildRequires:	libyaml-devel
BuildRequires:	openssl-devel
BuildRequires:	p11-kit-devel
BuildRequires:	sqlite-devel
BuildRequires:	tpm2-tools
BuildRequires:	tpm2-tss-devel
# for tests
BuildRequires:	libcmocka-devel
BuildRequires:	dbus-daemon
# for tools
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-pyasn1-modules
BuildRequires:	python3-pyyaml
BuildRequires:	python3-cryptography
# for tarball signature verification
BuildRequires:	gnupg2

%description
PKCS #11 is a Public-Key Cryptography Standard that defines a standard method
to access cryptographic services from tokens/ devices such as hardware security
modules (HSM), smart cards, etc. In this project we intend to use a TPM2 device
as the cryptographic token.

%package tools
Summary: The tools required to setup and configure TPM2 for PKCS#11
# Automatic generator does not work for me even though the requires.txt is in place
Requires:	python3-cryptography
Requires:	python3-pyyaml
Requires:	python3-pyasn1-modules

%description tools
The tools required to setup and configure TPM2 for PKCS#11.

%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -p1 -n %{name}-%{version}%{?candidate:-%{candidate}}


%build
%configure --enable-unit CFLAGS="%{optflags} -Wno-error=deprecated-declarations"
%{make_build}
cd tools
%py3_build


%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/tpm2-pkcs11.pc
[ -f $RPM_BUILD_ROOT%{_libdir}/pkcs11/libtpm2_pkcs11.la ] && \
  rm $RPM_BUILD_ROOT%{_libdir}/pkcs11/libtpm2_pkcs11.la
[ -f $RPM_BUILD_ROOT%{_libdir}/pkcs11/libtpm2_pkcs11.a ] && \
  rm $RPM_BUILD_ROOT%{_libdir}/pkcs11/libtpm2_pkcs11.a
cd tools
%py3_install
install -Dpm 755 tpm2_ptool $RPM_BUILD_ROOT%{_bindir}/tpm2_ptool


%check
make check
cd tools
%{__python3} setup.py test


%files
%license LICENSE
%{_datadir}/p11-kit/modules/tpm2_pkcs11.module
%%dir %{_libdir}/pkcs11
%{_libdir}/pkcs11/libtpm2_pkcs11.so
%{_libdir}/pkcs11/libtpm2_pkcs11.so.0*

%files tools
%{_bindir}/tpm2_ptool
%{python3_sitelib}/tpm2_pkcs11/*
%{python3_sitelib}/tpm2_pkcs11_tools-*/*


%changelog
* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 1.5.0-9
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Jul 02 2021 Jerry Snitselaar <jsnitsel@redhat.com> - 1.5.0-8
- Fix product version for gating
Resolves: rhbz#1972907

* Wed Jun 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.5.0-7
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Wed May 19 2021 Jerry Snitselaar <jsnitsel@redhat.com> - 1.5.0-6
- Work around for openssl 3.0 update. Related: rhbz#1958030

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.5.0-5
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Mon Feb 01 2021 Jakub Jelen <jjelen@redhat.com> - 1.5.0-4}
- Unbreak the build on s390x (#1923383)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 07 2020 Jeff Law <law@redhat.com> - 1.5.0-2
- Avoid stringop-overflow diagnostic in testsuite

* Wed Nov 18 2020 Jakub Jelen <jjelen@redhat.com> - 1.5.0-1
- New upstream release

* Tue Sep 15 2020 Jeff Law <law@redhat.com> - 1.4.0-2
- Fix two source over-reads detected by gcc-11

* Mon Aug 24 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Mon Aug 10 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Mon Jul 27 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Tue Jul 07 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Thu Jul 02 2020 Jakub Jelen <jjelen@redhat.com> - 1.3.0-0.1-RC0
- Update to 1.3.0-RC0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-2
- Rebuilt for Python 3.9

* Mon Mar 30 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Mon Mar 09 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Mon Mar  2 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.0-0.1-RC1
- Update to 1.1.0 RC1 candidate

* Mon Feb 10 2020 Jakub Jelen <jjelen@redhat.com> - 1.0.1-3
- Unbreak build with gcc10 (#1796383)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Jakub Jelen <jjelen@redhat.com> - 1.0.1-1
- New upstream release (#1784580)

* Tue Dec 31 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.0-1
- Update to 1.0 stable release

* Thu Dec 26 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.0-0.1-RC1
- Update to 1.0 RC1 candidate

* Fri Oct 11 2019 Jakub Jelen <jjelen@redhat.com> - 0-0.3.20191011git0b7ceff
- Update to current git version
- Fix missing requires (#1757179)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0-0.7.20190813git2f3058c
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 21 2019 Miro Hrončok <mhroncok@redhat.com> - 0-0.6.20190813git2f3058c
- Rebuilt for Python 3.8

* Tue Aug 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0-0.5.20190813git2f3058c
- Update to new git snapshot for better use of tss2-tools 4.0 features

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0-0.4.20190219git1e84553
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.3.20190219git1e84553
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 23 2019 Jakub Jelen <jjelen@redhat.com> - 0-0.2.20190219git1e84553
- Package missing python tool for TPM2 initialization
- Update to current version from github

* Tue Feb 19 2019 Jakub Jelen <jjelen@redhat.com> - 0-0.1.20190219git836d715
- Initial release for Fedora


