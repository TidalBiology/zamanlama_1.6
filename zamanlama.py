import pygame
import pgzero
import random
import pgzrun

pgzero.game.show_default_icon = lambda: None

WIDTH = 1280
HEIGHT = 720
score = 0
highscore = 0  # En yüksek skoru tutacak değişken
TITLE = "Zamanlama"  # Oyunun Adı
FPS = 60  # Saniyedeki Kare Sayısı

arkaplan = Actor("arkaplan")
yukari = Actor("yukari")
sol = Actor("sol")
sag = Actor("sag")
asagi = Actor("asagi")

mod = 0
sayi = random.randint(1, 4)
death = 0  # Hata sayısı
max_death = 6  # Maksimum hata sayısı
time_left = 5  # Oyuncunun kalan süresi
min_time = 2  # Süre 2 saniyenin altına düşmesin
base_time = 5  # Süre sıfırlandığında geri döneceği değer


def draw():
    if mod == 0:
        arkaplan.draw()
        screen.draw.text("Başlatmak için SPACE", center=(WIDTH // 2, HEIGHT // 2), color="black", fontsize=50)
    elif mod == 1:
        if sayi == 1:
            yukari.draw()
        elif sayi == 2:
            sol.draw()
        elif sayi == 3:
            sag.draw()
        elif sayi == 4:
            asagi.draw()
        # Skor, Zaman, En Yüksek Skor, ve Hatalar bölümlerinin konumları
        screen.draw.text(f"Skor: {score}", topleft=(50, 50), color="black", fontsize=45)
        screen.draw.text(f"Zaman: {time_left}", topleft=(50, 110), color="black", fontsize=45)
        screen.draw.text(f"En Yüksek Skor: {highscore}", topleft=(50, 170), color="black", fontsize=45)
        screen.draw.text(f"Hatalar: {death}/{max_death}", topleft=(50, 230), color="black", fontsize=45)  # Hata sayısı
    elif mod == 2:
        arkaplan.draw()
        screen.draw.text("Kaybettiniz", center=(WIDTH // 2, HEIGHT // 2 - 120), color="black", fontsize=60)
        screen.draw.text("Başlatmak için SPACE", center=(WIDTH // 2, HEIGHT // 2), color="black", fontsize=50)
        screen.draw.text(f"Skor: {score}", center=(WIDTH // 2, HEIGHT // 2 + 100), color="black", fontsize=50)
        screen.draw.text(f"En Yüksek Skor: {highscore}", center=(WIDTH // 2, HEIGHT // 2 + 170), color="black", fontsize=50)
        screen.draw.text(f"Hatalar: {death}/{max_death}", center=(WIDTH // 2, HEIGHT // 2 + 240), color="black", fontsize=50)  # Oyun sonunda hata sayısı
    


def on_key_down(key):
    global score, sayi, death, mod, time_left, highscore

    if mod == 0 and keyboard.space:
        mod = 1
        start_timer()  # Zamanlayıcı başlat
       
    elif mod == 2 and keyboard.space:
        mod = 1
        reset_game()  # Oyunu sıfırla
    

    if mod == 1:
        if sayi == 1 and keyboard.up:
            score += 1
            sayi = random.randint(1, 4)
            reset_timer()  # Doğru tuş basılınca zamanı sıfırla
        elif sayi == 2 and keyboard.left:
            score += 1
            sayi = random.randint(1, 4)
            reset_timer()  # Doğru tuş basılınca zamanı sıfırla
        elif sayi == 3 and keyboard.right:
            score += 1
            sayi = random.randint(1, 4)
            reset_timer()  # Doğru tuş basılınca zamanı sıfırla
        elif sayi == 4 and keyboard.down:
            score += 1
            sayi = random.randint(1, 4)
            reset_timer()  # Doğru tuşa basılınca zamanı sıfırla
        else:
            if keyboard.space:
                sayi = random.randint(1, 4)  # Hata olsa bile yeni bir yön ver
            else:
                death += 1  # Hata sayısını artır
                sayi = random.randint(1, 4)
                if death >= max_death:  # Maksimum hataya ulaşıldığında oyunu bitir
                    if score > highscore:  # En yüksek skor kaydedilsin
                        highscore = score
                    mod = 2

        # Her 30 skorda bir zaman azalması
        if score % 30 == 0 and score != 0:
            decrease_base_time()


def update(dt):
    global mod, time_left, highscore

    if mod == 1:
        if time_left <= 0:
            mod = 2
            # Skoru kontrol et ve highscore'u güncelle
            if score > highscore:
                highscore = score
            clock.unschedule(decrease_time)  # Zamanlayıcıyı durdur


def start_timer():
    """Zamanlayıcıyı başlat."""
    global time_left
    time_left = base_time  # Süreyi başlat
    clock.schedule_interval(decrease_time, 1.0)  # Her saniyede bir çağır


def decrease_time():
    """Zamanı azalt."""
    global time_left
    if time_left > 0:
        time_left -= 1
    else:
        clock.unschedule(decrease_time)  # Zaman sıfırlanınca durdur


def reset_timer():
    """Süreyi sıfırla."""
    global time_left
    time_left = base_time  # Doğru tuşa basılınca zaman sıfırlanır


def decrease_base_time():
    """Her 30 skorda bir süreyi 1 saniye azalt."""
    global base_time, min_time
    if base_time > min_time:
        base_time -= 1


def reset_game():
    """Oyunu sıfırla."""
    global score, death, base_time, time_left
    score = 0
    death = 0
    base_time = 5  # Süreyi sıfırlayınca tekrar 5'e dön
    start_timer()  # Zamanı tekrar başlat

pgzrun.go()
