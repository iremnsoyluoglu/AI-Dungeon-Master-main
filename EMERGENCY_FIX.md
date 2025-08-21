# 🚨 ACİL DURUM - OYUNU GERİ GETİR

## Sorun
Vercel'de SSO (Single Sign-On) etkinleştirilmiş ve oyuna erişim engelleniyor.

## Hızlı Çözüm (5 Dakika)

### 1. Vercel Dashboard'a Gidin
- https://vercel.com/dashboard adresine gidin
- Giriş yapın

### 2. Projenizi Bulun
- `ai-dungeon-master-main` projesini bulun
- Projeye tıklayın

### 3. Settings Sekmesine Gidin
- Üst menüde "Settings" sekmesine tıklayın

### 4. Authentication Bölümünü Bulun
- Sol menüde "Authentication" veya "SSO" bölümünü bulun
- Eğer göremiyorsanız "Security" veya "Access Control" bölümüne bakın

### 5. SSO'yu Kapatın
- "Enable SSO" veya "Authentication Required" toggle'ını bulun
- **KAPATIN** (OFF yapın)
- "Save" butonuna tıklayın

### 6. Yeniden Deploy Edin
- "Deployments" sekmesine gidin
- En son deployment'da "Redeploy" butonuna tıklayın

## Alternatif Çözüm

Eğer yukarıdaki adımlar çalışmazsa:

1. **Yeni Proje Oluşturun:**
   - Dashboard'da "New Project" butonuna tıklayın
   - GitHub'dan `ai-dungeon-master-main` repository'sini seçin
   - Proje adı: `ai-dungeon-master-fixed`
   - Deploy edin

2. **Yeni URL'yi Kullanın:**
   - Yeni proje size farklı bir URL verecek
   - Bu URL SSO olmadan çalışacak

## Oyun Özellikleri (Geri Geldiğinde)

✅ **4 Tam Senaryo:**
- 🐉 Dragon Hunter Path (Fantasy)
- 🌳 Magical Forest Mysteries (Fantasy)
- 🏙️ Hive City Defense (Sci-Fi)
- 🌃 Cyberpunk City Secrets (Cyberpunk)

✅ **NPC Etkileşimleri**
✅ **Savaş Sistemi**
✅ **Karakter Gelişimi**
✅ **Hikaye Dallanması**
✅ **Plot Twist'ler**

## Test Etmek İçin

Düzeltme sonrası:
```bash
python check_deployment_status.py
```

**OYUN TAMAMEN ÇALIŞIYOR - SADECE SSO SORUNU VAR!**
