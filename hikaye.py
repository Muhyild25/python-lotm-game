import random

class HikayeYoneticisi:
    def __init__(self):
        self.adim = 0
        self.gunluk_sayfasi = 0
        
    def gorev_metnini_getir(self):
        if self.adim == 0:
            return "📍 GÖREV: Sislerin ardındaki sırrı çözmek için sokakları araştır."
        elif self.adim == 1:
            return f"📍 GÖREV: Kurbanların bıraktığı Kayıp Günlük Sayfalarını topla ({self.gunluk_sayfasi}/3)"
        elif self.adim == 2:
            return "📍 GÖREV: Tingen Kilisesi'ndeki yozlaşmış pusuya karşı kendini hazırla!"
        elif self.adim == 3:
            return "🎉 BÖLÜM TAMAMLANDI: Sisler seni Tarot Kulübü'ne çağırıyor..."
            
    def sokak_arastirmasi_yap(self):
        """Sokakta araştırma yapıldığında hikaye metinlerini döndürür"""
        if self.adim == 0:
            self.adim = 1
            self.gunluk_sayfasi = 1
            return "\n📜 Çamurların arasında kan lekeli bir kağıt parçası buldun! Bu bir günlüğün ilk sayfası...\nFısıltılar diyor ki: 'Geceleri kiliseden gelen sesler dua değil, aç bir canavarın hırıltısı...'"
            
        elif self.adim == 1 and random.randint(1, 2) == 1:
            self.gunluk_sayfasi += 1
            if self.gunluk_sayfasi == 3:
                self.adim = 2
                return "\n📜 Bir günlük sayfası daha buldun!\n⚠️ Günlük tamamlandı! Şehirdeki yozlaşmanın kaynağı Tingen Kilisesi'nin rahibiymiş!\nKilisenin kapıları artık açıldı. Oraya gitmeden önce iyice hazırlandığından emin ol."
            else:
                return f"\n📜 Bir günlük sayfası daha buldun! Gizem çözülüyor... ({self.gunluk_sayfasi}/3)"
                
        return "" # Eğer hikaye ilerlemediyse boş metin döndür