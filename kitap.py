import json
import os
from datetime import datetime

# Dosya adı
DOSYA_ADI = "kitaplar.json"

# Türler listesi
TURLER = [
    "Kurgu",
    "Tarih",
    "Bilim",
    "Fantezi",
    "Bilim Kurgu",
    "Kişisel Gelişim",
    "Diğer"
]

def kitaplari_yukle():
    """
    Dosyadan kitapları yükler.
    Dosya yoksa boş liste döndürür.
    """
    if os.path.exists(DOSYA_ADI):
        try:
            with open(DOSYA_ADI, 'r', encoding='utf-8') as dosya:
                kitaplar = json.load(dosya)
                return kitaplar
        except (json.JSONDecodeError, IOError) as hata:
            print("Uyarı: Dosya okunurken hata oluştu: " + str(hata))
            print("Yeni bir liste oluşturuldu.\n")
            return []
    else:
        return []


def kitaplari_kaydet(kitaplar):
    """
    Kitapları JSON dosyasına kaydeder.
    """
    try:
        with open(DOSYA_ADI, 'w', encoding='utf-8') as dosya:
            json.dump(kitaplar, dosya, ensure_ascii=False, indent=2)
        print("Kitaplar başarıyla kaydedildi.")
    except IOError as hata:
        print("Uyarı: Dosya kaydedilirken hata oluştu: " + str(hata))


def ana_menu():
    """
    Ana menüyü gösterir ve kullanıcıdan seçim alır.
    """
    print("\n" + "="*50)
    print("--- KİTAP TAKİP UYGULAMASI ---")
    print("="*50)
    print("1. Kitapları Listele")
    print("2. Yeni Kitap Ekle")
    print("3. Okundu/Okunmadı İşaretle")
    print("4. Kitap Sil")
    print("5. Kitap Ara")
    print("6. Kitapları Sırala")
    print("7. Okunmamış Kitapları Göster")
    print("8. Okunan Kitapları Göster")
    print("9. Kitaba Puan Ver")
    print("10. İstatistikleri Göster")
    print("11. Çıkış")
    print("="*50)
    
    secim = input("Seçiminiz (1-11): ").strip()
    return secim


def kitaplari_listele(kitaplar):
    """
    Kitapları numaralandırılmış olarak ve durumuyla listeler.
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.\n")
        return
    
    print("\n" + "-"*70)
    print("--- KİTAP LİSTESİ ---")
    print("-"*70)
    
    for i, kitap in enumerate(kitaplar, 1):
        durum = "okundu" if kitap.get("okundu", False) else "okunmadı"
        tur = kitap.get("tur", "Diğer")
        puan = kitap.get("puan", 0)
        puan_goster = str(puan) + "/5" if puan > 0 else "-"
        
        print(f"{i}. {kitap['baslik']} — {kitap['yazar']}")
        print(f"   Tür: {tur} | Durum: [{durum}] | Puan: {puan_goster}")
    
    print("-"*70 + "\n")


def kitap_ekle(kitaplar):
    """
    Kullanıcıdan başlık ve yazar bilgisini alarak yeni kitap ekler.
    """
    print("\n" + "-"*50)
    baslik = input("Kitap başlığı: ").strip()
    
    if not baslik:
        print("Başlık boş olamaz!\n")
        return
    
    yazar = input("Yazar: ").strip()
    
    if not yazar:
        print("Yazar boş olamaz!\n")
        return
    
    print("\nKitap Türü Seçin:")
    for i, tur in enumerate(TURLER, 1):
        print(f"{i}. {tur}")
    
    tur_secim = input("Türü seçin (1-7): ").strip()
    
    try:
        tur_no = int(tur_secim)
        if 1 <= tur_no <= len(TURLER):
            secilen_tur = TURLER[tur_no - 1]
        else:
            secilen_tur = "Diğer"
    except ValueError:
        secilen_tur = "Diğer"
    
    # Yeni kitap sözlüğü oluştur
    yeni_kitap = {
        "baslik": baslik,
        "yazar": yazar,
        "okundu": False,
        "tur": secilen_tur,
        "puan": 0,
        "ekleme_tarihi": datetime.now().strftime("%d.%m.%Y %H:%M")
    }
    
    kitaplar.append(yeni_kitap)
    print(f"'{baslik}' ({secilen_tur}) eklendi.")
    print("-"*50 + "\n")
    kitaplari_kaydet(kitaplar)


def durum_degistir(kitaplar):
    """
    Kitap numarasına göre seçilip durumu (okundu/okunmadı) değiştirir.
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.\n")
        return
    
    kitaplari_listele(kitaplar)
    
    print("-"*50)
    try:
        numara_str = input("Durumunu değiştirmek istediğiniz kitabın numarası: ").strip()
        
        if not numara_str.isdigit():
            print("Lütfen bir sayı girin!\n")
            return
        
        numara = int(numara_str)
        
        if numara < 1 or numara > len(kitaplar):
            print("Geçersiz kitap numarası!\n")
            return
        
        # Durum değiştir
        kitap = kitaplar[numara - 1]
        kitap["okundu"] = not kitap["okundu"]
        durum = "okundu" if kitap["okundu"] else "okunmadı"
        
        print(f"'{kitap['baslik']}' artık [{durum}] olarak işaretlendi.")
        print("-"*50 + "\n")
        kitaplari_kaydet(kitaplar)
        
    except ValueError:
        print("Lütfen bir sayı girin!\n")


def kitap_sil(kitaplar):
    """
    Kitap numarasına göre kitabı siler.
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.\n")
        return
    
    kitaplari_listele(kitaplar)
    
    print("-"*50)
    try:
        numara_str = input("Silmek istediğiniz kitabın numarası: ").strip()
        
        if not numara_str.isdigit():
            print("Lütfen bir sayı girin!\n")
            return
        
        numara = int(numara_str)
        
        if numara < 1 or numara > len(kitaplar):
            print("Geçersiz kitap numarası!\n")
            return
        
        # Kitabı sil
        silinen_kitap = kitaplar.pop(numara - 1)
        print(f"'{silinen_kitap['baslik']}' silindi.")
        print("-"*50 + "\n")
        kitaplari_kaydet(kitaplar)
        
    except ValueError:
        print("Lütfen bir sayı girin!\n")


def kitap_ara(kitaplar):
    """
    Başlık veya yazara göre kitap arar.
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.\n")
        return
    
    arama_terimi = input("\nAranan kitap adı veya yazar: ").strip().lower()
    
    if not arama_terimi:
        print("Arama terimi boş olamaz!\n")
        return
    
    sonuclar = []
    for i, kitap in enumerate(kitaplar):
        if (arama_terimi in kitap['baslik'].lower() or 
            arama_terimi in kitap['yazar'].lower()):
            sonuclar.append((i, kitap))
    
    if not sonuclar:
        print(f"\n'{arama_terimi}' ile ilgili kitap bulunamadı.\n")
        return
    
    print(f"\n{len(sonuclar)} sonuç bulundu:\n")
    print("-"*70)
    
    for idx, (kitap_no, kitap) in enumerate(sonuclar, 1):
        durum = "okundu" if kitap.get("okundu", False) else "okunmadı"
        tur = kitap.get("tur", "Diğer")
        puan = kitap.get("puan", 0)
        puan_goster = str(puan) + "/5" if puan > 0 else "-"
        
        print(f"{idx}. {kitap['baslik']} — {kitap['yazar']}")
        print(f"   Tür: {tur} | Durum: [{durum}] | Puan: {puan_goster}")
    
    print("-"*70 + "\n")


def kitaplari_sirala(kitaplar):
    """
    Kitapları başlık veya yazara göre sıralar.
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.\n")
        return
    
    print("\n--- SIRALAMA SEÇENEKLERİ ---")
    print("1. Başlığa göre (A-Z)")
    print("2. Yazara göre (A-Z)")
    print("3. Son eklenenler")
    print("4. En yüksek puana göre")
    
    secim = input("Seçiminiz (1-4): ").strip()
    
    if secim == "1":
        kitaplar_siralanmis = sorted(kitaplar, key=lambda x: x['baslik'].lower())
        baslik = "BAŞLIĞA GÖRE SIRALI"
    elif secim == "2":
        kitaplar_siralanmis = sorted(kitaplar, key=lambda x: x['yazar'].lower())
        baslik = "YAZARA GÖRE SIRALI"
    elif secim == "3":
        kitaplar_siralanmis = list(reversed(kitaplar))
        baslik = "SON EKLENENLER"
    elif secim == "4":
        kitaplar_siralanmis = sorted(kitaplar, key=lambda x: x.get("puan", 0), reverse=True)
        baslik = "EN YÜKSEK PUANA GÖRE"
    else:
        print("Geçersiz seçim!\n")
        return
    
    print("\n" + "-"*70)
    print(f"--- KİTAP LİSTESİ ({baslik}) ---")
    print("-"*70)
    
    for i, kitap in enumerate(kitaplar_siralanmis, 1):
        durum = "okundu" if kitap.get("okundu", False) else "okunmadı"
        tur = kitap.get("tur", "Diğer")
        puan = kitap.get("puan", 0)
        puan_goster = str(puan) + "/5" if puan > 0 else "-"
        
        print(f"{i}. {kitap['baslik']} — {kitap['yazar']}")
        print(f"   Tür: {tur} | Durum: [{durum}] | Puan: {puan_goster}")
    
    print("-"*70 + "\n")


def okunmamis_kitaplari_goster(kitaplar):
    """
    Sadece okunmamış kitapları listeler.
    """
    okunmamis = [k for k in kitaplar if not k.get("okundu", False)]
    
    if not okunmamis:
        print("\nTebrikler! Tüm kitapları okudunuz!\n")
        return
    
    print("\n" + "-"*70)
    print("--- OKUNMAMIS KİTAPLAR ---")
    print(f"Toplam: {len(okunmamis)} kitap")
    print("-"*70)
    
    for i, kitap in enumerate(okunmamis, 1):
        tur = kitap.get("tur", "Diğer")
        puan = kitap.get("puan", 0)
        puan_goster = str(puan) + "/5" if puan > 0 else "-"
        
        print(f"{i}. {kitap['baslik']} — {kitap['yazar']}")
        print(f"   Tür: {tur} | Puan: {puan_goster}")
    
    print("-"*70 + "\n")


def okunan_kitaplari_goster(kitaplar):
    """
    Sadece okunan kitapları listeler.
    """
    okunan = [k for k in kitaplar if k.get("okundu", False)]
    
    if not okunan:
        print("\nHenüz hiçbir kitap okunmadı.\n")
        return
    
    print("\n" + "-"*70)
    print("--- OKUNAN KİTAPLAR ---")
    print(f"Toplam: {len(okunan)} kitap")
    print("-"*70)
    
    for i, kitap in enumerate(okunan, 1):
        tur = kitap.get("tur", "Diğer")
        puan = kitap.get("puan", 0)
        puan_goster = str(puan) + "/5" if puan > 0 else "-"
        
        print(f"{i}. {kitap['baslik']} — {kitap['yazar']}")
        print(f"   Tür: {tur} | Puan: {puan_goster}")
    
    print("-"*70 + "\n")


def kitap_puanla(kitaplar):
    """
    Kitaba puan verir (1-5).
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.\n")
        return
    
    kitaplari_listele(kitaplar)
    
    try:
        numara_str = input("Puanlamak istediğiniz kitabın numarası: ").strip()
        
        if not numara_str.isdigit():
            print("Lütfen bir sayı girin!\n")
            return
        
        numara = int(numara_str)
        
        if numara < 1 or numara > len(kitaplar):
            print("Geçersiz kitap numarası!\n")
            return
        
        print("Puan girin (1-5):")
        puan_str = input("Puanınız: ").strip()
        
        if not puan_str.isdigit():
            print("Lütfen bir sayı girin!\n")
            return
        
        puan = int(puan_str)
        
        if puan < 1 or puan > 5:
            print("Puan 1-5 arası olmalı!\n")
            return
        
        kitap = kitaplar[numara - 1]
        kitap["puan"] = puan
        
        print(f"'{kitap['baslik']}' kitabı {puan}/5 puan ile puanlandı.")
        print("-"*50 + "\n")
        kitaplari_kaydet(kitaplar)
        
    except ValueError:
        print("Lütfen bir sayı girin!\n")


def istatistikleri_goster(kitaplar):
    """
    Kitap koleksiyonu hakkında istatistikler gösterir.
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.\n")
        return
    
    toplam_kitap = len(kitaplar)
    okunan = sum(1 for k in kitaplar if k.get("okundu", False))
    okunmamis = toplam_kitap - okunan
    toplam_puan = sum(k.get("puan", 0) for k in kitaplar)
    ortalama_puan = toplam_puan / toplam_kitap if toplam_kitap > 0 else 0
    
    # Tür istatistikleri
    tur_sayilari = {}
    for kitap in kitaplar:
        tur = kitap.get("tur", "Diğer")
        tur_sayilari[tur] = tur_sayilari.get(tur, 0) + 1
    
    print("\n" + "="*70)
    print("--- KÜTÜPHANENİZ İSTATİSTİKLERİ ---")
    print("="*70)
    print(f"Toplam Kitap:        {toplam_kitap}")
    print(f"Okunan Kitap:        {okunan} ({okunan*100//toplam_kitap}%)")
    print(f"Okunmamış Kitap:     {okunmamis} ({okunmamis*100//toplam_kitap}%)")
    print(f"Ortalama Puan:       {ortalama_puan:.1f}/5.0")
    
    print("\nKitap Türü Dağılımı:")
    for tur, sayi in sorted(tur_sayilari.items()):
        yuzde = (sayi * 100) // toplam_kitap
        print(f"  {tur}: {sayi} ({yuzde}%)")
    
    print("="*70 + "\n")


def gecersiz_secim():
    """
    Geçersiz seçim yapıldığında hata mesajı gösterir.
    """
    print("Geçersiz seçim! Lütfen 1-11 arası bir değer girin.\n")


def main():
    """
    Ana program döngüsü.
    """
    # Başlangıç mesajı
    print("\n" + "="*50)
    print("Kitap Takip Uygulamasına Hoş Geldiniz!")
    print("="*50)
    
    # Kitapları yükle
    kitaplar = kitaplari_yukle()
    
    if os.path.exists(DOSYA_ADI) and kitaplar:
        print("Kitaplar başarıyla yüklendi.")
    elif os.path.exists(DOSYA_ADI):
        print("Dosya mevcut ancak boş.")
    else:
        print("Kayıt dosyası bulunamadı. Yeni bir liste oluşturuldu.")
    
    print("="*50 + "\n")
    
    # Ana döngü
    while True:
        secim = ana_menu()
        
        if secim == "1":
            kitaplari_listele(kitaplar)
        elif secim == "2":
            kitap_ekle(kitaplar)
        elif secim == "3":
            durum_degistir(kitaplar)
        elif secim == "4":
            kitap_sil(kitaplar)
        elif secim == "5":
            kitap_ara(kitaplar)
        elif secim == "6":
            kitaplari_sirala(kitaplar)
        elif secim == "7":
            okunmamis_kitaplari_goster(kitaplar)
        elif secim == "8":
            okunan_kitaplari_goster(kitaplar)
        elif secim == "9":
            kitap_puanla(kitaplar)
        elif secim == "10":
            istatistikleri_goster(kitaplar)
        elif secim == "11":
            print("\nProgramdan çıkılıyor...\n")
            break
        else:
            gecersiz_secim()


if __name__ == "__main__":
    main()
