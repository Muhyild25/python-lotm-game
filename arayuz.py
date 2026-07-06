import random

def deli_yazdir(metin, sanity):
    """Karakterin delilik seviyesine göre ekrana basılan metni bozar."""
    if sanity >= 60:
        print(metin)
        return
    fisiltilar = ["\n(Gölgeler hareket ediyor...)", "\n(Onlara güvenme...)", "\n(Gözlere bakma...)", "\n(Derinin altında bir şeyler sürünüyor...)"]
    if 30 <= sanity < 60:
        if random.randint(1, 4) == 1: print(random.choice(fisiltilar))
        print(metin)
    elif sanity < 30:
        if random.randint(1, 3) == 1: print(random.choice(fisiltilar))
        bozuk_metin = "".join(random.choice(["#", "?", "!", "%", "x", "_"]) if harf != " " and random.randint(1, 6) == 1 else harf for harf in metin)
        print(bozuk_metin)