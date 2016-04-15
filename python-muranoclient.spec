%global pypi_name muranoclient

%if 0%{?fedora}
%global with_python3 0
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        0.8.4
Release:        1%{?dist}
Summary:        Client library for OpenStack Murano API

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Client library for Murano built on the Murano API. It provides a Python
API (the muranoclient module) and a command-line tool (murano).


%package -n     python2-%{pypi_name}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr >= 1.6

Requires:       python-babel >= 1.3
Requires:       python-glanceclient >= 2.0.0
Requires:       python-httplib2 >= 0.7.5
Requires:       python-iso8601 >= 0.1.9
Requires:       python-keystoneclient >= 1.6.0
Requires:       python-openstackclient >= 2.1.0
Requires:       python-pbr >= 1.6
Requires:       python-prettytable >= 0.7
Requires:       python-requests >= 2.8.1
Requires:       python-six >= 1.9.0
Requires:       python-yaql >= 1.1.0
Requires:       python2-oslo-log >= 1.14.0
Requires:       python2-oslo-i18n >= 2.1.0
Requires:       python2-oslo-serialization >= 1.10.0
Requires:       python2-oslo-utils >= 3.5.0
Requires:       pyOpenSSL >= 0.14
Requires:       PyYAML >= 3.1.0

Summary:        Client library for OpenStack Murano API.
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Client library for Murano built on the Murano API. It provides a Python
API (the muranoclient module) and a command-line tool (murano).

# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Support of EC2 API for OpenStack
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6
BuildRequires:  python-tools

Requires:       python3-babel >= 1.3
Requires:       python3-glanceclient >= 2.0.0
Requires:       python3-httplib2 >= 0.7.5
Requires:       python3-iso8601 >= 0.1.9
Requires:       python3-keystoneclient >= 1.6.0
Requires:       python3-oslo-log >= 1.14.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.5.0
Requires:       python3-pbr >= 0.6
Requires:       python3-prettytable >= 0.7
Requires:       python3-requests >= 2.8.1
Requires:       python3-six >= 1.9.0
Requires:       python3-yaql >= 1.1.0
Requires:       pyOpenSSL >= 0.14
Requires:       PyYAML >= 3.1.0

%description -n python3-%{pypi_name}
Client library for Murano built on the Murano API. It provides a Python
API (the muranoclient module) and a command-line tool (murano).
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Murano API Client

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx >= 2.3.0

%description -n python-%{pypi_name}-doc
Documentation for the client library for interacting with Openstack
Murano API.

%prep
%autosetup -n %{name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/murano %{buildroot}%{_bindir}/python3-murano
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# rename binaries, make compat symlinks
pushd %{buildroot}%{_bindir}
%if 0%{?with_python3}
for i in %{pypi_name}-{3,%{?python3_shortver}}; do
    ln -s  python3-%{pypi_name} $i
done
%endif
popd

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/murano*

# Files for python3
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/python3-murano
%{_bindir}/murano*
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE

%changelog
* Wed Apr 13 2016 Marcos Fermin Lobo <marcos.fermin.lobo@cern.ch> 0.8.4-1
- First RPM
