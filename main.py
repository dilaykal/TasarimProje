import os
import random  # random modülü eklendi
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from urllib.parse import quote

def setup_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Bot tespitini zorlaştırmak için ek ayarlar
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-infobars')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--memory-pressure-off')
    options.add_argument('--window-size=1920,1080')  # Sabit pencere boyutu
    options.add_argument('--start-maximized')
    
    # User agent belirleme
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'
    ]
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    options.page_load_strategy = 'eager'
    
    driver_path = "C:\\Users\\dilay\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    
    try:
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        print(f"Sürücü başlatma hatası: {str(e)}")
        return None


def wait_for_tweets(driver, timeout=30):
    try:
        wait = WebDriverWait(driver, timeout)
        selectors = [
            'article[data-testid="tweet"]',
            'article[role="article"]',
            'div[data-testid="tweetText"]'
        ]
        
        for selector in selectors:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                return True
            except:
                continue
        return False
    except Exception as e:
        print(f"Bekleme hatası: {str(e)}")
        return False

def extract_tweet_info(element):
    try:
        # Tweet metnini al
        tweet_text = element.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
        
        # Tweet tarihini al
        time_element = element.find_element(By.CSS_SELECTOR, 'time')
        tweet_date = time_element.get_attribute('datetime')
        
        # Beğeni sayısını al
        try:
            like_element = element.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
            like_count = like_element.text
        except:
            like_count = "0"
            
        # Retweet sayısını al
        try:
            retweet_element = element.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]')
            retweet_count = retweet_element.text
        except:
            retweet_count = "0"
            
        # Kullanıcı adını al
        try:
            username = element.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]').text
        except:
            username = "Bilinmeyen Kullanıcı"
        
        return {
            'date': tweet_date,
            'username': username,
            'text': tweet_text,
            'likes': like_count,
            'retweets': retweet_count
        }
    except Exception as e:
        return None

def scroll_and_collect_tweets(driver, tweet_count=2000):
    tweets = set()
    scroll_attempts = 0
    max_attempts = 50
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    print("Tweetler toplanıyor...")
    
    while len(tweets) < tweet_count and scroll_attempts < max_attempts:
        try:
            # Rastgele bekleme süresi
            time.sleep(random.uniform(2, 4))
            
            elements = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
            
            for element in elements:
                tweet_info = extract_tweet_info(element)
                if tweet_info:
                    tweet_text = (f"Tarih: {tweet_info['date']}\n"
                                f"Kullanıcı: {tweet_info['username']}\n"
                                f"Tweet: {tweet_info['text']}\n"
                                f"Beğeni: {tweet_info['likes']}\n"
                                f"Retweet: {tweet_info['retweets']}\n")
                    
                    if tweet_text not in tweets:
                        tweets.add(tweet_text)
                        print(f"Yeni tweet bulundu. Toplam: {len(tweets)}")
            
            # Rastgele scroll miktarı
            scroll_amount = random.randint(500, 1000)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                time.sleep(random.uniform(3, 5))
                if driver.execute_script("return document.body.scrollHeight") == last_height:
                    break
            last_height = new_height
            
            scroll_attempts += 1
            
        except Exception as e:
            print(f"Scroll hatası: {str(e)}")
            scroll_attempts += 1
            time.sleep(random.uniform(2, 4))
    
    return list(tweets)

def save_tweets(tweets, filename='Hatay_deprem_tweetleri.txt'):
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(f"6 Şubat 2023 Depremi Tweetleri\n")
            file.write(f"Toplam Tweet Sayısı: {len(tweets)}\n")
            file.write("=" * 50 + "\n\n")
            
            for i, tweet in enumerate(tweets, 1):
                file.write(f"Tweet {i}:\n{tweet}\n")
                file.write("-" * 50 + "\n")
        print(f"Tweetler {filename} dosyasına kaydedildi")
    except Exception as e:
        print(f"Kaydetme hatası: {str(e)}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("6 Şubat Depremi Hatay tweet toplama işlemi başlatılıyor...")
    
    search_queries = [
        # Temel aramalar - 1 yıllık zaman aralığı
        '(Hatay deprem) until:2024-02-06 since:2023-02-06 lang:tr',
        '(Hatay enkaz) until:2024-02-06 since:2023-02-06 lang:tr',
        '(Antakya deprem) until:2024-02-06 since:2023-02-06 lang:tr',
        
        # İlçe bazlı aramalar (3'er aylık periyotlar)
        *[f'({ilce}) (deprem OR enkaz OR yardım OR acil) until:{end_date} since:{start_date} lang:tr'
          for ilce in [
              "Antakya", "İskenderun", "Defne", "Samandağ", "Kırıkhan",
              "Arsuz", "Reyhanlı", "Dörtyol", "Altınözü", "Hassa",
              "Belen", "Yayladağı", "Erzin", "Payas"
          ]
          for start_date, end_date in [
              ("2023-02-06", "2023-05-06"),
              ("2023-05-06", "2023-08-06"),
              ("2023-08-06", "2023-11-06"),
              ("2023-11-06", "2024-02-06")
          ]
        ],
        
        # Dönemsel aramalar (3'er aylık)
        '(Hatay) (enkaz OR yardım OR acil) until:2023-05-06 since:2023-02-06 lang:tr', # İlk 3 ay
        '(Hatay) (enkaz OR yardım OR acil) until:2023-08-06 since:2023-05-06 lang:tr', # İkinci 3 ay
        '(Hatay) (enkaz OR yardım OR acil) until:2023-11-06 since:2023-08-06 lang:tr', # Üçüncü 3 ay
        '(Hatay) (enkaz OR yardım OR acil) until:2024-02-06 since:2023-11-06 lang:tr', # Son 3 ay
        
        # Önemli bölgeler ve mahalleler
        *[f'(Hatay OR Antakya) "{mahalle}" (enkaz OR yardım) until:{end_date} since:{start_date} lang:tr'
          for mahalle in [
              "Aksaray Mahallesi", "Ürgenpaşa Mahallesi", "Cumhuriyet Mahallesi",
              "Gündüz Mahallesi", "Cebrail Mahallesi", "Odabaşı Mahallesi",
              "Sümerler Mahallesi", "Akevler Mahallesi", "General Şükrü Kanatlı Mahallesi",
              "Akasya Mahallesi", "Anayazı Mahallesi", "Saraykent Mahallesi"
          ]
          for start_date, end_date in [
              ("2023-02-06", "2023-05-06"),
              ("2023-05-06", "2023-08-06"),
              ("2023-08-06", "2023-11-06"),
              ("2023-11-06", "2024-02-06")
          ]
        ],
        
        # İskenderun özel sorguları
        *[f'(İskenderun) "{bolge}" (deprem OR enkaz OR yardım) until:{end_date} since:{start_date} lang:tr'
          for bolge in [
              "Merkez", "Sahil", "Barbaros Mahallesi", "Mustafa Kemal Mahallesi",
              "Yenişehir Mahallesi", "Numune Mahallesi", "Çay Mahallesi"
          ]
          for start_date, end_date in [
              ("2023-02-06", "2023-05-06"),
              ("2023-05-06", "2023-08-06"),
              ("2023-08-06", "2023-11-06"),
              ("2023-11-06", "2024-02-06")
          ]
        ],
        
        # Kritik altyapı ve hizmetler
        '(Hatay) (hastane OR sağlık OR okul OR eğitim) until:2024-02-06 since:2023-02-06 lang:tr',
        '(Hatay) (su OR elektrik OR doğalgaz) until:2024-02-06 since:2023-02-06 lang:tr',
        '(Hatay) (yol OR ulaşım OR altyapı) until:2024-02-06 since:2023-02-06 lang:tr',
        
        # Barınma ve yerleşim
        '(Hatay) (çadır OR konteyner OR barınma) until:2024-02-06 since:2023-02-06 lang:tr',
        '(Hatay) (kira OR ev OR konut) (yardım OR destek) until:2024-02-06 since:2023-02-06 lang:tr',
        '(Hatay) (TOKİ OR kalıcı konut) until:2024-02-06 since:2023-02-06 lang:tr',
        
        # Resmi kurumlar ve yardım organizasyonları
        '(Hatay) (AFAD OR valilik OR belediye) until:2024-02-06 since:2023-02-06 lang:tr',
        'from:hataybbld until:2024-02-06 since:2023-02-06',
        'from:AFAD (Hatay) until:2024-02-06 since:2023-02-06',
        
        # Özel durumlar
        '(Hatay) (tarihi eser OR kültürel miras) until:2024-02-06 since:2023-02-06 lang:tr',
        '(Hatay) (esnaf OR işyeri OR ekonomi) until:2024-02-06 since:2023-02-06 lang:tr',
        '(Hatay) (öğrenci OR üniversite) until:2024-02-06 since:2023-02-06 lang:tr',
        
        # Yeniden yapılanma ve iyileştirme
        '(Hatay) (yeniden yapılanma OR iyileştirme OR onarım) until:2024-02-06 since:2023-02-06 lang:tr',
        '(Hatay) (kentsel dönüşüm OR imar OR plan) until:2024-02-06 since:2023-02-06 lang:tr',
        
        # Hashtag'ler (3'er aylık dönemler)
        *[f'#{tag} until:{end_date} since:{start_date} lang:tr'
          for tag in [
              'HatayDeprem', 'AntakyaDeprem', 'HatayaYardım',
              'İskenderunDeprem', 'DefneDeprem', 'SamandağDeprem'
          ]
          for start_date, end_date in [
              ("2023-02-06", "2023-05-06"),
              ("2023-05-06", "2023-08-06"),
              ("2023-08-06", "2023-11-06"),
              ("2023-11-06", "2024-02-06")
          ]
        ],
        
        # İyileşme süreci sorguları
        '(Hatay) (normalleşme OR iyileşme OR toparlanma) until:2024-02-06 since:2023-08-06 lang:tr',
        '(Hatay) (yeniden inşa OR restorasyon) until:2024-02-06 since:2023-08-06 lang:tr',
        
        # Uzun vadeli etki ve yıldönümü sorguları
        '(Hatay deprem) (1 yıl OR birinci yıl OR yıldönümü) until:2024-02-06 since:2024-01-01 lang:tr',
        
        # Özel yardım çağrıları
        '(Hatay) (acil yardım OR ses geliyor OR kurtarın) until:2023-03-06 since:2023-02-06 lang:tr',
        '(Hatay) (arama kurtarma OR AKUT OR JAK) until:2023-03-06 since:2023-02-06 lang:tr'
    ]
    
    tweets_per_query = 2000
    all_tweets = set()
    driver = setup_driver()
    if not driver:
        return
        
    
    try:
        for query in search_queries:
            try:
                encoded_query = quote(query)
                url = f'https://x.com/search?q={encoded_query}&src=typed_query&f=top'
                
                print(f"\nArama yapılıyor: {query}")
                driver.get(url)
                
                # Sayfa yükleme bekleme süresi optimize edildi
                time.sleep(15)  # İlk yükleme için daha uzun bekleme
                
                if wait_for_tweets(driver):
                    tweets = scroll_and_collect_tweets(driver, tweet_count=tweets_per_query)
                    all_tweets.update(tweets)
                    print(f"Bu aramada {len(tweets)} tweet bulundu")
                else:
                    print("Bu arama için tweet bulunamadı")
                    
                # Her aramadan sonra dinamik bekleme
                time.sleep(random.uniform(8, 12))
                
            except Exception as e:
                print(f"Bu arama sırasında hata oluştu: {str(e)}")
                try:
                    driver.quit()
                except:
                    pass
                driver = setup_driver()
                if not driver:
                    print("Sürücü yeniden başlatılamadı. Program sonlandırılıyor.")
                    return
                time.sleep(15)
                continue
        
        if all_tweets:
            print(f"\nToplam {len(all_tweets)} benzersiz tweet bulundu")
            save_tweets(all_tweets)
        else:
            print("Hiç tweet bulunamadı")
        
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
    
    finally:
        try:
            driver.quit()
        except:
            pass
        print("İşlem tamamlandı.")

if __name__ == "__main__":
    main()