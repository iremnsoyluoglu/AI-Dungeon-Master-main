@echo off
echo 🚀 AI Dungeon Master Başlatılıyor...
echo.

echo 📦 Bağımlılıklar kontrol ediliyor...
npm install

echo.
echo 🔧 Backend sunucusu başlatılıyor (Port 5009)...
start "Backend Server" cmd /k "node server.js"

echo.
echo ⏳ Backend'in başlaması için 3 saniye bekleniyor...
timeout /t 3 /nobreak > nul

echo.
echo 🎮 Frontend sunucusu başlatılıyor (Port 3001)...
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ✅ Sistem başlatıldı!
echo 📱 Frontend: http://localhost:3001
echo 🔧 Backend API: http://localhost:5009
echo.
echo 💡 Tarayıcıda http://localhost:3001 adresini açın
echo.
pause 