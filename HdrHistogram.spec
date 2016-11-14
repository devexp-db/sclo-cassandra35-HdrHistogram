%{?scl:%scl_package HdrHistogram}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}HdrHistogram
Version:	2.1.9
Release:	2%{?dist}
Summary:	A High Dynamic Range (HDR) Histogram
License:	BSD and CC0
URL:		http://hdrhistogram.github.io/%{pkg_name}/
Source0:	https://github.com/%{pkg_name}/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz

# remove maven-replacer-plugin because it has no meaningfull use
Patch0:		%{pkg_name}-%{version}-remove-replacer.patch

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:	%{?scl_prefix_maven}sonatype-oss-parent
BuildRequires:	%{?scl_prefix_java_common}junit
%{?scl:Requires: %scl_runtime}

BuildArch:	noarch

%description
HdrHistogram supports the recording and analyzing sampled data value
counts across a configurable integer value range with configurable value
precision within the range. Value precision is expressed as the number of
significant digits in the value recording, and provides control over value
quantization behavior across the value range and the subsequent value
resolution at any given level.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}
find  -name "*.class"  -print -delete
find  -name "*.jar"  -print -delete

# plugin is prety much useless and as it is missing in RHEL we remove it
%patch0 -p1

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_remove_plugin :maven-dependency-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-source-plugin

%mvn_file :%{pkg_name} %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}
%jpackage_script org.%{pkg_name}.HistogramLogProcessor "" "" %{pkg_name} HistogramLogProcessor true

%files -f .mfiles
%{_bindir}/HistogramLogProcessor
%doc README.md
%license COPYING.txt LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license COPYING.txt LICENSE.txt

%changelog
* Thu Nov 10 2016 Tomas Repik <trepik@redhat.com> - 2.1.9-2
- scl conversion

* Tue Jun 21 2016 Tomas Repik <trepik@redhat.com> - 2.1.9-1
- Update to 2.1.9

* Mon Mar 07 2016 Tomas Repik <trepik@redhat.com> - 2.1.8-1
- launcher HistogramLogProcessor installation
- Update to 2.1.8

* Thu Oct 22 2015 gil cattaneo <puntogil@libero.it> 2.1.7-1
- initial rpm
