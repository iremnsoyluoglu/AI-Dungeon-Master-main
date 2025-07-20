#!/usr/bin/env python3
"""
AI Dungeon Master - Test Script
===============================

Bu script uygulamayı test etmek için kullanılır.
"""

import requests
import time
import webbrowser
import subprocess
import sys
import os

def test_api_endpoints():
    """API endpoint'lerini test et"""
    base_url = "http://localhost:5050"
    
    print("🧪 API Testleri Başlıyor...")
    print("=" * 50)
    
    # Health check test
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']} | Version: {data['version']}")
        else:
            print(f"❌ Health Check: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check Hatası: {e}")
        return False
    
    # Campaigns test
    try:
        response = requests.get(f"{base_url}/api/campaigns", timeout=5)
        if response.status_code == 200:
            data = response.json()
            campaigns = data.get('campaigns', [])
            print(f"✅ Campaigns API: {len(campaigns)} kampanya yüklendi")
            for campaign in campaigns[:3]:  # İlk 3'ünü göster
                print(f"   - {campaign['name']} ({campaign['id']})")
        else:
            print(f"❌ Campaigns API: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Campaigns API Hatası: {e}")
        return False
    
    # Dice roll test
    try:
        response = requests.post(f"{base_url}/api/game/roll-dice", 
                               json={"dice_type": "d20", "modifier": 0},
                               timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dice Roll: {data['dice_type']}+{data['modifier']} = {data['result']}")
        else:
            print(f"❌ Dice Roll: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Dice Roll Hatası: {e}")
    
    print("=" * 50)
    return True

def start_server():
    """Sunucuyu başlat"""
    print("🚀 Sunucu Başlatılıyor...")
    
    # Sunucu zaten çalışıyor mu kontrol et
    try:
        response = requests.get("http://localhost:5050/api/health", timeout=2)
        if response.status_code == 200:
            print("✅ Sunucu zaten çalışıyor!")
            return True
    except:
        pass
    
    # Sunucuyu başlat
    try:
        # Python script'ini başlat
        script_path = os.path.join("src", "main.py")
        if os.path.exists(script_path):
            print(f"📁 Script bulundu: {script_path}")
            
            # Background'da başlat
            process = subprocess.Popen([sys.executable, script_path], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # Sunucunun başlamasını bekle
            print("⏳ Sunucu başlatılıyor, lütfen bekleyin...")
            time.sleep(3)
            
            # Sunucu çalışıyor mu kontrol et
            for i in range(10):
                try:
                    response = requests.get("http://localhost:5050/api/health", timeout=2)
                    if response.status_code == 200:
                        print("✅ Sunucu başarıyla başlatıldı!")
                        return True
                except:
                    pass
                time.sleep(1)
            
            print("❌ Sunucu başlatılamadı!")
            return False
            
        else:
            print(f"❌ Script bulunamadı: {script_path}")
            return False
            
    except Exception as e:
        print(f"❌ Sunucu başlatma hatası: {e}")
        return False

def open_browser():
    """Tarayıcıyı aç"""
    url = "http://localhost:5050"
    print(f"🌐 Tarayıcı açılıyor: {url}")
    
    try:
        webbrowser.open(url)
        print("✅ Tarayıcı açıldı!")
        return True
    except Exception as e:
        print(f"❌ Tarayıcı açma hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🧙‍♂️ AI Dungeon Master - Test Script")
    print("=" * 50)
    
    # 1. Sunucuyu başlat
    if not start_server():
        print("❌ Test başarısız: Sunucu başlatılamadı")
        return
    
    # 2. API testleri
    if not test_api_endpoints():
        print("❌ Test başarısız: API endpoint'leri çalışmıyor")
        return
    
    # 3. Tarayıcıyı aç
    open_browser()
    
    print("\n🎉 Test tamamlandı!")
    print("📝 Manuel test için:")
    print("   1. Tarayıcıda http://localhost:5050 adresine gidin")
    print("   2. 'Oyunu Başlat' butonuna tıklayın")
    print("   3. Karakter oluşturun")
    print("   4. Seçim butonlarını test edin")
    
    print("\n🛑 Sunucuyu durdurmak için Ctrl+C tuşlayın")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Test sonlandırıldı")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}") 