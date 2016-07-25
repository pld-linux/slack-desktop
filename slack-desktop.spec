# TODO
# - src.rpm specifies, is it correct (link is 404)
#   URL - https://github.com/tinyspeck/slack-winssb.git
#   License - MIT
# - it's based on atom

Summary:	Desktop client for Slack
Name:		slack-desktop
Version:	2.1.0
Release:	1
License:	?
Group:		X11/Applications
# Source0Download: https://slack.com/downloads
Source0:	https://slack-ssb-updates.global.ssl.fastly.net/linux_releases/slack-%{version}-0.1.fc21.x86_64.rpm
# NoSource0-md5:	ca2d2762850a0bdc24596710d0b73a95
NoSource:	0
Patch0:		desktop.patch
URL:		https://slack.com/
BuildRequires:	rpm-utils
BuildRequires:	rpmbuild(macros) >= 1.596
Requires:	desktop-file-utils
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_prefix}/lib/%{name}

%description
Get full access to your messages and archives, upload files easily,
and receive notifications whether you're at your desk or on the go.

%prep
%setup -qcT
SOURCE=%{S:0}

version=$(rpm -qp --nodigest --nosignature --qf '%{V}' $SOURCE)
test version:${version} = version:%{version}
rpm2cpio $SOURCE | cpio -i -d

mv usr/lib/slack .
mv usr/share/pixmaps/* .
mv usr/share/applications/* .
mv slack/LICENSE* .

%ifarch linux
rm -v resources/*/*/lib/*.dll
%endif

%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir},%{_desktopdir},%{_pixmapsdir}}

cp -a slack/* $RPM_BUILD_ROOT%{_appdir}
ln -s %{_appdir}/slack $RPM_BUILD_ROOT%{_bindir}

cp -p slack.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p slack.png $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_bindir}/slack
%{_desktopdir}/slack.desktop
%{_pixmapsdir}/slack.png
%dir %{_appdir}
%{_appdir}/version
%{_appdir}/*.bin
%{_appdir}/content_shell.pak
%{_appdir}/icudtl.dat
%attr(755,root,root) %{_appdir}/slack
%attr(755,root,root) %{_appdir}/libCallsCore.so
%attr(755,root,root) %{_appdir}/libffmpeg.so
%attr(755,root,root) %{_appdir}/libnode.so

%{_appdir}/locales

%dir %{_appdir}/resources
%{_appdir}/resources/app.asar
%{_appdir}/resources/default_app.asar
%{_appdir}/resources/electron.asar

# too many files to list, assume file permissions
%defattr(-,root,root,-)
%{_appdir}/resources/app.asar.unpacked
