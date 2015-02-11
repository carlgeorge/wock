Name: wock
Version: 0.1
Release: 1%{?dist}
Summary: A wrapper for mock
Group: Development/Tools
License: ASL 2.0
URL: https://github.rackspace.com/carl-george/wock
Source0: https://github.rackspace.com/carl-george/%{name}/archive/%{version}.tar.gz
Source1: wock.bash_completion
BuildArch: noarch
BuildRequires: bash-completion
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires: bash-completion
Requires: python3-click


%description
A wrapper for mock.


%prep
%setup -q


%build
%{__python3} setup.py build


%install
%{__python3} setup.py install --skip-build --root %{buildroot}
%{__install} -Dm0644 %{SOURCE1} %{buildroot}/%{_datadir}/bash-completion/completions/wock


%files
%doc README.md
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py?.?.egg-info
%{_datadir}/bash-completion/completions/wock


%changelog
* Tue Feb 10 2015 Carl George <carl.george@rackspace.com> - 0.1-1
- Initial package