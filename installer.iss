[Setup]
AppName=Desktop Cleaner
AppVersion=1.0
DefaultDirName={localappdata}\DesktopCleaner
DefaultGroupName=Desktop Cleaner
OutputDir=.
DisableProgramGroupPage=no
UninstallDisplayIcon={app}\cleaner.exe
PrivilegesRequired=lowest

[Files]
Source: "dist\cleaner.exe"; DestDir: "{app}"
Source: "dist\settings.exe"; DestDir: "{app}"
Source: "config.json"; DestDir: "{app}"; Flags: onlyifdoesntexist

[Registry]
; Пункт контекстного меню (тільки для поточного користувача)
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\DesktopCleaner"; ValueType: string; ValueData: "Очистити робочий стіл"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\DesktopCleaner"; ValueName: "Icon"; ValueType: string; ValueData: "{app}\cleaner.exe"
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\DesktopCleaner\command"; ValueType: string; ValueData: """{app}\cleaner.exe"""

[Tasks]
Name: "desktopicon"; Description: "Створити ярлик на робочому столі"; GroupDescription: "Додаткові задачі:"; Flags: checkedonce

[Icons]
; Меню Пуск
Name: "{group}\Очистити робочий стіл"; Filename: "{app}\cleaner.exe"
Name: "{group}\Налаштування"; Filename: "{app}\settings.exe"
Name: "{group}\Видалити Desktop Cleaner"; Filename: "{uninstallexe}"

; Опційний ярлик на робочому столі
Name: "{userdesktop}\Desktop Cleaner Settings"; Filename: "{app}\settings.exe"; Tasks: desktopicon