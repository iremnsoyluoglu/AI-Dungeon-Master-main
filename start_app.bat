@echo off
chcp 65001 >nul
title AI Dungeon Master - Başlatıcı

echo.
echo 🧙‍♂️ AI Dungeon Master - Başlatıcı
echo =================================
echo.

:: Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python'u yükleyin.
    pause
    exit /b 1
)

:: Gerekli dosyaları kontrol et
if not exist "src\main.py" (
    echo ❌ src\main.py dosyası bulunamadı!
    pause
    exit /b 1
)

:: Sunucu zaten çalışıyor mu kontrol et
echo 🔍 Sunucu durumu kontrol ediliyor...
curl -s http://localhost:5050/api/health >nul 2>&1
if not errorlevel 1 (
    echo ✅ Sunucu zaten çalışıyor!
    goto :open_browser
)

:: Sunucuyu başlat
echo 🚀 Sunucu başlatılıyor...
echo.
python src\main.py

:open_browser
echo.
echo 🌐 Tarayıcı açılıyor...
start http://localhost:5050

echo.
echo ✅ Uygulama başlatıldı!
echo 📝 Adres: http://localhost:5050
echo.
echo 🛑 Sunucuyu durdurmak için bu pencereyi kapatın
pause 