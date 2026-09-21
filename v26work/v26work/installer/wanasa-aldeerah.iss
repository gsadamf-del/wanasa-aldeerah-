#define MyAppName "Wanasa Al Deerah"
#define MyAppVersion "26.0.0"
#define MyAppExeName "wanasa_aldeerah.exe"
[Setup]
AppId={{9D6B6A5C-8D2A-4C8C-9F6B-5A0B4C260001}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\Wanasa Al Deerah
DefaultGroupName=Wanasa Al Deerah
OutputDir=output
OutputBaseFilename=WanasaAlDeerah-Setup-v26.0.0
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
[Files]
Source: "..\mobile\build\windows\x64\runner\Release\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion
[Icons]
Name: "{autoprograms}\Wanasa Al Deerah"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Wanasa Al Deerah"; Filename: "{app}\{#MyAppExeName}"
[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "تشغيل وناسة الديرة"; Flags: nowait postinstall skipifsilent
