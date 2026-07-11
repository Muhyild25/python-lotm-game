import sys
import random
import sqlite3 
import os 

from karakter import Sleepless, Seer, Assassin 
try:
    from yapay_zeka import YZMotoru
    YZ_AKTIF = True
except ImportError:
    YZ_AKTIF = False
    print("[SYS_WARN] yapay_zeka.py modülü bulunamadı, AI Fallback sistemi devrede.")

from savas_arayuzu import SavasPenceresi

from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QTextEdit, QPushButton, QFrame,
                             QMessageBox, QInputDialog, QStackedWidget, QLineEdit, QComboBox, QDialog)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect

def veritabani_hazirla():
    """
    Yerel SQLite veritabanı (Local Storage) başlatma fonksiyonu.
    Uygulama yaşam döngüsü öncesi şema doğrulamasını (Schema Validation) gerçekleştirir.
    """
    conn = sqlite3.connect('lotm_save.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kayitlar (
                        isim TEXT PRIMARY KEY, 
                        pathway TEXT, 
                        hp INTEGER, 
                        sanity INTEGER,
                        pound INTEGER, 
                        sequence INTEGER, 
                        envanter TEXT)''')
    conn.commit()
    conn.close()


class BossSavasPenceresi(QDialog):
    """
    Final Boss karşılaşmasını yöneten Modal Dialog sınıfı.
    Normal savaşlardan (SavasPenceresi) farklı olarak kaçış mekanizması (Flee) devre dışı bırakılmış 
    ve hikaye eşyalarına (Quest Items) bağlı dinamik zorluk ölçeklendirmesi (Difficulty Scaling) eklenmiştir.
    """
    def __init__(self, oyuncu, ebeveyn):
        super().__init__(ebeveyn)
        self.pencere = ebeveyn.pencere
        self.setWindowTitle("FİNAL SAVAŞI: Yozlaşmış Megose")
        self.setFixedSize(550, 450)
        self.setStyleSheet("background-color: #1a0000; color: #ffcccc; font-family: 'Consolas';")
        self.oyuncu = oyuncu
        self.sonuc = None

        # State Dependency: Boss stat'ları envanterdeki spesifik quest-item varlığına göre manipüle edilir.
        self.tilsim_var_mi = "Güneş Tılsımı" in self.oyuncu.envanter
        
        if self.tilsim_var_mi:
            self.boss_hp = 150
            self.boss_hasar_min = 15
            self.boss_hasar_max = 30
        else:
            # Hard-Enrage State: Gerekli eşya yoksa hayatta kalma ihtimali sıfırlanır.
            self.boss_hp = 999
            self.boss_hasar_min = 80
            self.boss_hasar_max = 150

        self.duzen = QVBoxLayout(self)
        
        # UI Layout: Boss HP & Karakter Durumu
        self.lbl_baslik = QLabel("⚠️ MEGOSE (Gerçek Yaratıcı'nın Tohumu) ⚠️")
        self.lbl_baslik.setStyleSheet("font-size: 20px; color: #ff0000; font-weight: bold;")
        self.lbl_baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.duzen.addWidget(self.lbl_baslik)

        self.lbl_durum = QLabel(f"Megose HP: {self.boss_hp}\nSenin HP: {self.oyuncu.hp} | Akıl Sağlığın: {self.oyuncu.sanity}")
        self.lbl_durum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_durum.setStyleSheet("font-size: 16px; color: #ffffff;")
        self.duzen.addWidget(self.lbl_durum)

        # Combat Log Görüntüleyici
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("background-color: #0d0000; border: 1px solid #ff0000; font-size: 14px;")
        self.txt_log.append("Bay Azik'in odasındaki gölgeler çatırdadı ve gerçeklik yırtıldı!")
        self.txt_log.append("Megose, karnındaki deforme kozmik bebekle üzerine çığlık atarak atılıyor!")
        
        if self.tilsim_var_mi:
            self.txt_log.append("\n☀️ Çantandaki 'Güneş Tılsımı' alev alev parlıyor! Kutsal güç Megose'nin yozlaşmış aurasını zayıflattı.")
            self.oyuncu.envanter.remove("Güneş Tılsımı") # Tüketilebilir eşya silinir (Item Consumption)
        else:
            self.txt_log.append("\n❌ DİKKAT: Üzerinde 'Güneş Tılsımı' yok! Megose'nin yaydığı ilkel yozlaşma (Corruption) aurası zihnini eziyor. Onu bu halde yenmen imkansız...")

        self.duzen.addWidget(self.txt_log)

        # Action Buttons
        self.btn_saldir = QPushButton("⚔️ Normal Saldırı")
        self.btn_saldir.setStyleSheet("background-color: #330000; border: 1px solid #ff4444; padding: 10px;")
        self.btn_saldir.clicked.connect(self.normal_saldiri)
        self.duzen.addWidget(self.btn_saldir)

        self.btn_ozel = QPushButton("🔮 Özel Yetenek (Akıl Sağlığı Tüketir)")
        self.btn_ozel.setStyleSheet("background-color: #1a0033; border: 1px solid #9933ff; padding: 10px;")
        self.btn_ozel.clicked.connect(self.ozel_yetenek)
        self.duzen.addWidget(self.btn_ozel)

    def dusman_saldirisi(self):
        """Counter-Attack mantığı: Oyuncu hamlesinden hemen sonra asenkron olmayan (senkron) yanıt."""
        if self.boss_hp <= 0:
            return
        hasar = random.randint(self.boss_hasar_min, self.boss_hasar_max)
        self.oyuncu.hp -= hasar
        self.txt_log.append(f"\n💥 Megose acımasızca vurdu ve {hasar} hasar verdi!")
        self.pencere.sfx_cal("canavar.wav")
        self.durum_guncelle()
        
        if self.oyuncu.hp <= 0:
            self.sonuc = "maglubiyet"
            self.txt_log.append("\n💀 Bedenin parçalandı... Tingen karanlığa gömüldü.")
            QApplication.processEvents() # UI donmalarını (freeze) engeller
            self.accept()

    def normal_saldiri(self):
        """Action Phase 1: Kaynak tüketmeyen standart saldırı algoritması."""
        hasar = self.oyuncu.saldir()
        if not self.tilsim_var_mi:
            hasar = 1 
            
        self.boss_hp -= hasar
        self.txt_log.append(f"\n> ⚔️ Megose'ye {hasar} hasar verdin!")
        self.pencere.sfx_cal("kilic.wav")
        self.durum_guncelle()
        
        if self.boss_hp <= 0:
            self.sonuc = "zafer"
            self.accept()
        else:
            self.dusman_saldirisi()

    def ozel_yetenek(self):
        """Action Phase 2: Polymorphic özel yetenek tetikleyicisi."""
        eski_hp = self.oyuncu.hp
        ozel_hasar = self.oyuncu.ozel_yetenek()
        
        if not self.tilsim_var_mi:
            ozel_hasar = 1 
            
        if ozel_hasar > 0:
            self.boss_hp -= ozel_hasar
            self.txt_log.append(f"\n> 🔮 Zihnini zorlayarak Megose'ye {ozel_hasar} hasar verdin!")
        elif self.oyuncu.hp > eski_hp:
            self.txt_log.append(f"\n> 🌙 Gölgelere karışıp kendini iyileştirdin.")
        else:
            self.txt_log.append(f"\n> ❌ Zihnin bu gücü kaldıramadı! Yetenek geri tepti.")
        
        self.pencere.sfx_cal("ozel_guc.wav")
        self.durum_guncelle()
        
        if self.boss_hp <= 0:
            self.sonuc = "zafer"
            self.accept()
        else:
            self.dusman_saldirisi()

    def durum_guncelle(self):
        """UI Refresh Metodu."""
        self.lbl_durum.setText(f"Megose HP: {self.boss_hp}\nSenin HP: {self.oyuncu.hp} | Akıl Sağlığın: {self.oyuncu.sanity}")
        self.txt_log.verticalScrollBar().setValue(self.txt_log.verticalScrollBar().maximum())


class AnaMenüEkranı(QWidget):
    """
    Uygulamanın Entry Point (Giriş Noktası) Görünümü (View).
    Yeni oyun yaratma (Initialization) veya mevcut kaydı çözümleme (Deserialization) işlemlerini Controller'a aktarır.
    """
    def __init__(self, pencere_referansi):
        super().__init__()
        self.pencere = pencere_referansi
        
        duzen = QVBoxLayout(self)
        duzen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_baslik = QLabel("LORD OF THE MYSTERIES\n- Tingen Sokakları -")
        lbl_baslik.setStyleSheet("color: #8a0303; font-size: 28px; font-weight: bold; font-family: 'Consolas';")
        lbl_baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        duzen.addWidget(lbl_baslik)
        
        duzen.addSpacing(30)
        
        self.lbl_isim = QLabel("Aday Adınız:")
        self.lbl_isim.setStyleSheet("color: #c4c4c4; font-size: 16px;")
        self.txt_isim = QLineEdit()
        self.txt_isim.setText("Muhammed")
        self.txt_isim.setStyleSheet("background-color: #1a1a1a; color: #fff; border: 1px solid #555; padding: 8px; font-size: 14px;")
        self.txt_isim.setFixedWidth(300)
        
        duzen.addWidget(self.lbl_isim, alignment=Qt.AlignmentFlag.AlignCenter)
        duzen.addWidget(self.txt_isim, alignment=Qt.AlignmentFlag.AlignCenter)
        
        duzen.addSpacing(30)
        
        btn_duzen = QHBoxLayout()
        btn_basla = QPushButton("Yeni Oyun (Sıradan İnsan Olarak)")
        btn_basla.setStyleSheet("QPushButton { background-color: #2b2b2b; color: #fff; font-size: 16px; font-family: 'Consolas'; padding: 12px; border: 1px solid #555; } QPushButton:hover { background-color: #8a0303; border: 1px solid #ff0000; }")
        btn_basla.clicked.connect(self.yeni_oyun_baslat)
        
        btn_yukle = QPushButton("Oyunu Yükle")
        btn_yukle.setStyleSheet("QPushButton { background-color: #1a3c1a; color: #fff; font-size: 16px; font-family: 'Consolas'; padding: 12px; border: 1px solid #555; } QPushButton:hover { background-color: #28a745; border: 1px solid #00ff00; }")
        btn_yukle.clicked.connect(self.oyunu_yukle)
        
        btn_duzen.addWidget(btn_basla)
        btn_duzen.addWidget(btn_yukle)
        duzen.addLayout(btn_duzen)

    def yeni_oyun_baslat(self):
        """Karakter modelini varsayılan state (Sıradan İnsan) ile başlatır."""
        isim = self.txt_isim.text().strip()
        if not isim:
            QMessageBox.warning(self, "Hata", "Lütfen bir isim girin!")
            return
        
        self.pencere.oyuncu = Sleepless(isim) 
        self.pencere.oyuncu.pathway = "Sıradan İnsan"
        self.pencere.oyuncu.sequence = 10 
        
        self.pencere.oyun_ekrani_widget.oyun_baslangic_ayari(yeni_mi=True)
        self.pencere.ekran_degistirici.setCurrentIndex(1) # Routing to Gameplay Screen

    def oyunu_yukle(self):
        """Veritabanından Payload okuyup Polymorphic Karakter Sınıflarını (Seer, Assassin, vb.) ayağa kaldırır."""
        isim = self.txt_isim.text().strip()
        if not isim:
            QMessageBox.warning(self, "Hata", "Yüklenecek karakterin adını girmelisin!")
            return
        conn = sqlite3.connect('lotm_save.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kayitlar WHERE isim=?", (isim,))
        kayit = cursor.fetchone()
        conn.close()
        
        if kayit:
            k_isim, k_pathway, k_hp, k_sanity, k_pound, k_sequence, k_envanter = kayit
            
            # Dinamik Instance Yaratımı (Factory Pattern benzeri yapı)
            if k_pathway == "Sleepless": self.pencere.oyuncu = Sleepless(k_isim)
            elif k_pathway == "Seer": self.pencere.oyuncu = Seer(k_isim)
            elif k_pathway == "Assassin": self.pencere.oyuncu = Assassin(k_isim)
            else: 
                self.pencere.oyuncu = Sleepless(k_isim)
                self.pencere.oyuncu.pathway = "Sıradan İnsan"
            
            self.pencere.oyuncu.hp = k_hp
            self.pencere.oyuncu.sanity = k_sanity
            self.pencere.oyuncu.pound = k_pound
            self.pencere.oyuncu.sequence = k_sequence
            self.pencere.oyuncu.envanter = k_envanter.split(",") if k_envanter else []
            self.pencere.oyun_ekrani_widget.oyun_baslangic_ayari(yeni_mi=False)
            self.pencere.ekran_degistirici.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Bulunamadı", f"'{isim}' adında bir kayıt bulunamadı!")


class OyunEkranı(QWidget):
    """
    Core Gameplay View Katmanı.
    Tüm aksiyon menülerini (Navigation), oyun loglarını ve karakter durumlarını render eder.
    """
    def __init__(self, pencere_referansi):
        super().__init__()
        self.pencere = pencere_referansi
        self.ana_duzen = QVBoxLayout(self)

        # Header: Vitals (HP, Sanity, Currency)
        self.stat_duzen = QHBoxLayout()
        self.lbl_can = QLabel("❤️ Can: -")
        self.lbl_sanity = QLabel("🧠 Akıl Sağlığı: -")
        self.lbl_para = QLabel("💷 Para: - Pound")
        self.stat_duzen.addWidget(self.lbl_can)
        self.stat_duzen.addWidget(self.lbl_sanity)
        self.stat_duzen.addWidget(self.lbl_para)
        self.ana_duzen.addLayout(self.stat_duzen)

        # Body: Narrative Log & Inventory Side Panel
        self.orta_duzen = QHBoxLayout()
        self.text_ekrani = QTextEdit()
        self.text_ekrani.setReadOnly(True)
        self.orta_duzen.addWidget(self.text_ekrani, stretch=3)

        self.yan_panel = QFrame()
        self.yan_panel.setObjectName("yan_panel")
        self.yan_duzen = QVBoxLayout(self.yan_panel)
        
        lbl_karakter = QLabel("KARAKTER DURUMU")
        lbl_karakter.setObjectName("bilgi_baslik")
        lbl_karakter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pathway = QLabel("Sınıf: -")
        self.lbl_pathway.setStyleSheet("color: #a3a3a3; font-size: 14px;")
        self.lbl_seviye = QLabel("Dizi (Sequence): -")
        self.lbl_seviye.setStyleSheet("color: #a3a3a3; font-size: 14px;")
        lbl_envanter_baslik = QLabel("\nENVANTER")
        lbl_envanter_baslik.setObjectName("bilgi_baslik")
        lbl_envanter_baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_envanter = QLabel("- Boş")
        self.lbl_envanter.setStyleSheet("color: #a3a3a3; font-size: 14px;")
        self.lbl_envanter.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.yan_duzen.addWidget(lbl_karakter)
        self.yan_duzen.addWidget(self.lbl_pathway)
        self.yan_duzen.addWidget(self.lbl_seviye)
        self.yan_duzen.addWidget(lbl_envanter_baslik)
        self.yan_duzen.addWidget(self.lbl_envanter)
        self.orta_duzen.addWidget(self.yan_panel, stretch=1)
        self.ana_duzen.addLayout(self.orta_duzen)

        # Footer: Action Buttons (Routing Controllers)
        self.buton_duzen = QHBoxLayout()
        self.btn_arastir = QPushButton("Sokakları Araştır")
        self.btn_dinlen = QPushButton("Kliniğe Gir (10£)")
        self.btn_karaborsa = QPushButton("Karaborsa")
        self.btn_azik = QPushButton("🎓 Khoy Üniv. (Bay Azik)")
        self.btn_azik.setStyleSheet("background-color: #3b2b1a; color: #ffcc99;")
        self.btn_kaydet = QPushButton("💾 Kaydet")
        self.btn_kaydet.setStyleSheet("background-color: #005082;")
        
        self.buton_duzen.addWidget(self.btn_arastir)
        self.buton_duzen.addWidget(self.btn_azik)
        self.buton_duzen.addWidget(self.btn_dinlen)
        self.buton_duzen.addWidget(self.btn_karaborsa)
        self.buton_duzen.addWidget(self.btn_kaydet)
        self.ana_duzen.addLayout(self.buton_duzen)

        # Event Bindings
        self.btn_arastir.clicked.connect(self.arastir_tiklandi)
        self.btn_dinlen.clicked.connect(self.klinik_tiklandi)
        self.btn_karaborsa.clicked.connect(self.karaborsa_tiklandi)
        self.btn_azik.clicked.connect(self.azik_tiklandi)
        self.btn_kaydet.clicked.connect(self.oyunu_kaydet)

    def oyun_baslangic_ayari(self, yeni_mi):
        self.text_ekrani.clear()
        if yeni_mi:
            self.text_ekrani.setText(f"Gölgeler toplanıyor...\nTingen şehrine hoş geldin, {self.pencere.oyuncu.isim}.\n\nŞu an sıradan bir insansın. Kaderini değiştirmek istiyorsan karanlık sırları açığa çıkarmalı ve Karaborsa'dan bir yol seçmelisin.")
        else:
            self.text_ekrani.setText(f"Karanlıktan geri döndün, {self.pencere.oyuncu.isim}.\nKaldığın yerden devam ediyorsun...")
        self.arayuzu_guncelle()

    def arayuzu_guncelle(self):
        """Tüm Data ve State değişikliklerini Görünüm (View) katmanına basar."""
        self.lbl_can.setText(f"❤️ Can: {self.pencere.oyuncu.hp}")
        self.lbl_sanity.setText(f"🧠 Akıl Sağlığı: {self.pencere.oyuncu.sanity}")
        self.lbl_para.setText(f"💷 Para: {self.pencere.oyuncu.pound} Pound")
        
        if self.pencere.oyuncu.sequence == 10:
            self.lbl_pathway.setText("Durum: Sıradan İnsan")
            self.lbl_seviye.setText("Dizi: Yok")
        else:
            self.lbl_pathway.setText(f"Sınıf: {self.pencere.oyuncu.pathway}")
            self.lbl_seviye.setText(f"Dizi: {self.pencere.oyuncu.sequence}")
            
        if not self.pencere.oyuncu.envanter:
            self.lbl_envanter.setText("- Boş")
        else:
            envanter_metni = "".join([f"- {e}\n" if isinstance(e, str) else f"- {e.isim}\n" for e in self.pencere.oyuncu.envanter])
            self.lbl_envanter.setText(envanter_metni)
        self.text_ekrani.verticalScrollBar().setValue(self.text_ekrani.verticalScrollBar().maximum())
        self.olum_kontrol()

    def olum_kontrol(self):
        """Game Over Listener."""
        if self.pencere.oyuncu.hp <= 0:
            QMessageBox.critical(self, "ÖLDÜN", "Aldığın yaralara dayanamadın. Kanın Tingen sokaklarına karıştı...")
            self.pencere.close()
        elif self.pencere.oyuncu.sanity <= 0:
            QMessageBox.critical(self, "KONTROLÜ KAYBETTİN", "Zihnin tamamen parçalandı. Artık yozlaşmış bir canavarsın (Rampager)...")
            self.pencere.close()

    def arastir_tiklandi(self):
        """Exploration State Logic - RNG tabanlı hikaye ve çatışma jeneratörü."""
        if "Antigonus Not Defteri" not in self.pencere.oyuncu.envanter and "Azik'in Bakır Düdüğü" not in self.pencere.oyuncu.envanter and random.randint(1, 10) > 8:
            self.text_ekrani.append("\n> 📜 Yıkık dökük bir evin zemininde deri kaplı, tekinsiz bir not defteri buldun! Üzerinde Antigonus ailesinin arması var.")
            self.pencere.sfx_cal("esya.wav")
            self.pencere.oyuncu.envanter.append("Antigonus Not Defteri")
            self.arayuzu_guncelle()
            return 

        olay = random.choice(["para", "delilik", "canavar", "hicbir_sey"]) 
        if olay == "para":
            bulunan = random.randint(3, 8)
            self.pencere.oyuncu.pound += bulunan  
            self.text_ekrani.append(f"\n> Karanlık bir köşede {bulunan} Pound buldun.")
            
        elif olay == "canavar":
            dusman_hasari = random.randint(15, 30)
            self.pencere.oyuncu.hp -= dusman_hasari
            self.text_ekrani.append(f"\n> 💥 Canavar sana saldırdı ve {dusman_hasari} hasar verdi.")
            self.pencere.sfx_cal("canavar.wav")
            self.arayuzu_guncelle()
            
            if self.pencere.oyuncu.hp > 0:
                savas_ekrani = SavasPenceresi(self.pencere.oyuncu, self)
                savas_ekrani.exec() 
                hamle = savas_ekrani.secilen_hamle
                
                if hamle == "normal":
                    benim_hasarim = self.pencere.oyuncu.saldir() 
                    silah = "Gümüş Hançer" if "Gümüş Hançer" in self.pencere.oyuncu.envanter else "Çıplak ellerin"
                    self.text_ekrani.append(f"> ⚔️ {silah} ile karşı saldırı yaptın ve canavara {benim_hasarim} hasar vererek onu alt ettin! (+10 Pound)")
                    self.pencere.sfx_cal("kilic.wav")
                    self.pencere.oyuncu.pound += 10
                elif hamle == "ozel":
                    if self.pencere.oyuncu.sequence == 10:
                        self.text_ekrani.append("> ❌ Henüz bir Beyonder değilsin! Özel yetenek kullanamazsın.")
                    else:
                        eski_hp = self.pencere.oyuncu.hp
                        ozel_hasar = self.pencere.oyuncu.ozel_yetenek() 
                        if ozel_hasar > 0:
                            self.text_ekrani.append(f"> 🔮 Zihninin sınırlarını zorladın! Yeteneğinle {ozel_hasar} hasar verdin ve canavarı yok ettin! (+15 Pound)")
                            self.pencere.sfx_cal("ozel_guc.wav")
                            self.pencere.oyuncu.pound += 15
                        elif self.pencere.oyuncu.hp > eski_hp:
                            self.text_ekrani.append(f"> 🌙 Karanlığı kullanarak kendini iyileştirdin ve canavardan sıyrıldın.")
                        else:
                            self.text_ekrani.append("> ❌ Zihnin bu gücü kaldıramadı! Yetenek geri tepti.")
                else: 
                    self.text_ekrani.append("> 💨 Ara sokaklara kaçtın. Korku zihnini kemiriyor (-5 Sanity).")
                    self.pencere.oyuncu.sanity -= 5
                    
        elif olay == "delilik":
            self.pencere.oyuncu.sanity -= random.randint(10, 20)
            self.text_ekrani.append("\n> Karanlıkta fısıltılar duydun... Zihnin bulanıyor!")
            # AI API Injection: Düşük Sanity durumunda LLM bazlı fısıltı üretimi.
            if self.pencere.oyuncu.sanity < 60 and self.pencere.oyuncu.sanity > 0 and YZ_AKTIF:
                self.text_ekrani.append("⏳ Zihninin derinliklerinden bir ses yükseliyor...")
                QApplication.processEvents() 
                ai_fisilti = YZMotoru.fisilti_uret(self.pencere.oyuncu.sanity)
                if ai_fisilti: self.text_ekrani.append(ai_fisilti)
        else:
            self.text_ekrani.append("\n> Karanlık bir sokağa girdin... Sadece rutubet kokusu var.")
        self.arayuzu_guncelle()

    def azik_tiklandi(self):
        """NPC Interaction & Boss Phase Trigger Controller."""
        self.text_ekrani.append("\n> 🎓 Khoy Üniversitesi'nin sakin koridorlarında Tarih Hocası Bay Azik'in odasına girdin.")
        
        # Condition Check for Final Encounter
        if "Azik'in Bakır Düdüğü" in self.pencere.oyuncu.envanter and self.pencere.oyuncu.pound >= 50 and self.pencere.oyuncu.sequence == 9:
            self.text_ekrani.append("> Bay Azik masaya koyduğun 50 Pound'a ve düdüğe baktı. Yüzü aniden ciddileşti.")
            self.text_ekrani.append("> 'Tingen'den ayrılmadan önce yüzleşmemiz gereken son bir karanlık var...'")
            self.arayuzu_guncelle()
            QApplication.processEvents()
            
            # --- BOSS ENCOUNTER BAŞLATILMASI ---
            self.pencere.sfx_cal("boss.wav")
            boss_ekrani = BossSavasPenceresi(self.pencere.oyuncu, self)
            boss_ekrani.exec()
            
            if boss_ekrani.sonuc == "zafer":
                self.pencere.sfx_cal("zafer.wav")
                self.pencere.oyuncu.pound -= 50
                self.pencere.oyuncu.sequence = 8
                self.text_ekrani.append("\n🧪 Megose'nin kalıntıları arasından doğrulup özel iksirini içtin! Ruhun güçlendi ve Dizi 8'e ulaştın.")
                self.arayuzu_guncelle()
                
                QMessageBox.information(
                    self, 
                    "BÖLÜM 1 SONU - TİNGEN'E VEDA", 
                    f"Tebrikler {self.pencere.oyuncu.isim}, Megose'yi alt ettin ve Dizi 8'e ulaştın!\n\n"
                    "Sisli peronun önünde duruyorsun. Kaptan Dunn Smith'in fedakarlığı ve "
                    "Bay Azik'in dostluğu kalbinde birer yara izi gibi duruyor.\n\n"
                    "Buharlı trenin acı düdüğü öttü. Çantanı alıp vagona bindin.\n"
                    "Bir sonraki hedefin, fırtınaların ve entrikaların başkenti: BACKLUND.\n\n"
                    "OYUNU KAZANDIN!"
                )
                self.pencere.close()
            else:
                self.olum_kontrol() 
            return
            
        elif "Azik'in Bakır Düdüğü" in self.pencere.oyuncu.envanter:
            if self.pencere.oyuncu.sequence == 10:
                self.text_ekrani.append("> Bay Azik sana sıcak bir şekilde gülümsedi: 'Tingen'den ayrılmak için hazırlanmalısın. Ama önce Karaborsa'dan bir yol seçip Beyonder olman gerek.'")
            else:
                self.text_ekrani.append("> Bay Azik uyardı: 'Megose yaklaşıyor. 50 Pound biriktirdiğinde bana gel, onunla yüzleşip seni Backlund trenine yetiştireceğim.'")
            self.pencere.oyuncu.sanity = min(100, self.pencere.oyuncu.sanity + 10)
            
        elif "Antigonus Not Defteri" in self.pencere.oyuncu.envanter:
            self.pencere.oyuncu.envanter.remove("Antigonus Not Defteri")
            self.text_ekrani.append("> Bay Azik'in gözleri elindeki deftere kaydı. 'Bu defter... Üzerindeki aura çok tanıdık ama geçmişim bir sis bulutu gibi.'")
            self.text_ekrani.append("> 🎁 Sana eski, bakır bir düdük uzattı. 'Bunu al. Bu Tingen'deki son adımında sana eşlik edecek. Şimdi gidip güçlen.'")
            self.pencere.sfx_cal("esya.wav")
            self.pencere.oyuncu.envanter.append("Azik'in Bakır Düdüğü")
            self.pencere.oyuncu.sanity = 100 
            
        else:
            self.text_ekrani.append("> Bay Azik dalgın görünüyor: 'Tingen'de son günlerde garip bir hareketlilik var. Efsaneler, Antigonus ailesine ait eski bir not defterinin sokaklarda dolaştığını söylüyor. Onu bulman kaderini etkileyebilir.'")
            
        self.arayuzu_guncelle()

    def klinik_tiklandi(self):
        """Recovery Controller (Health/Sanity Restoration)."""
        if self.pencere.oyuncu.pound >= 10:
            self.pencere.oyuncu.pound -= 10
            maks_hp = 120 if isinstance(self.pencere.oyuncu, Sleepless) else 100
            self.pencere.oyuncu.hp = min(maks_hp, self.pencere.oyuncu.hp + 40)
            self.pencere.oyuncu.sanity = min(100, self.pencere.oyuncu.sanity + 30)
            self.text_ekrani.append("\n> Kliniğe girdin. İlaçlar seni kendine getirdi. (-10 Pound)")
        else:
            self.text_ekrani.append("\n> Yetersiz bakiye!")
        self.arayuzu_guncelle()

    def karaborsa_tiklandi(self):
        """Shop System Integration - Obje/Class modifikasyonu."""
        if self.pencere.oyuncu.sequence == 10:
            esyalar = [
                "Sleepless İksiri (20 £) - Gecenin gücünü uyandırır.", 
                "Seer İksiri (20 £) - Kaderin sırlarını fısıldar.", 
                "Assassin İksiri (20 £) - Gölgelerde ölüm olursun."
            ]
        else:
            esyalar = ["Gümüş Hançer (25 £)", "Güneş Tılsımı (40 £)"]
            
        secim, tamam = QInputDialog.getItem(self, "Karaborsa", f"Ne almak istersin?\n(Bakiyen: {self.pencere.oyuncu.pound}£)", esyalar, 0, False)
        if tamam and secim:
            if "Sleepless İksiri" in secim and self.pencere.oyuncu.pound >= 20:
                self.sinif_degistir(Sleepless, "Sleepless", 20)
            elif "Seer İksiri" in secim and self.pencere.oyuncu.pound >= 20:
                self.sinif_degistir(Seer, "Seer", 20)
            elif "Assassin İksiri" in secim and self.pencere.oyuncu.pound >= 20:
                self.sinif_degistir(Assassin, "Assassin", 20)
            elif "Gümüş Hançer" in secim and self.pencere.oyuncu.pound >= 25:
                self.pencere.oyuncu.pound -= 25
                self.pencere.oyuncu.envanter.append("Gümüş Hançer")
                self.text_ekrani.append("\n> Gümüş Hançer satın aldın.")
                self.pencere.sfx_cal("esya.wav")
            elif "Güneş Tılsımı" in secim and self.pencere.oyuncu.pound >= 40:
                self.pencere.oyuncu.pound -= 40
                self.pencere.oyuncu.envanter.append("Güneş Tılsımı")
                self.text_ekrani.append("\n> Güneş Tılsımı satın aldın.")
                self.pencere.sfx_cal("esya.wav")
            else:
                self.text_ekrani.append("\n> Satıcı pis pis sırıttı: 'Yetersiz bakiye!'")
        self.arayuzu_guncelle()

    def sinif_degistir(self, sinif_class, isim, ucret):
        """Class Mutation (Type-casting) Controller."""
        eski_isim = self.pencere.oyuncu.isim
        eski_para = self.pencere.oyuncu.pound - ucret
        eski_envanter = self.pencere.oyuncu.envanter.copy() 
        
        self.pencere.oyuncu = sinif_class(eski_isim)
        self.pencere.oyuncu.pound = eski_para
        self.pencere.oyuncu.envanter = eski_envanter
        
        self.text_ekrani.append(f"\n🧪 Karaborsa'dan aldığın {isim} İksiri'ni oracıkta içtin... Zihnin genişliyor!")
        self.text_ekrani.append(f"🔼 Kaderin ağları örüldü. Artık resmi olarak bir {self.pencere.oyuncu.pathway}'sın! (Dizi 9)")
        self.pencere.sfx_cal("ozel_guc.wav")
        self.pencere.oyuncu.hp = 100 
        self.arayuzu_guncelle()

    def oyunu_kaydet(self):
        """Current State nesnesini SQLite veritabanına Serileştirme."""
        try:
            conn = sqlite3.connect('lotm_save.db')
            cursor = conn.cursor()
            env_str = ",".join([e if isinstance(e, str) else e.isim for e in self.pencere.oyuncu.envanter])
            cursor.execute('''REPLACE INTO kayitlar (isim, pathway, hp, sanity, pound, sequence, envanter)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (self.pencere.oyuncu.isim, self.pencere.oyuncu.pathway,
                            self.pencere.oyuncu.hp, self.pencere.oyuncu.sanity,
                            self.pencere.oyuncu.pound, self.pencere.oyuncu.sequence, env_str))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Kayıt Başarılı", f"{self.pencere.oyuncu.isim}, verilerin kara kaplı deftere işlendi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt sırasında bir hata oluştu:\n{str(e)}")


class AnaPencere(QMainWindow):
    """
    Main Application Window (Root Controller).
    Ekranlar arası geçişi (View Routing) ve global servisleri (Audio Engine, Database) yönetir.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lord of the Mysteries - Tingen Sokakları")
        self.setGeometry(100, 100, 1050, 650) 
        
        self.oyuncu = None 
        veritabani_hazirla()

        # Audio Engine Initialization (Background Music & Sound Effects)
        self.ses_calar = QMediaPlayer()
        self.ses_cikisi = QAudioOutput()
        self.ses_cikisi.setVolume(0.3) 
        self.ses_calar.setAudioOutput(self.ses_cikisi)
        
        muzik_yolu = os.path.join(os.getcwd(), "sesler", "ambiyans.mp3")
        if os.path.exists(muzik_yolu):
            self.ses_calar.setSource(QUrl.fromLocalFile(muzik_yolu))
            self.ses_calar.setLoops(-1) # Infinite Loop
            self.ses_calar.play()
            
        # SFX Object Pool (Efektlerin bellek yönetimi için hash tablosu)
        self.sfx_havuzu = {}
        sfx_dosyalar = ["kilic.wav", "canavar.wav", "boss.wav", "zafer.wav", "ozel_guc.wav", "esya.wav"]
        for ses in sfx_dosyalar:
            yol = os.path.join(os.getcwd(), "sesler", ses)
            efekt = QSoundEffect(self)
            if os.path.exists(yol):
                efekt.setSource(QUrl.fromLocalFile(yol))
                efekt.setVolume(0.8)
            self.sfx_havuzu[ses] = efekt

        # UI/UX Routing Stack (QStackedWidget)
        self.ekran_degistirici = QStackedWidget()
        self.setCentralWidget(self.ekran_degistirici)

        self.ana_menu_widget = AnaMenüEkranı(self)
        self.oyun_ekrani_widget = OyunEkranı(self)

        self.ekran_degistirici.addWidget(self.ana_menu_widget)
        self.ekran_degistirici.addWidget(self.oyun_ekrani_widget)
        
        # Global Stylesheet (CSS benzeri arayüz şekillendirmesi)
        self.setStyleSheet("""
            QMainWindow { background-color: #0d0d0d; }
            QWidget { background-color: #0d0d0d; }
            QTextEdit { background-color: #1a1a1a; color: #c4c4c4; font-size: 16px; font-family: 'Consolas'; border: 1px solid #333; padding: 10px; }
            QLabel { color: #8a0303; font-size: 16px; font-weight: bold; font-family: 'Consolas'; }
            QLabel#bilgi_baslik { color: #c4c4c4; font-size: 18px; text-decoration: underline; }
            QPushButton { background-color: #2b2b2b; color: #ffffff; font-size: 14px; font-family: 'Consolas'; padding: 8px; border: 1px solid #555; }
            QPushButton:hover { background-color: #8a0303; border: 1px solid #ff0000; }
            QFrame#yan_panel { border: 1px solid #333; background-color: #141414; }
        """)
        
    def sfx_cal(self, dosya_adi):
        """Asenkron Ses Efekti Tetikleyicisi (Event Emitter)."""
        if dosya_adi in self.sfx_havuzu and self.sfx_havuzu[dosya_adi].source().isValid():
            self.sfx_havuzu[dosya_adi].play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec())