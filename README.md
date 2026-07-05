# Lord of the Mysteries - Text Based RPG 🌫️

Bu proje, Python ve Nesne Yönelimli Programlama (OOP) mimarisi kullanılarak geliştirilmiş, metin tabanlı bir karanlık fantastik rol yapma oyunudur. Lord of the Mysteries evreninin psikolojik gerilim atmosferini yansıtır.

## 🚀 Proje Özellikleri (Mevcut Sürüm)
* **Kalıtım (Inheritance) Mimarisi:** Karakterler ve düşmanlar ortak bir `Varlik` ata sınıfından türetilmiştir.
* **Kapsamlı Envanter Sistemi:** Sınıf tabanlı eşya yönetimi ve Karaborsa mekaniği.
* **Delilik (Madness) Algoritması:** Karakterin akıl sağlığı düştükçe arayüzdeki metinleri dinamik olarak bozan ve fısıltılar ekleyen özel string manipülasyonu.
* **Kalıcı Kayıt Sistemi (SQLite):** Oyuncunun canı, parası, eşyaları ve evrendeki hikaye ilerlemesi ilişkisel veri tabanına JSON formatında serileştirilerek kaydedilir.
* **Durum Makinesi (State Machine) ile Hikaye Yönetimi:** Oyuncunun eylemlerine göre açılan yeni görevler ve dinamik Boss savaşları.

## 🛠️ Kurulum
1. Projeyi bilgisayarınıza klonlayın.
2. Terminal üzerinden proje dizinine gidin.
3. `python oyun.py` komutuyla oyunu başlatın.