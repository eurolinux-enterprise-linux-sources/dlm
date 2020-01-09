Name:           dlm
Version:        4.0.6
Release:        1%{?dist}
License:        GPLv2 and GPLv2+ and LGPLv2+
# For a breakdown of the licensing, see README.license
Group:          System Environment/Kernel
Summary:        dlm control daemon and tool
URL:            https://fedorahosted.org/cluster
BuildRequires:  glibc-kernheaders
BuildRequires:  corosynclib-devel >= 1.99.9
BuildRequires:  pacemaker-libs-devel >= 1.1.7
BuildRequires:  libxml2-devel
BuildRequires:  systemd-units
BuildRequires:  systemd-devel
Source0:        http://git.fedorahosted.org/cgit/dlm.git/snapshot/%{name}-%{version}.tar.gz

# Patch0: 0001-foo.patch

%if 0%{?rhel}
ExclusiveArch: i686 x86_64 s390x
%endif

Requires:       %{name}-lib = %{version}-%{release}
Requires:       corosync >= 1.99.9
%{?fedora:Requires: kernel-modules-extra}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Conflicts: cman

%description
The kernel dlm requires a user daemon to control membership.

%prep
%setup -q

# %patch0 -p1 -b .0001-foo.patch

%build
# upstream does not require configure
# upstream does not support _smp_mflags
CFLAGS=$RPM_OPT_FLAGS make
CFLAGS=$RPM_OPT_FLAGS make -C fence

%install
rm -rf $RPM_BUILD_ROOT
make install LIBDIR=%{_libdir} DESTDIR=$RPM_BUILD_ROOT
make -C fence install LIBDIR=%{_libdir} DESTDIR=$RPM_BUILD_ROOT

install -Dm 0644 init/dlm.service %{buildroot}%{_unitdir}/dlm.service
install -Dm 0644 init/dlm.sysconfig %{buildroot}/etc/sysconfig/dlm

%post
%systemd_post dlm.service

%preun
%systemd_preun dlm.service

%postun
%systemd_postun_with_restart dlm.service

%files
%defattr(-,root,root,-)
%doc README.license
%{_unitdir}/dlm.service
%{_sbindir}/dlm_controld
%{_sbindir}/dlm_tool
%{_sbindir}/dlm_stonith
%{_mandir}/man8/dlm*
%{_mandir}/man5/dlm*
%{_mandir}/man3/*dlm*
%config(noreplace) %{_sysconfdir}/sysconfig/dlm

%package        lib
Summary:        Library for %{name}
Group:          System Environment/Libraries
Conflicts:      clusterlib

%description    lib
The %{name}-lib package contains the libraries needed to use the dlm
from userland applications.

%post lib -p /sbin/ldconfig

%postun lib -p /sbin/ldconfig

%files          lib
%defattr(-,root,root,-)
/usr/lib/udev/rules.d/*-dlm.rules
%{_libdir}/libdlm*.so.*

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-lib = %{version}-%{release}
Conflicts:      clusterlib-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files          devel
%defattr(-,root,root,-)
%{_libdir}/libdlm*.so
%{_includedir}/libdlm*.h
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Jun 10 2016 David Teigland <teigland@redhat.com> - 4.0.6-1
- New upstream release

* Tue Apr 26 2016 David Teigland <teigland@redhat.com> - 4.0.5-1
- New upstream release

* Mon Feb 29 2016 David Teigland <teigland@redhat.com> - 4.0.4-1
- New upstream release

* Mon Jul 06 2015 David Teigland <teigland@redhat.com> - 4.0.2-6
- dlm_controld: don't log error from cpg_dispatch

* Mon Nov 17 2014 David Teigland <teigland@redhat.com> - 4.0.2-5
- dlm_tool: fix status printing in libdlmcontrol 

* Fri Sep 12 2014 David Teigland <teigland@redhat.com> - 4.0.2-4
- Enable s390x, fix non-zeroed addrs

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.0.2-3
- Mass rebuild 2013-12-27

* Thu Aug 01 2013 David Teigland <teigland@redhat.com> - 4.0.2-2
- Add dlm_stonith man page, move udev file from /lib to /usr/lib

* Wed Jul 31 2013 David Teigland <teigland@redhat.com> - 4.0.2-1
- New upstream release

