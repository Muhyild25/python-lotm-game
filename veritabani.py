import sqlite3
import json

def veritabani_kur():
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    # YENİ: hikaye_adim ve gunluk_sayfasi sütunları eklendi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kayitlar (
            isim TEXT PRIMARY KEY,
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

# YENİ: Artık hikaye objesini de parametre olarak alıyoruz
def oyunu_kaydet(oyuncu, hikaye):
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    
    envanter_isimleri = [esya.isim for esya in oyuncu.envanter]
    envanter_json = json.dumps(envanter_isimleri)
    
    cursor.execute('''
        INSERT OR REPLACE INTO kayitlar (isim, sequence, hp, sanity, pound, envanter, hikaye_adim, gunluk_sayfasi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (oyuncu.isim, oyuncu.sequence, oyuncu.hp, oyuncu.sanity, oyuncu.pound, envanter_json, hikaye.adim, hikaye.gunluk_sayfasi))
    
    conn.commit()
    conn.close()
    print("\n💾 Oyun durumu, envanter ve HİKAYE başarıyla kaydedildi!")

# YENİ: Yüklerken hikaye objesini de güncelliyoruz
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
                        
        # Hikaye ilerlemesini geri yüklüyoruz
        hikaye.adim = kayit[5]
        hikaye.gunluk_sayfasi = kayit[6]

        print(f"\n📂 Eski kayıt bulundu! {oyuncu.isim}, hikayeye kaldığı yerden devam ediyor...")
        return True
    else:
        print("\n🆕 Eski kayıt bulunamadı. Yeni bir maceraya başlanıyor...")
        return False