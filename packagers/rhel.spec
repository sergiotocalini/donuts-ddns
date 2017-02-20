Summary:                 Donuts Dynamic DNS updater agent.
Name:                    donuts-ddns
Version:                 1.0.1
Release:                 1%{?dist}
License:                 GPLv3
URL:                     https://github.com/sergiotocalini/donuts-ddns
Source0:                 https://github.com/sergiotocalini/donuts-ddns/download/donuts_ddns-%{version}.tar.gz
Group:                   Development/Languages
BuildArch:               noarch
Requires:                python26
Requires:                python26-requests
Requires:                python26-PyYAML
Requires:                python26-setuptools

%description
Donuts DDNS is an agent to update your dynamic DNS records from Donuts Manager.

%clean

%prep
%setup -q -n donuts_ddns-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add donuts-ddns
/sbin/chkconfig --level 345 donuts-ddns on

%files
%defattr(-,root,root,-)
                        /etc/donuts
                        /etc/init.d/donuts*
                        %{python_sitelib}/donuts_ddns
			%{python_sitelib}/donuts_ddns-*-py2.*.egg-info
%attr(755,-,-)          /usr/bin

%changelog
* Sat Jul 23 2016 Sergio Tocalini Joerg <sergiotocalini@gmail.com> - 1.0.1
- Initial spec with donuts_ddns-1.0.1 version.
