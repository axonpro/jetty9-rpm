%define pkgname %{?override_pkgname}%{?!override_pkgname:jetty9b}
%define jetty9user %{pkgname}
%define jetty9group %{pkgname}
%define dirname jetty-distribution

Name:		%{pkgname}
#Version:	9.0.5.v20130815
#Version:	9.1.1.v20140108
Version:	9.0.7.v20131107
Release:	26%{?dist}
Summary:	Jetty Binary Distribution
Packager:	Ernest Beinrohr <Ernest.Beinrohr@axonpro.sk>
Group:		Java
License:	Apache and Eclipse
URL:		http://www.eclipse.org/jetty/
Source0:	http://eclipse.org/downloads/download.php?r=1&file=/jetty/stable-9/dist/%{dirname}-%{version}.tar.gz
Source2:	%{pkgname}-sysconfig
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Summary:	Jetty is an open-source project providing an HTTP server, HTTP client, and javax.servlet container.

Requires:	java-1.7.0-oracle
Conflicts:	jdk
Obsoletes:	jdk

%description
The Jetty Web Server provides a HTTP server and Servlet
container capable of serving static and dynamic contend
either from a standalone or embedded instantiations. From
jetty-7, the jetty webserver and other core compoments are
hosted by the eclipse foundation. The project provides:
* Asynchronous HTTP Server
* Standard based Servlet Container
* Web Sockets server
* Asynchronous HTTP Client
* OSGi, JNDI, JMX, JASPI, AJP support

%prep
rm -rf %{buildroot}
%setup -q -n %{dirname}-%{version} 

%build

%pre
getent group %{jetty9group} >/dev/null || groupadd -r %{jetty9group}
getent passwd %{jetty9user} >/dev/null || \
useradd -r -g %{jetty9group} -d /var/lib/%{name} \
    -c "Jetty user" %{jetty9user} || :

%post
chkconfig --add %{name}
chkconfig %{name} on

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    service %{name} stop
    chkconfig %{name} off
    chkconfig --del %{name}
fi

%install
install -m 755 -d %{buildroot}/usr/share/doc/%{name}-%{version}/
install -m 755 -d %{buildroot}/etc/%$name}/
install -m 755 -d %{buildroot}/%{_initddir}/
install -m 755 -d %{buildroot}/%{_javadir}/%{name}/
install -m 755 -d %{buildroot}/%{_javadir}/%{name}/resources
install -m 755 -d %{buildroot}/var/log/%{name}/
install -m 755 -d %{buildroot}/var/run/%{name}/
install -m 755 -d %{buildroot}/var/lib/%{name}/
install -m 755 -d %{buildroot}/var/lib/%{name}/start.d/
install -m 755 -d %{buildroot}/var/lib/%{name}/work
install -m 755 -d %{buildroot}/etc/sysconfig/
install -m 755 -d %{buildroot}/etc/default/

cp -a README.txt notice.html VERSION.txt  license-eplv10-aslv20.html %{buildroot}/usr/share/doc/%{name}-%{version}/
cp -a etc/ %{buildroot}/etc/%{name}/
cp -a resources/* %{buildroot}/etc/%{name}/
cp bin/jetty.sh %{buildroot}/%{_initddir}/%{name}
#cp -a lib/ start.jar start.ini start.d/ %{buildroot}/%{_javadir}/%{name}/
#cp -a webapps start.d %{buildroot}/var/lib/%{name}/
#cp -a modules/ start.ini %{buildroot}/%{_javadir}/%{name}/
cp -a lib/ start.jar start.ini %{buildroot}/%{_javadir}/%{name}/
cp -a webapps %{buildroot}/var/lib/%{name}/
cp %{SOURCE2} %{buildroot}/etc/sysconfig/%{name}
ln -s /etc/sysconfig/%{name} %{buildroot}/etc/default/
ln -s /etc/%{pkgname}/ %{buildroot}%{_javadir}/%{name}/etc
ln -s /var/log/%{name}/     %{buildroot}/%{_javadir}/%{name}/logs
ln -s /var/log/%{name}/     %{buildroot}/var/lib/%{name}/logs
ln -s /var/lib/%{name}/webapps     %{buildroot}/%{_javadir}/%{name}/webapps
ln -s /var/lib/%{name}/work     %{buildroot}/%{_javadir}/%{name}/work

perl -p -i -e 's/ETC\/default\/jetty/ETC\/default\/%{pkgname}/g' %{buildroot}/%{_initddir}/%{name}

echo "OPTIONS=rewrite" >> %{buildroot}/%{_javadir}/%{name}/start.ini
echo "OPTIONS=client" >> %{buildroot}/%{_javadir}/%{name}/start.ini
echo "OPTIONS=jaas" >> %{buildroot}/%{_javadir}/%{name}/start.ini
echo "OPTIONS=jndi" >> %{buildroot}/%{_javadir}/%{name}/start.ini
echo "OPTIONS=plus" >> %{buildroot}/%{_javadir}/%{name}/start.ini
echo "OPTIONS=annotations" >> %{buildroot}/%{_javadir}/%{name}/start.ini

#echo "--module=rewrite" >> %{buildroot}/%{_javadir}/%{name}/start.ini
#echo "--module=client" >> %{buildroot}/%{_javadir}/%{name}/start.ini
#echo "--module=jaas" >> %{buildroot}/%{_javadir}/%{name}/start.ini
#echo "--module=jndi" >> %{buildroot}/%{_javadir}/%{name}/start.ini
#echo "--module=plus" >> %{buildroot}/%{_javadir}/%{name}/start.ini
#echo "--module=annotations" >> %{buildroot}/%{_javadir}/%{name}/start.ini

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc /usr/share/doc/%{name}-%{version}
%config /etc/%{name}
%{_javadir}/%{name}/
%attr(775, %{jetty9user}, %{jetty9group}) /var/log/%{name}/
%attr(775, %{jetty9user}, %{jetty9group}) /var/run/%{name}/
%attr(751, %{jetty9user}, %{jetty9group}) /var/lib/%{name}
%{_initddir}/%{name}
%config /etc/sysconfig/%{name}
/etc/default/%{name}

%changelog
* Tue Mar 11 2014 Ernest Beinrohr <Ernest@Beinrohr.sk> - 9.0.7
- New jetty
- oracle java & -jdk

* Wed Jan 15 2014 Ernest Beinrohr <Ernest@Beinrohr.sk> - 9.1.1.v20140108.17
- New jetty
- Added $jetty_home/work dir + symlink
- chkconfig upgrade repair
- modules added + OPTIONS removed
- resources dir added

* Tue Nov 06 2013 Ernest Beinrohr <Ernest@Beinrohr.sk> - 9.0.5.v20130815.14
- Added options to start.ini

* Thu Oct 30 2013 Ernest Beinrohr <Ernest@Beinrohr.sk>
- Re-added start.d 

* Thu Oct 11 2013 Ernest Beinrohr <Ernest@Beinrohr.sk>
- Dropped start.d dir with demo.ini

* Thu Oct 11 2013 Ernest Beinrohr <Ernest@Beinrohr.sk>
- Parametrized build

* Thu Oct 01 2013 Ernest Beinrohr <Ernest@Beinrohr.sk>
- Java opts

* Thu Sep 30 2013 Ernest Beinrohr <Ernest@Beinrohr.sk>
- Demo apps disabled, sysconfig option added

* Thu Sep 26 2013 Ernest Beinrohr <Ernest@Beinrohr.sk>
- Require Oracle java 1.7 (jdk-1.7)

* Thu Aug 23 2013 Ernest Beinrohr <Ernest@Beinrohr.sk>  - 9.0.5.v20130815.3
- Conflicting ports 8443

* Thu Aug 23 2013 Ernest Beinrohr <Ernest@Beinrohr.sk>
- Changed jettys homedir, so ssh keys can be used

* Thu Aug 23 2013 Ernest Beinrohr <Ernest@Beinrohr.sk>
- Initial RPM release


