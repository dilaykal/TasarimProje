
# Afet Yönetimi için Sosyal Medya Analiz Sistemi

## Proje Hakkında
Afet durumlarında sosyal medya verilerini analiz ederek ihtiyaç ve kaynakları coğrafi olarak haritalandıran, afet yönetim ekiplerine hızlı karar alma sürecinde yardımcı olan bir sistem.

## Kullanılan Teknolojiler
- Python
- Selenium WebDriver & ChromeDriver
- BERT ve RoBERTa dil modelleri
- Geopy kütüphanesi
- Web Scraping

## Temel Özellikler
- XLM-RoBERTa ile dil tespiti
- Metin sınıflandırma ve önceliklendirme
- Coğrafi haritalama
- Otomatik veri toplama ve işleme

## Kullanılan Modeller
- BERT Türkçe (dbmdz/bert-base-turkish-uncased)
- XLM-RoBERTa


## Önceliklendirme Formülü
```
Final Skor = (Anahtar Kelime Skoru × Pozisyon Çarpanı × Temel Öncelik) + 
             (Konum Skoru × 2) + (Aciliyet Skoru × 1.5)
```
