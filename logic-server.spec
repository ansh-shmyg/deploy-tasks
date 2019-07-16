Name:           logic-server
Version:        1
Release:        1
Summary:        The logic service for Trading App

License:        GPL
URL:            https://github.com/ansh-shmyg/logic-srv
Source0:        logic-server-1.0.tar.gz

#BuildRequiroes:  
BuildRequires:	systemd
Requires:       python36
#BuildArch:      noarch
%description
The service for devops team traiding app.

%global	username app-logic

%pre
getent group %{username} >/dev/null || groupadd -r %{username}
getent passwd %{username} >/dev/null || \
useradd -r -g %{username} -M -s /sbin/nologin \
-c "Account to own and run %{username}" %{username}
exit

%post
/usr/bin/systemctl start %{username}.service >/dev/null 2>&1 && \
/usr/bin/systemctl enable %{username}.service >/dev/null 2>&1

%preun
/usr/bin/systemctl stop %{username}.service >/dev/null 2>&1 && \
/usr/bin/systemctl disable %{username}.service >/dev/null 2>&1

%postun
getent passwd %{username} >/dev/null && userdel -r %{username} >/dev/null 2>&1

%prep
%setup -q
%build
%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/opt/%{username}
install -m 0755 -d $RPM_BUILD_ROOT/etc/systemd/system
install -m 0755 -d $RPM_BUILD_ROOT/etc/default
install -m 0750 logic_server.py $RPM_BUILD_ROOT/opt/%{username}/logic_server.py
install -m 0644 %{username}.service $RPM_BUILD_ROOT/etc/systemd/system/%{username}.service
install -m 0644 %{username} $RPM_BUILD_ROOT/etc/default/%{username}

%files
%defattr(0750, %{username}, %{username}, 0755)
/opt/%{username}
/opt/%{username}/logic_server.py
%attr(0644,root,root) /etc/systemd/system/%{username}.service
%attr(0644,root,root) /etc/default/%{username}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jul 17 2019 Andrii Shmyhovskiy 1.0.1
  - Add systemd unit setup

* Tue Jul 16 2019 Andrii Shmyhovskiy 1.0.0
  - Build simple package
