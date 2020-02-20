
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%global with_doc 1

%global pypi_name muranoclient
%global cname murano

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Client library for Murano built on the Murano API. It provides a Python \
API (the muranoclient module) and a command-line tool (murano).

Name:           python-%{pypi_name}
Version:        1.3.0
Release:        1%{?dist}
Summary:        Client library for OpenStack Murano API

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        Client library for OpenStack Murano API.
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pypi_name} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr >= 2.0.0

Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-glanceclient >= 1:2.8.0
Requires:       python%{pyver}-iso8601 >= 0.1.11
Requires:       python%{pyver}-keystoneclient >= 1:3.8.0
Requires:       python%{pyver}-murano-pkg-check >= 0.3.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-prettytable >= 0.7.2
Requires:       python%{pyver}-requests >= 2.14.2
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-yaql >= 1.1.3
Requires:       python%{pyver}-osc-lib >= 1.10.0
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-pyOpenSSL >= 16.2.0
# Handle python2 exception
%if %{pyver} == 2
Requires:       PyYAML >= 3.10
%else
Requires:       python%{pyver}-PyYAML >= 3.10
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Murano API Client

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for the client library for interacting with Openstack
Murano API.
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cname} %{buildroot}%{_bindir}/%{cname}-%{pyver}

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/murano
%{_bindir}/murano-%{pyver}

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Sep 20 2019 RDO <dev@lists.rdoproject.org> 1.3.0-1
- Update to 1.3.0

