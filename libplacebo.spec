#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Reusable library for GPU-accelerated video/image rendering
Summary(pl.UTF-8):	Biblioteka do renderowania filmów/obrazu ze wsparciem GPU
Name:		libplacebo
Version:	3.120.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://code.videolan.org/videolan/libplacebo/tags
Source0:	https://code.videolan.org/videolan/libplacebo/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	e345e3b572771eed7e336d33b6a140e5
URL:		https://code.videolan.org/videolan/libplacebo
BuildRequires:	gcc >= 5:3.2
BuildRequires:	glslang-devel
# >= 2763
BuildRequires:	lcms2-devel >= 2.6
BuildRequires:	libepoxy >= 1.4.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	meson >= 0.51
BuildRequires:	ninja >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shaderc-devel >= 2021.0-2
BuildRequires:	Vulkan-Loader-devel >= 1.0.42
Requires:	libepoxy >= 1.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Reusable library for GPU-accelerated video/image rendering.

%description -l pl.UTF-8
Biblioteka do renderowania filmów/obrazu ze wsparciem GPU.

%package devel
Summary:	Header files for libplacebo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libplacebo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lcms2-devel >= 2.6
Requires:	shaderc-devel
Requires:	Vulkan-Loader-devel

%description devel
Header files for libplacebo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libplacebo.

%package static
Summary:	Static libplacebo library
Summary(pl.UTF-8):	Statyczna biblioteka libplacebo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libplacebo library.

%description static -l pl.UTF-8
Statyczna biblioteka libplacebo.

%prep
%setup -q -n %{name}-v%{version}

%{__sed} -ne '1,/^-----/ p' LICENSE > COPYING

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Ddemos=false

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_libdir}/libplacebo.so.120

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libplacebo.so
%{_includedir}/libplacebo
%{_pkgconfigdir}/libplacebo.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libplacebo.a
%endif
