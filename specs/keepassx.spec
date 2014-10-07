%define alpha master
%define attdir 69

Name:           keepassx
Version:        2.0
Release:        0.20140929%{?dist}
Summary:        Cross-platform password manager
Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.keepassx.org
Source0:        http://www.keepassx.org/dev/attachments/download/%{attdir}/%{name}-%{version}-%{alpha}.tar.gz
Source1:        %{name}.desktop
BuildRequires:  qt4-devel > 4.1
BuildRequires:  libXtst-devel
BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  libgcrypt-devel
Requires:       hicolor-icon-theme
Requires:       libgcrypt

%description
KeePassX is an application for people with extremly high demands on secure
personal data management.
KeePassX saves many different information e.g. user names, passwords, urls,
attachemts and comments in one single database. For a better management
user-defined titles and icons can be specified for each single entry.
Furthermore the entries are sorted in groups, which are customizable as well.
The integrated search function allows to search in a single group or the
complete database.
KeePassX offers a little utility for secure password generation. The password
generator is very customizable, fast and easy to use. Especially someone who
generates passwords frequently will appreciate this feature.
The complete database is always encrypted either with AES (alias Rijndael) or
Twofish encryption algorithm using a 256 bit key. Therefore the saved
information can be considered as quite safe. KeePassX uses a database format
that is compatible with KeePass Password Safe for MS Windows.

%prep
%setup -qn keepassx-%{version}-%{alpha}

%build
mkdir build
cd build
cmake .. \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_VERBOSE_MAKEFILE=ON \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DWITH_GUI_TESTS=ON

make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

# Use png in _datadir/icons/hicolor instead of xpm in pixmaps
#mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
#convert %{buildroot}%{_datadir}/pixmaps/keepassx.xpm \
#        %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/keepassx.png
#rm -f %{buildroot}%{_datadir}/pixmaps/keepassx.xpm

# Menu
%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__cp} %{SOURCE1}  %{buildroot}%{_datadir}/applications/%{name}.desktop
       
desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications \
        --delete-original \
        --add-mime-type application/x-keepass \
        %{buildroot}%{_datadir}/applications/%{name}.desktop

# Associate KDB* files
cat > x-keepass.desktop << EOF
[Desktop Entry]
Comment=
Hidden=false
Icon=keepassx
MimeType=application/x-keepass
Patterns=*.kdb;*.KDB;*.kdbx;*.KDBX*;
Type=MimeType
EOF
install -D -m 644 -p x-keepass.desktop \
  %{buildroot}%{_datadir}/mimelnk/application/x-keepass.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc CHANGELOG INSTALL COPYING LICENSE*

%{_bindir}/keepassx

%ifarch i386
%{_prefix}/lib/keepassx/*.so
%else
%{_prefix}/lib64/keepassx/*.so
%endif

%{_datadir}/keepassx
%{_datadir}/applications/*.desktop
%{_datadir}/mimelnk/application/*.desktop
%{_datadir}/mime/packages/keepassx.xml
%{_datadir}/icons/hicolor/*/apps/keepassx.*
%{_datadir}/icons/hicolor/*/mimetypes/application-x-keepassx.*

