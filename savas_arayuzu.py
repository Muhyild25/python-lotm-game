from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class SavasPenceresi(QDialog):
    """Canavar saldırılarında açılan özel 3 seçenekli savaş ekranı."""
    def __init__(self, oyuncu, parent=None):
        super().__init__(parent)
        self.oyuncu = oyuncu
        self.secilen_hamle = "kac" # Varsayılan olarak kaçmak

        self.setWindowTitle("SAVAŞ ZAMANI!")
        self.setFixedSize(350, 250)
        
        # Karanlık Tema
        self.setStyleSheet("""
            QDialog { background-color: #0a0a0a; border: 2px solid #8a0303; }
            QLabel { color: #ff4444; font-size: 15px; font-family: 'Consolas'; font-weight: bold; }
            QPushButton { color: #ffffff; font-size: 14px; font-family: 'Consolas'; padding: 10px; border: 1px solid #555; }
            QPushButton:hover { border: 1px solid #ff0000; }
        """)

        duzen = QVBoxLayout(self)

        # Bilgi Ekranı
        lbl_bilgi = QLabel(f"Sisin içinden bir canavar fırladı!\n\nSınıfın: {self.oyuncu.pathway}\n❤️ Can: {self.oyuncu.hp} | 🧠 Sanity: {self.oyuncu.sanity}")
        lbl_bilgi.setAlignment(Qt.AlignmentFlag.AlignCenter)
        duzen.addWidget(lbl_bilgi)
        
        duzen.addSpacing(10)

        # 1. Normal Saldırı Butonu
        btn_normal = QPushButton("⚔️ Normal Saldırı (Güvenli)")
        btn_normal.setStyleSheet("background-color: #2b2b2b;")
        btn_normal.clicked.connect(self.normal_sec)
        
        # 2. Özel Yetenek Butonu
        btn_ozel = QPushButton("🔮 Özel Yetenek Kullan (Sanity Harcar)")
        btn_ozel.setStyleSheet("background-color: #3b0b0b; color: #ff9999;") # Daha kırmızı/tekinsiz bir buton
        btn_ozel.clicked.connect(self.ozel_sec)
        
        # 3. Kaçış Butonu
        btn_kac = QPushButton("💨 Karanlığa Kaç (-5 Sanity)")
        btn_kac.setStyleSheet("background-color: #1a1a1a;")
        btn_kac.clicked.connect(self.kac_sec)

        duzen.addWidget(btn_normal)
        duzen.addWidget(btn_ozel)
        duzen.addWidget(btn_kac)

    # Butonlara basıldığında kararı kaydedip pencereyi kapatıyoruz
    def normal_sec(self):
        self.secilen_hamle = "normal"
        self.accept()

    def ozel_sec(self):
        self.secilen_hamle = "ozel"
        self.accept()

    def kac_sec(self):
        self.secilen_hamle = "kac"
        self.accept()