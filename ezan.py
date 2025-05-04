import time
import json
from datetime import datetime, timedelta
import pygame
import threading

# JSON dosyasının tam yolunu belirtin
file_path = r'C:\Users\srvtc\OneDrive\Desktop\vakit.json'

# Her ezan vakti için mp3 dosyalarının yolunu belirleyin
mp3_files = {
    "sabah": r'C:\Users\srvtc\OneDrive\Desktop\sabah.mp3',
    "ogle": r'C:\Users\srvtc\OneDrive\Desktop\ogle.mp3',
    "ikindi": r'C:\Users\srvtc\OneDrive\Desktop\ikindi.mp3',
    "aksam": r'C:\Users\srvtc\OneDrive\Desktop\aksam.mp3',
    "yatsi": r'C:\Users\srvtc\OneDrive\Desktop\yatsi.mp3'
}

# JSON dosyasından namaz vakitlerini okuma fonksiyonu
def load_prayer_times(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Belirtilen saati sürekli kontrol et ve saat geldiğinde mp3 dosyasını çal
def play_mp3_at_time(prayer, mp3_file, target_hour, target_minute, play_duration=240):
    print(f"Belirtilen saat bekleniyor... {prayer} vakti için {mp3_file}")
    while True:
        now = datetime.now()
        if now.hour == target_hour and now.minute == target_minute:
            break
        time.sleep(10)  # Saati kontrol etmek için her 10 saniyede bir bekle
    
    print(f"Saat geldi! {prayer} vakti, Mp3 çalınıyor... {mp3_file}")
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()

    # MP3 dosyasını belirtilen süre sonra durdur
    pygame.time.wait(play_duration * 1000)  # pygame.time.wait milliseconds cinsinden çalışır
    pygame.mixer.music.stop()

    print(f"{prayer} vakti, Mp3 çalma tamamlandı.")
    pygame.mixer.quit()

# Günün namaz vakitlerini ekrana yazdırma
def print_prayer_times(prayer_times, day):
    print(f"\n{day} günü namaz vakitleri:")
    for prayer, time in prayer_times.items():
        print(f"{prayer}: {time}")

# Ana program
def main():
    global file_path, mp3_files
    
    while True:
        # Mevcut tarihi al
        today = datetime.now().strftime("%d.%m.%Y")
        data = load_prayer_times(file_path)
        
        if today in data:
            day_data = data[today]
            day_name = list(day_data.keys())[0]
            prayer_times = day_data[day_name]
            
            print_prayer_times(prayer_times, today)
            
            # Şu anki vakte göre sıradaki namaz vakitlerini belirle
            now = datetime.now()
            for prayer, time_str in prayer_times.items():
                hour, minute = map(int, time_str.split(':'))
                prayer_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
                if now < prayer_time:
                    print(f"\nŞu an {prayer} vakti sırada.")
                    # Pass target_hour and target_minute to play_mp3_at_time
                    play_mp3_at_time(prayer, mp3_files[prayer], hour, minute)
        
        # Gece yarısını bekleyip bir sonraki güne geçme
        now = datetime.now()
        next_update = (now + timedelta(days=1)).replace(hour=0, minute=1, second=0, microsecond=0)
        sleep_seconds = (next_update - now).total_seconds()
        print(f"\nGüncelleme bekleniyor: {int(sleep_seconds // 3600)} saat {int(sleep_seconds % 3600 // 60)} dakika")
        time.sleep(sleep_seconds)



if __name__ == "__main__":
    main()
