#Module-Specific definitions
%define mod_name mod_estraier
%define mod_conf A54_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	An apache module that uses the API of Hyper Estraier
Name:		apache-%{mod_name}
Version:	0.3.2
Release:	%mkrel 2
Group:		System/Servers
License:	Apache License
URL:		http://modestraier.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/modestraier/mod_estraier-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.0.54
Requires(pre):	apache >= 2.0.54
Requires:	apache-conf >= 2.0.54
Requires:	apache >= 2.0.54
BuildRequires:	apache-devel >= 2.0.54
BuildRequires:	file
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	libqdbm-devel
BuildRequires:	libhyperestraier-devel
BuildRequires:	libtidy-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_estraier is an apache module that registers web pages processed by the
apache and search from them using the node API of Hyper Estraier. Especially,
indexing and searching the documents through the proxy or dynamic contents like
Wiki or BBS is the main object of mod_estraier.

%prep

%setup -q -n %{mod_name}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
sh ./autogen.sh

%configure2_5x \
    --with-apxs=%{_sbindir}/apxs \
    --with-tidy=%{_prefix}

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/mod_estraier_cache.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0755 .libs/mod_estraier_search.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0755 .libs/mod_estraier.so %{buildroot}%{_libdir}/apache-extramodules/

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/* tmpl/* ChangeLog README* TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_estraier_cache.so
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_estraier_search.so
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_estraier.so
%{_var}/www/html/addon-modules/*


