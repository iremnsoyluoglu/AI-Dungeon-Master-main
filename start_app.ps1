# AI Dungeon Master - PowerShell Başlatıcı
# ========================================

Write-Host "🧙‍♂️ AI Dungeon Master - Başlatıcı" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Python kontrolü
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python bulundu: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python bulunamadı! Lütfen Python'u yükleyin." -ForegroundColor Red
    Read-Host "Devam etmek için Enter tuşlayın"
    exit 1
}

# Gerekli dosyaları kontrol et
if (-not (Test-Path "src\main.py")) {
    Write-Host "❌ src\main.py dosyası bulunamadı!" -ForegroundColor Red
    Read-Host "Devam etmek için Enter tuşlayın"
    exit 1
}

# Sunucu zaten çalışıyor mu kontrol et
Write-Host "🔍 Sunucu durumu kontrol ediliyor..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5050/api/health" -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Sunucu zaten çalışıyor!" -ForegroundColor Green
        $serverRunning = $true
    }
} catch {
    $serverRunning = $false
}

# Sunucu çalışmıyorsa başlat
if (-not $serverRunning) {
    Write-Host "🚀 Sunucu başlatılıyor..." -ForegroundColor Yellow
    Write-Host ""
    
    # Sunucuyu background'da başlat
    $process = Start-Process -FilePath "python" -ArgumentList "src\main.py" -PassThru -WindowStyle Hidden
    
    # Sunucunun başlamasını bekle
    Write-Host "⏳ Sunucu başlatılıyor, lütfen bekleyin..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    
    # Sunucu çalışıyor mu kontrol et
    $maxAttempts = 10
    $attempt = 0
    $serverReady = $false
    
    while ($attempt -lt $maxAttempts -and -not $serverReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:5050/api/health" -TimeoutSec 2 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                $serverReady = $true
                Write-Host "✅ Sunucu başarıyla başlatıldı!" -ForegroundColor Green
            }
        } catch {
            $attempt++
            Start-Sleep -Seconds 1
        }
    }
    
    if (-not $serverReady) {
        Write-Host "❌ Sunucu başlatılamadı!" -ForegroundColor Red
        Read-Host "Devam etmek için Enter tuşlayın"
        exit 1
    }
}

# Tarayıcıyı aç
Write-Host ""
Write-Host "🌐 Tarayıcı açılıyor..." -ForegroundColor Yellow
try {
    Start-Process "http://localhost:5050"
    Write-Host "✅ Tarayıcı açıldı!" -ForegroundColor Green
} catch {
    Write-Host "❌ Tarayıcı açma hatası!" -ForegroundColor Red
}

Write-Host ""
Write-Host "✅ Uygulama başlatıldı!" -ForegroundColor Green
Write-Host "📝 Adres: http://localhost:5050" -ForegroundColor Cyan
Write-Host ""
Write-Host "🧪 Test için:" -ForegroundColor Yellow
Write-Host "   1. 'Oyunu Başlat' butonuna tıklayın" -ForegroundColor White
Write-Host "   2. Karakter oluşturun" -ForegroundColor White
Write-Host "   3. Seçim butonlarını test edin" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Sunucuyu durdurmak için Ctrl+C tuşlayın" -ForegroundColor Red

# Sürekli çalışması için bekle
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} catch {
    Write-Host ""
    Write-Host "👋 Uygulama sonlandırıldı" -ForegroundColor Yellow
} 