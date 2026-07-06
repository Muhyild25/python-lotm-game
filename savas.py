import random

class SavasYoneticisi:
    @staticmethod
    def normal_savas(oyuncu, yaratik, deli_yazdir):
        deli_yazdir(f"\n🦇 Karanlıktan '{yaratik.isim}' fırladı!", oyuncu.sanity)
        while yaratik.hp > 0 and oyuncu.hp > 0:
            hamle = input(f"\n[HP: {oyuncu.hp} | Sanity: {oyuncu.sanity} | Canavar HP: {yaratik.hp}]\n1- Normal Saldırı, 2- Özel Yetenek Kullan, 3- Kaç: ")
            
            if hamle == '1':
                yaratik.hasar_al(oyuncu.saldir())
                if yaratik.hp > 0: oyuncu.hasar_al(yaratik.saldir())
            elif hamle == '2':
                verilen_hasar = oyuncu.ozel_yetenek()
                if verilen_hasar > 0:
                    yaratik.hasar_al(verilen_hasar)
                    print(f"💥 Düşmana {verilen_hasar} hasar verdin!")
                if yaratik.hp > 0: oyuncu.hasar_al(yaratik.saldir())
            elif hamle == '3':
                print("🏃 Gölgelere kaçıp kurtuldun!")
                return "kacti"
                
        if oyuncu.hp <= 0:
            print("\n💀 Öldün... Tingen sokakları seni de yuttu.")
            return "oldu"
        elif yaratik.hp <= 0:
            kazanc = random.randint(10, 20)
            oyuncu.pound += kazanc
            print(f"\n🏆 Canavarı yendin! {kazanc} Pound kazandın.")
            return "kazandi"

    @staticmethod
    def boss_savasi(oyuncu, boss):
        print(f"\n⛪ Kilisenin kapısını kırarak içeri girdin! '{boss.isim}' sana saldırdı!")
        while boss.hp > 0 and oyuncu.hp > 0:
            hamle = input(f"\n🚨 [SENİN HP: {oyuncu.hp} | Sanity: {oyuncu.sanity} | BOSS HP: {boss.hp}]\n1- Normal Saldırı, 2- Özel Yetenek Kullan: ")
            
            if hamle == '1':
                boss.hasar_al(oyuncu.saldir())
                if boss.hp > 0: oyuncu.hasar_al(boss.saldir())
            elif hamle == '2':
                verilen_hasar = oyuncu.ozel_yetenek()
                if verilen_hasar > 0:
                    boss.hasar_al(verilen_hasar)
                    print(f"💥 Boss'a {verilen_hasar} hasar verdin!")
                if boss.hp > 0: oyuncu.hasar_al(boss.saldir())
                
        if oyuncu.hp <= 0:
            print("\n💀 Boss zihnini paramparça etti.")
            return "oldu"
        elif boss.hp <= 0:
            return "kazandi"