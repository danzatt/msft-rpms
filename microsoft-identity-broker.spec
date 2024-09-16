Name: microsoft-identity-broker
Version: 2.0.1
Release: 1
Summary: Installer for the broker service

License: Proprietary
URL: https://www.microsoft.com

%global msft_version %{version_no_tilde}
%global msft_release 1
Source0: https://packages.microsoft.com/rhel/9/prod/Packages/m/microsoft-identity-broker-%{msft_version}-%{msft_release}.x86_64.rpm
Source1: lsb-release-ubuntu-22.04
Source2: os-release-ubuntu-22.04
Source3: wrapper-identity-broker

BuildRequires: systemd-rpm-macros
%{?sysusers_requires_compat}
Requires: (microsoft-edge-beta or microsoft-edge-dev or microsoft-edge-stable)
Requires: java-headless
Requires: javapackages-filesystem
Requires: javapackages-tools

%define _opt_prefix /opt/microsoft/identity-broker/
%define _opt_bindir %{_opt_prefix}/bin
%define _opt_javadir %{_opt_prefix}/lib

%description
Installer for the broker service

%prep
rpm2cpio %{SOURCE0} | cpio -idmv > /dev/null 2>&1

%install

install -D -m 0755 %{SOURCE3} %{buildroot}/%{_bindir}/microsoft-identity-broker
install -D -m 0755 %{SOURCE3} %{buildroot}/%{_bindir}/microsoft-identity-device-broker

install -D -m 0755 %{_builddir}/opt/microsoft/identity-broker/bin/microsoft-identity-broker %{buildroot}/%{_opt_bindir}/microsoft-identity-broker
install -D -m 0755 %{_builddir}/opt/microsoft/identity-broker/bin/microsoft-identity-device-broker %{buildroot}/%{_opt_bindir}/microsoft-identity-device-broker

install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/lsb-release
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/os-release

install -D %{_builddir}/usr/share/doc/microsoft-identity-broker/LICENSE %{buildroot}/%{_docdir}/%{name}/LICENSE

mkdir -p "%{buildroot}/%{_fontdir}"
cp -r %{_builddir}/usr/share/fonts/. %{buildroot}/%{_fontdir}

mkdir -p "%{buildroot}/%{_opt_javadir}"
cp -r %{_builddir}/opt/microsoft/identity-broker/lib/. %{buildroot}/%{_opt_javadir}

# systemd/dbus services
sed -i -r "s:^Exec(Start)?=.*/([^/]+):Exec\1=%{_bindir}/\2:" \
	%{_builddir}/usr/lib/systemd/*/*.service %{_builddir}/usr/share/dbus-1/*/*.service

install -D -m 0644 %{_builddir}/usr/lib/systemd/system/microsoft-identity-device-broker.service %{buildroot}/%{_unitdir}/microsoft-identity-device-broker.service
install -D -m 0644 %{_builddir}/usr/lib/systemd/user/microsoft-identity-broker.service %{buildroot}/%{_userunitdir}/microsoft-identity-broker.service

install -D -m 0644 %{_builddir}/usr/share/dbus-1/services/com.microsoft.identity.broker1.service %{buildroot}/%{_datadir}/dbus-1/services/com.microsoft.identity.broker1.service
install -D -m 0644 %{_builddir}/usr/share/dbus-1/system.d/com.microsoft.identity.devicebroker1.service.conf %{buildroot}/%{_datadir}/dbus-1/system.d/com.microsoft.identity.devicebroker1.service.conf
install -D -m 0644 %{_builddir}/usr/share/dbus-1/system-services/com.microsoft.identity.devicebroker1.service %{buildroot}/%{_datadir}/dbus-1/system-services/com.microsoft.identity.devicebroker1.service

install -p -D -m 0644 %{_builddir}/usr/lib/sysusers.d/microsoft-identity-broker.conf %{buildroot}/%{_sysusersdir}/%{name}.conf

%pre
%sysusers_create_compat %{_sysusersdir}/%{name}.conf

%post
%systemd_post microsoft-identity-device-broker.service
%systemd_user_post microsoft-identity-broker.service

%preun
%systemd_preun microsoft-identity-device-broker.service
%systemd_user_preun microsoft-identity-broker.service

%postun
%systemd_postun_with_restart microsoft-identity-device-broker.service
%systemd_user_postun_with_restart microsoft-identity-broker.service

%files

%{_bindir}/microsoft-identity-broker
%{_bindir}/microsoft-identity-device-broker
%{_opt_bindir}/microsoft-identity-broker
%{_opt_bindir}/microsoft-identity-device-broker

%{_sysconfdir}/%{name}/lsb-release
%{_sysconfdir}/%{name}/os-release

%{_fontdir}/*.ttf
%{_opt_javadir}/*.jar

%{_unitdir}/microsoft-identity-device-broker.service
%{_userunitdir}/microsoft-identity-broker.service
%{_datadir}/dbus-1/services/com.microsoft.identity.broker1.service
%{_datadir}/dbus-1/system.d/com.microsoft.identity.devicebroker1.service.conf
%{_datadir}/dbus-1/system-services/com.microsoft.identity.devicebroker1.service

%{_sysusersdir}/%{name}.conf

%license %{_docdir}/%{name}/LICENSE

%changelog
%autochangelog
