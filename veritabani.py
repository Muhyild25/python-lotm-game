import sqlite3
import json

def veritabani_kur():
    """
    Veritabanı şemasını başlatır.
    Oyun durumu, karakter istatistikleri ve hikaye ilerlemesini kalıcı olarak 
    saklamak (Data Persistence) için gerekli tablo yoksa oluşturulur.
    """
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    
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

def kayitli_yol_bul(isim):
    """
    Karakterin Pathway (sınıf) bilgisini veritabanından sorgular.
    Polymorphism yapısında doğru alt sınıfın (Sleepless, Seer vb.) 
    örneklendirilmesi (Instantiation) için veritabanından ön okuma yapar.
    """
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT pathway FROM kayitlar WHERE isim = ?', (isim,))
        kayit = cursor.fetchone()
        conn.close()
        return kayit[0] if kayit else None
    except sqlite3.Error:
        # Veritabanı okuma hatalarında sistemin çökmesini engeller
        return None

def oyunu_kaydet(oyuncu, hikaye):
    """
    Oyunun mevcut durumunu (State) SQLite veritabanına serileştirerek kaydeder.
    Envanter listesi, ilişkisel veritabanı mimarisine uyum sağlamak amacıyla JSON formatına dönüştürülür.
    """
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    
    # Envanter objeleri veri kalıcılığı için JSON formatında serileştirilir (Serialization).
    envanter_isimleri = [esya if isinstance(esya, str) else esya.isim for esya in oyuncu.envanter]
    envanter_json = json.dumps(envanter_isimleri)
    
    cursor.execute('''
        INSERT OR REPLACE INTO kayitlar (isim, pathway, sequence, hp, sanity, pound, envanter, hikaye_adim, gunluk_sayfasi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (oyuncu.isim, oyuncu.pathway, oyuncu.sequence, oyuncu.hp, oyuncu.sanity, oyuncu.pound, envanter_json, hikaye.adim, hikaye.gunluk_sayfasi))
    
    conn.commit()
    conn.close()
    
    # Konsol loglaması (GUI arayüzünde çalışırken terminalde işlem takibi sağlar)
    print("\n[DB_SYS] State serileştirme işlemi tamamlandı ve veritabanına işlendi.")

def kayit_yukle(oyuncu, tum_esyalar, hikaye):
    """
    Kalıcı depolama alanından (Persistent Storage) oyun durumunu okur ve 
    bellekteki (Memory) nesnelere çözümleyerek (Deserialization) aktarır.
    """
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
        
        # JSON stringi çözümlenerek bellek objelerine (Envanter listesi) dönüştürülür.
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
        
        print(f"\n[DB_SYS] State başarıyla deserialize edildi: {oyuncu.isim} ({oyuncu.pathway} Sınıfı).")
        return True
    else:
        return False