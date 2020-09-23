%global uuid    com.github.Latesil.%{name}

Name:           project-starter
Version:        0.1.5
Release:        1%{?dist}
Summary:        Simple program for starting new projects with various templates and with various languages.

License:        GPLv3+
URL:            https://github.com/Latesil/project-starter
Source0:        %{url}/archive/%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(gtk+-3.0)
Requires:       hicolor-icon-theme

%description
%{summary}.


%prep
%autosetup -n %{name}-%{version} -p1


%build
%meson
%meson_build


%install
%meson_install
%find_lang %{uuid}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{uuid}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/symbolic/*/*.svg
%{_metainfodir}/*.xml


%changelog
* Wed Sep 23 2020 Latesil <vihilantes@gmail.com> - 0.1.5-1
- Refactor some code

* Thu Jul 30 2020 Latesil <vihilantes@gmail.com> - 0.1.4-1
- Initial package

