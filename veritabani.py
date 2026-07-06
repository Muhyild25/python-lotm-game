import sqlite3
import json

def veritabani_kur():
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    # YENİ: 'pathway TEXT' sütunu eklendi!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kayitlar (
            isim TEXT PRIMARY KEY,
            pathway TEXT,
            sequence INTEGER,
            hp INTEGER,
            sanity INTEGER,
            pound INTEGER,
            envanter TEXT,
            hikaye_adim INTEGER,
            gunluk_sayfasi INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# YENİ FONKSİYON: Karakteri yaratmadan önce veri tabanına bakıp yolunu öğreniyor
def kayitli_yol_bul(isim):
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT pathway FROM kayitlar WHERE isim = ?', (isim,))
        kayit = cursor.fetchone()
        conn.close()
        return kayit[0] if kayit else None
    except:
        return None

def oyunu_kaydet(oyuncu, hikaye):
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    envanter_isimleri = [esya.isim for esya in oyuncu.envanter]
    envanter_json = json.dumps(envanter_isimleri)
    
    # Pathway bilgisini de veri tabanına gönderiyoruz
    cursor.execute('''
        INSERT OR REPLACE INTO kayitlar (isim, pathway, sequence, hp, sanity, pound, envanter, hikaye_adim, gunluk_sayfasi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (oyuncu.isim, oyuncu.pathway, oyuncu.sequence, oyuncu.hp, oyuncu.sanity, oyuncu.pound, envanter_json, hikaye.adim, hikaye.gunluk_sayfasi))
    
    conn.commit()
    conn.close()
    print("\n💾 Oyun durumu, envanter ve HİKAYE başarıyla kaydedildi!")

def kayit_yukle(oyuncu, tum_esyalar, hikaye):
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    cursor.execute('SELECT sequence, hp, sanity, pound, envanter, hikaye_adim, gunluk_sayfasi FROM kayitlar WHERE isim = ?', (oyuncu.isim,))
    kayit = cursor.fetchone()
    conn.close()
    
    if kayit:
        oyuncu.sequence = kayit[0]
        oyuncu.hp = kayit[1]
        oyuncu.sanity = kayit[2]
        oyuncu.pound = kayit[3]
        if kayit[4]:
            kayitli_isimler = json.loads(kayit[4])
            oyuncu.envanter = []
            for isim in kayitli_isimler:
                for ornek_esya in tum_esyalar:
                    if ornek_esya.isim == isim:
                        oyuncu.envanter.append(ornek_esya)
                        break
        hikaye.adim = kayit[5]
        hikaye.gunluk_sayfasi = kayit[6]
        print(f"\n📂 Eski kayıt bulundu! {oyuncu.isim} ({oyuncu.pathway} Sınıfı), hikayeye kaldığı yerden devam ediyor...")
        return True
    else:
        return False