Name: wock
Version: 0.1
Release: 1%{?dist}
Summary: A stupid wrapper for mock
Group: Development/Tools
License: ASL 2.0
URL: https://github.com/cgtx/wock
Source0: https://github.com/cgtx/%{name}/archive/%{version}.tar.gz
Source1: wock.bash_completion
BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires: python3-click


%description
A stupid wrapper for mock.


%prep
%setup -q


%build
%{__python3} setup.py build


%install
%{__python3} setup.py install --skip-build --root %{buildroot}
%{__install} -Dm0644 %{SOURCE1} %{buildroot}/%{_datadir}/bash-completion/completions/wock


%files
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py?.?.egg-info
%{_datadir}/bash-completion/completions/wock


%changelog
* Tue Feb 10 2015 Carl George <carl.george@rackspace.com> - 0.1-1
- Initial package
