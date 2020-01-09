Name:           dlm
Version:        4.0.2
Release:        3%{?dist}
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

Patch0: 0001-dlm_stonith-add-man-page.patch
Patch1: 0002-dlm_stonith-install-man-page.patch
Patch2: 0003-libdlm-udev-dir-now-under-usr-lib.patch

%if 0%{?rhel}
ExclusiveArch: i686 x86_64
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

%patch0 -p1 -b .0001-dlm_stonith-add-man-page.patch
%patch1 -p1 -b .0002-dlm_stonith-install-man-page.patch
%patch2 -p1 -b .0003-libdlm-udev-dir-now-under-usr-lib.patch

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
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.0.2-3
- Mass rebuild 2013-12-27

* Thu Aug 01 2013 David Teigland <teigland@redhat.com> - 4.0.2-2
- Add dlm_stonith man page, move udev file from /lib to /usr/lib

* Wed Jul 31 2013 David Teigland <teigland@redhat.com> - 4.0.2-1
- New upstream release

