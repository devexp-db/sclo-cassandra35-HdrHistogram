Name:          HdrHistogram
Version:       2.1.9
Release:       1%{?dist}
Summary:       A High Dynamic Range (HDR) Histogram
License:       BSD and CC0
URL:           http://hdrhistogram.github.io/%{name}/
Source0:       https://github.com/%{name}/%{name}/archive/%{name}-%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(com.google.code.maven-replacer-plugin:replacer)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)
# fedora 25
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)

BuildArch:     noarch

%description
HdrHistogram supports the recording and analyzing sampled data value
counts across a configurable integer value range with configurable value
precision within the range. Value precision is expressed as the number of
significant digits in the value recording, and provides control over value
quantization behavior across the value range and the subsequent value
resolution at any given level.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}
find  -name "*.class"  -print -delete
find  -name "*.jar"  -print -delete

%pom_remove_plugin :maven-dependency-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-source-plugin

%pom_xpath_set "pom:plugin[pom:groupId = 'com.google.code.maven-replacer-plugin' ]/pom:artifactId" replacer

%mvn_file :%{name} %{name}

%build
%mvn_build

%install
%mvn_install

%jpackage_script org.%{name}.HistogramLogProcessor "" "" %{name} HistogramLogProcessor true

%files -f .mfiles
%{_bindir}/HistogramLogProcessor
%doc README.md
%license COPYING.txt LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license COPYING.txt LICENSE.txt

%changelog
* Tue Jun 21 2016 Tomas Repik <trepik@redhat.com> - 2.1.9-1
- Update to 2.1.9

* Mon Mar 07 2016 Tomas Repik <trepik@redhat.com> - 2.1.8-1
- launcher HistogramLogProcessor installation
- Update to 2.1.8

* Thu Oct 22 2015 gil cattaneo <puntogil@libero.it> 2.1.7-1
- initial rpm
