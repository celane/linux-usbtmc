#
# build rpm from git, use 'git-build-rpm' :
# git build-rpm --rpm-dir /home/me/rpmbuild --dist .fc35
# the --rpm-dir is to save the .srpm file, the --dist is
# to avoid the longwinded version that is otherwise autogenerated
#
Name:           linux-usbtmc
Version:        1.4
Release:        1%{?dist}
Summary:        USBTMC driver (GPIB over USB)

License:        GPL
URL:            https://github.com/celane/linux-usbtmc
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch
Requires:       dkms
BuildRequires:  sed
BuildRequires:  gawk

%description
Driver for USBTMC interface to USBTMC devices in DKMS package


%prep
%autosetup

v=`awk '/#define\s+USBTMC_VERSION/ {print $3}' usbtmc.c | sed 's/\"//g'`
if [ "$v" != "%{version}" ] ; then
echo "version mismatch, spec file  vs code"
exit 1
fi
sed -i -e 's/__VERSION_STRING/%{version}/g' dkms.conf

%build


%install

install -d %{buildroot}%{_usrsrc}/%{name}-%{version}-%{release}
cp *.c *.h Makefile  %{buildroot}%{_usrsrc}/%{name}-%{version}-%{release}
install -p -m 0644 dkms.conf %{buildroot}%{_usrsrc}/%{name}-%{version}-%{release}



%files
%license LICENSE
%doc COPYING README.md
%dir %{_usrsrc}/%{name}-%{version}-%{release}
%{_usrsrc}/%{name}-%{version}-%{release}/*

%post
dkms add -m %{name} -v %{version}-%{release} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel
dkms build -m %{name} -v %{version}-%{release} -q || :
dkms install -m %{name} -v %{version}-%{release} -q --force || :


%preun 
# Remove all versions from DKMS registry
dkms remove -m %{name} -v %{version}-%{release} -q --all --rpm_safe_upgrade || :

%changelog
* Fri Dec 30 2022 lane@dchooz.org
- initial version

