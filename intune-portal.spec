Name: intune-portal
Version: 1.2405.17
Release: 1
Summary: Microsoft Intune
License: see /usr/share/doc/intune-portal/copyright
URL: https://www.microsoft.com

Requires: microsoft-identity-broker

%global msft_version %{version_no_tilde}
%global msft_release 1
Source0: https://packages.microsoft.com/rhel/9/prod/Packages/i/intune-portal-%{msft_version}-%{msft_release}.el9.x86_64.rpm
Source1: wrapper-intune-portal

%define _opt_prefix /opt/microsoft/intune/
%define _opt_bindir %{_opt_prefix}/bin
%define _opt_javadir %{_opt_prefix}/lib
%define _opt_datadir %{_opt_prefix}/share

%description
Microsoft Intune helps organizations manage access to corporate apps, data, and
resources. Microsoft Intune is the app that lets you, as an employee of your
company, securely access those resources.

Before you can use this app, make sure your IT admin has set up your work
account. Your company must also have a subscription to Microsoft Intune.

Microsoft Intune helps simplify the tasks you need to do for work:

- Enroll your device to access corporate resources, including Office, email,
and OneDrive for Business.
- Sign in to corporate resources with company-issued certificates.
- View and manage your enrolled devices – and wipe them if they get lost or
stolen.
- Get help directly from your IT department through available contact
information.

A note about Intune: every organization has different access requirements, and
will use Intune in ways that they determine will best manage their information.
Some functionality might be unavailable in certain countries. If you have
questions about how this app is being used within your organization, your
company’s IT administrator should have those answers for you. Microsoft, your
network provider, and your device’s manufacturer do not know how Intune will
be used by your organization.

%prep
rpm2cpio %{SOURCE0} | cpio -idmv > /dev/null 2>&1

%install

mkdir -p %{buildroot}/%{_bindir}

mkdir -p %{buildroot}/%{_opt_prefix}
mkdir -p %{buildroot}/%{_opt_bindir}
mkdir -p %{buildroot}/%{_opt_javadir}

mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_userunitdir}
mkdir -p %{buildroot}/%{_presetdir}
mkdir -p %{buildroot}/%{_userpresetdir}
mkdir -p %{buildroot}/%{_pam_moduledir}
mkdir -p %{buildroot}/%{_tmpfilesdir}

mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
mkdir -p %{buildroot}%{_opt_datadir}/locale

install -m 0755 %{SOURCE1} %{buildroot}/%{_bindir}/intune-agent
install -m 0755 %{SOURCE1} %{buildroot}/%{_bindir}/intune-daemon
install -m 0755 %{SOURCE1} %{buildroot}/%{_bindir}/intune-portal

install -m 0755 %{_builddir}%{_opt_bindir}/intune-agent %{buildroot}/%{_opt_bindir}/
install -m 0755 %{_builddir}%{_opt_bindir}/intune-daemon %{buildroot}/%{_opt_bindir}/
install -m 0755 %{_builddir}%{_opt_bindir}/intune-portal %{buildroot}/%{_opt_bindir}/

sed -i -r "s:^Exec(Start)?=.*/([^/]+):Exec\1=%{_bindir}/\2:" \
	%{_builddir}/usr/lib/systemd/*/*.service

# system services
install -m 0644 %{_builddir}/usr/lib/systemd/system/intune-daemon.service %{buildroot}/%{_unitdir}/
install -m 0644 %{_builddir}/usr/lib/systemd/system/intune-daemon.socket %{buildroot}/%{_unitdir}/
install -m 0644 %{_builddir}/usr/lib/systemd/system-preset/50-intune-system.preset %{buildroot}/%{_presetdir}/

# user services
install -m 0644 %{_builddir}/usr/lib/systemd/user/intune-agent.service %{buildroot}/%{_userunitdir}/
install -m 0644 %{_builddir}/usr/lib/systemd/user/intune-agent.timer %{buildroot}/%{_userunitdir}/
install -m 0644 %{_builddir}/usr/lib/systemd/user-preset/50-intune-user.preset %{buildroot}/%{_userpresetdir}/

install -m 0755 %{_builddir}/usr/lib64/security/pam_intune.so %{buildroot}/%{_pam_moduledir}/
install -m 0644 %{_builddir}/usr/lib/tmpfiles.d/intune.conf %{buildroot}%{_tmpfilesdir}/

#rm -rf usr/lib/.build-id/

cp %{_builddir}/opt/microsoft/intune/NOTICE.txt %{buildroot}/%{_opt_prefix}/
sed -i -r 's: [^ ]*bin/intune-portal: %{_bindir}/intune-portal:g' %{_builddir}/usr/share/applications/intune-portal.desktop
cp %{_builddir}/usr/share/applications/intune-portal.desktop %{buildroot}%{_datadir}/applications
cp %{_builddir}/usr/share/icons/hicolor/48x48/apps/intune.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
cp %{_builddir}/usr/share/polkit-1/actions/com.microsoft.intune.policy %{buildroot}%{_datadir}/polkit-1/actions/com.microsoft.intune.policy
cp -r %{_builddir}/opt/microsoft/intune/share/locale/. %{buildroot}/%{_opt_datadir}/locale

%post
%systemd_post intune-daemon.service intune-daemon.socket
%systemd_user_post intune-agent.service intune-agent.timer

%preun
%systemd_preun intune-daemon.service intune-daemon.socket
%systemd_user_preun intune-agent.service intune-agent.timer

%postun
%systemd_postun_with_restart intune-daemon.service intune-daemon.socket
%systemd_user_postun_with_restart intune-agent.service intune-agent.timer

%files

%{_pam_moduledir}/pam_intune.so

%{_opt_datadir}/locale/*

%{_tmpfilesdir}/intune.conf

%{_unitdir}/intune-daemon.service
%{_unitdir}/intune-daemon.socket
%{_presetdir}/50-intune-system.preset

%{_userunitdir}/intune-agent.service
%{_userunitdir}/intune-agent.timer
%{_userpresetdir}/50-intune-user.preset

%{_opt_bindir}/intune-agent
%{_opt_bindir}/intune-daemon
%{_opt_bindir}/intune-portal

%{_bindir}/intune-agent
%{_bindir}/intune-daemon
%{_bindir}/intune-portal

%license %{_opt_prefix}/NOTICE.txt
%{_datadir}/applications/intune-portal.desktop
%{_datadir}/icons/hicolor/48x48/apps/intune.png
%{_datadir}/polkit-1/actions/com.microsoft.intune.policy

%changelog
%autochangelog
