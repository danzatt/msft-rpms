#!/bin/bash

function fail()
{
        [ -n "$1" ] && echo "FAILED: $1"
        exit 1
}


sudo dnf install -y rpmdevtools rpmlint dpkg || fail "Failed to instal required packages."
rpmdev-setuptree || fail "Failed to setup RPM tree."

cp wrapper-identity-broker \
	wrapper-intune-portal \
	lsb-release-ubuntu-22.04 \
	os-release-ubuntu-22.04 \
	~/rpmbuild/SOURCES/

for specfile in *.spec
do
	spectool -g -R $specfile || fail "Cannot dowload sources for $specfile"
	rpmbuild -bb $specfile || fail "Failed to build $specfile"
done

dnf install -y ~/rpmbuild/RPMS/x86_64/*
