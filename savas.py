import random

class SavasYoneticisi:
    """
    Oyun içi savaş mekaniklerini ve sıra tabanlı (turn-based) çarpışma döngülerini (combat loop) 
    yöneten statik kontrolcü sınıfı.
    """

    @staticmethod
    def normal_savas(oyuncu, yaratik, deli_yazdir):
        """
        Standart düşman karşılaşmalarını (Encounter) çözer.
        Karakter ve düşman HP state'leri (durumları) sıfırın altına inene kadar veya kaçış (flee) 
        tetiklenene kadar döngüyü sürdürür.
        """
        deli_yazdir(f"\n🦇 Karanlıktan '{yaratik.isim}' fırladı!", oyuncu.sanity)
        
        # Savaş Döngüsü (Combat State Loop): İki taraftan birinin HP değeri tükenene kadar devam eder.
        while yaratik.hp > 0 and oyuncu.hp > 0:
            # I/O ve Eylem Seçimi (Action Phase)
            hamle = input(f"\n[HP: {oyuncu.hp} | Sanity: {oyuncu.sanity} | Canavar HP: {yaratik.hp}]\n1- Normal Saldırı, 2- Özel Yetenek Kullan, 3- Kaç: ")
            
            if hamle == '1':
                # Hasar Çözümlemesi (Damage Resolution): Oyuncu saldırısı ve düşman misillemesi
                yaratik.hasar_al(oyuncu.saldir())
                if yaratik.hp > 0: 
                    oyuncu.hasar_al(yaratik.saldir())
            
            elif hamle == '2':
                # Özel Yetenek Kullanımı (Skill Execution) ve Kaynak (Resource) yönetimi
                verilen_hasar = oyuncu.ozel_yetenek()
                if verilen_hasar > 0:
                    yaratik.hasar_al(verilen_hasar)
                    print(f"💥 Düşmana {verilen_hasar} hasar verdin!")
                
                # Misilleme (Counter-Attack) kontrolü
                if yaratik.hp > 0: 
                    oyuncu.hasar_al(yaratik.saldir())
            
            elif hamle == '3':
                # Kaçış eylemi (Flee Mechanism)
                print("🏃 Gölgelere kaçıp kurtuldun!")
                return "kacti"
                
        # Savaş Sonucu Değerlendirmesi (Encounter Conclusion)
        if oyuncu.hp <= 0:
            print("\n💀 Öldün... Tingen sokakları seni de yuttu.")
            return "oldu"
        elif yaratik.hp <= 0:
            # Ekonomi / Ganimet (Loot) Entegrasyonu
            kazanc = random.randint(10, 20)
            oyuncu.pound += kazanc
            print(f"\n🏆 Canavarı yendin! {kazanc} Pound kazandın.")
            return "kazandi"

    @staticmethod
    def boss_savasi(oyuncu, boss):
        """
        Hikaye sonu (Boss) karşılaşmalarını çözer. 
        Standart savaştan farklı olarak tasarım gereği kaçış (flee) mekanizması devre dışı bırakılmıştır.
        """
        print(f"\n⛪ Kilisenin kapısını kırarak içeri girdin! '{boss.isim}' sana saldırdı!")
        
        # Boss Savaş Döngüsü (Boss Encounter Loop)
        while boss.hp > 0 and oyuncu.hp > 0:
            hamle = input(f"\n🚨 [SENİN HP: {oyuncu.hp} | Sanity: {oyuncu.sanity} | BOSS HP: {boss.hp}]\n1- Normal Saldırı, 2- Özel Yetenek Kullan: ")
            
            if hamle == '1':
                boss.hasar_al(oyuncu.saldir())
                if boss.hp > 0: 
                    oyuncu.hasar_al(boss.saldir())
            
            elif hamle == '2':
                verilen_hasar = oyuncu.ozel_yetenek()
                if verilen_hasar > 0:
                    boss.hasar_al(verilen_hasar)
                    print(f"💥 Boss'a {verilen_hasar} hasar verdin!")
                
                if boss.hp > 0: 
                    oyuncu.hasar_al(boss.saldir())
                
        # Boss Savaş Sonucu Değerlendirmesi
        if oyuncu.hp <= 0:
            print("\n💀 Boss zihnini paramparça etti.")
            return "oldu"
        elif boss.hp <= 0:
            return "kazandi"