# AI Dungeon Master - PowerShell Başlatıcı
# ========================================

Write-Host "🚀 AI Dungeon Master Başlatılıyor..." -ForegroundColor Green
Write-Host ""

Write-Host "📦 Bağımlılıklar kontrol ediliyor..." -ForegroundColor Yellow
npm install

Write-Host ""
Write-Host "🔧 Backend sunucusu başlatılıyor (Port 5009)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "node server.js" -WindowStyle Normal

Write-Host ""
Write-Host "⏳ Backend'in başlaması için 3 saniye bekleniyor..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "🎮 Frontend sunucusu başlatılıyor (Port 3001)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "✅ Sistem başlatıldı!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:3001" -ForegroundColor White
Write-Host "🔧 Backend API: http://localhost:5009" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tarayıcıda http://localhost:3001 adresini açın" -ForegroundColor Yellow
Write-Host ""

Read-Host "Devam etmek için Enter'a basın" 