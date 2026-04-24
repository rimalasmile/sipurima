@echo off
REM ==========================================================================
REM  Sipurima Image Pipeline
REM  Runs: face-blur -> frame-extract -> responsive WebP+JPG generation
REM  Prereq: Python 3.12 with opencv-python, mediapipe, pillow installed
REM          ImageMagick and ffmpeg on fixed paths (see variables below)
REM ==========================================================================

setlocal
set PY=C:\Users\Avner\AppData\Local\Programs\Python\Python312\python.exe
set ROOT=C:\Users\Avner\Documents\sipurima
set SCRIPTS=%ROOT%\website\scripts
set ASSETS=%ROOT%\website\assets
set SRC_IMG=%ASSETS%\source-to-blur
set BLURRED=%ASSETS%\blurred
set VIDEOS=%ROOT%\brand\from-rima
set FRAMES=%ASSETS%\frames-raw
set SELECTED=%ASSETS%\selected
set FINAL=%ASSETS%\images

echo.
echo === STEP 1: Blur faces on 5 gallery source images (PROTECT RIMA) ===
set RIMA_PORTRAIT=%ROOT%\brand\from-rima\אתר המופלא של סיפורימה-20260418T175307Z-3-001\תמונות ועוד\Screenshot_20240718_131943_WhatsApp.jpg
"%PY%" "%SCRIPTS%\blur_faces.py" "%SRC_IMG%" "%BLURRED%" --pixel-size 20 --margin 0.25 --rima-portrait "%RIMA_PORTRAIT%" --zones "%SCRIPTS%\rima_zones.json"

echo.
echo === STEP 2: Extract frames (25%%, 50%%, 75%%) from all videos ===
"%PY%" "%SCRIPTS%\extract_frames.py" "%VIDEOS%" "%FRAMES%" --ffmpeg "C:\ffmpeg\bin\ffmpeg.exe" --ffprobe "C:\ffmpeg\bin\ffprobe.exe"

echo.
echo === STEP 3 (MANUAL): Review %FRAMES% and copy 3-4 best frames
echo      (Rima solo, children from behind, no faces) to %SELECTED%
echo      Rename to: gallery-frame-1.jpg, gallery-frame-2.jpg, etc.
echo      Then re-run this script from STEP 4.
if not exist "%SELECTED%" (
  echo      [SKIP STEP 4] %SELECTED% not yet prepared.
  goto :END
)

echo.
echo === STEP 4: Build final responsive set (480/768/1200 webp+jpg) ===
"%PY%" "%SCRIPTS%\make_responsive.py" "%SELECTED%" "%FINAL%"

:END
echo.
echo === Pipeline complete ===
endlocal
