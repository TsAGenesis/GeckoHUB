@echo off
cd /d "C:\Users\niko3\GeckoHUB"

REM Fügt ALLE neuen/geänderten Dateien im images-Ordner hinzu:
git add images 2>nul

echo --------------------------------------------------
git status
echo --------------------------------------------------

git diff --cached --quiet
if %ERRORLEVEL% EQU 0 (
    echo Keine neuen oder geänderten Bilder gefunden.
    pause
    exit /b 0
)

for /f "tokens=2 delims==." %%I in ('"wmic os get localdatetime /value"') do set datetime=%%I
set commitdate=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%
git commit -m "Auto: add/update images %commitdate%"
git push

echo.
echo ✅ Bilder wurden (falls vorhanden) hochgeladen!
pause
