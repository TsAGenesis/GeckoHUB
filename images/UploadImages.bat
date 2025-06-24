@echo off
REM Automatischer Git-Workflow für images-Ordner

REM Setze den Pfad zu deinem Repo an! (ggf. anpassen)
set "REPO=C:\Users\niko3\GeckoHUB"

cd /d "%REPO%"

REM Alle neuen/geänderten Dateien in images hinzufügen
git add images

REM Zeig Status
git status

REM Prüfe, ob überhaupt was zu committen ist
git diff --cached --quiet
if %ERRORLEVEL% EQU 0 (
    echo Keine neuen oder geänderten Bilder gefunden.
    pause
    exit /b 0
)

REM Commit mit aktuellem Datum/Uhrzeit
for /f "tokens=2 delims==." %%I in ('"wmic os get localdatetime /value"') do set datetime=%%I
set commitdate=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%
git commit -m "Auto: add/update images %commitdate%"

REM Pull, um Konflikte zu vermeiden
git pull --no-edit

REM Zeig Merge-Konflikte (falls welche da sind)
git status
findstr /C:"Unmerged paths" NUL 2>NUL
if not errorlevel 1 (
    echo.
    echo Merge-Konflikt! Bitte Konflikt manuell im Repo lösen.
    pause
    exit /b 1
)

REM Push
git push

echo.
echo ✅ Bilder wurden (falls vorhanden) hochgeladen!
pause
