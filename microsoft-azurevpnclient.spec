Name: microsoft-azurevpnclient
Version: 3.0.0
Release: 1
Summary: Azure VPN Client
License: see /usr/share/doc/microsoft-azurevpnclient/copyright
URL: https://www.microsoft.com

%global msft_version %{version_no_tilde}
Source0: https://packages.microsoft.com/ubuntu/22.04/prod/pool/main/m/microsoft-azurevpnclient/microsoft-azurevpnclient_%{msft_version}_amd64.deb
Source1: find-requires

%define _opt_prefix /opt/microsoft/microsoft-azurevpnclient

BuildRequires: dpkg

%description
   The Azure VPN Client lets you connect to Azure securely from anywhere in the world. It supports Microsoft Entra ID and certificate-based authentication.

# Note: 'global' evaluates NOW, 'define' allows recursion later...
%global _use_internal_dependency_generator 0
%global __find_requires_orig %{__find_requires}
%define __find_requires %{_builddir}/%{?buildsubdir}/find-requires %{__find_requires_orig}

%prep
dpkg-deb -x %{SOURCE0} %{buildroot}
rm -rf %{buildroot}/etc/rsyslog.d/

%post
setcap cap_net_admin+eip /opt/microsoft/microsoft-azurevpnclient/microsoft-azurevpnclient

%files
%{_opt_prefix}/data/flutter_assets/*
%{_opt_prefix}/data/icudtl.dat

%{_opt_prefix}/lib/*.so
%{_opt_prefix}/microsoft-azurevpnclient

%{_datadir}/applications/microsoft-azurevpnclient.desktop

%{_datadir}/icons/microsoft-azurevpnclient.png

%{_datadir}/polkit-1/rules.d/microsoft-azurevpnclient.rules
"/var/lib/polkit-1/localauthority/50-local.d/10-microsoft-azurevpnclient.pkla"

%{_datadir}/doc/microsoft-azurevpnclient/changelog.gz
%{_datadir}/doc/microsoft-azurevpnclient/NOTICE.txt.gz
%license %{_datadir}/doc/microsoft-azurevpnclient/copyright

%changelog
%autochangelog
