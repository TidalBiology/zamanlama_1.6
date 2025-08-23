import pygame
import pgzero
import random
import pgzrun

pgzero.game.show_default_icon = lambda: None

WIDTH = 1920
HEIGHT = 1080
m_score = 0
k_score = 0
highscore = 0
TITLE = "Zamanlama"
FPS = 60

# Aktörler
arkaplan = Actor("arkaplan")
m_ust = Actor("m_ust")
m_sag = Actor("m_sag")
m_sol = Actor("m_sol")
m_alt = Actor("m_alt")
k_sol = Actor("k_sol")
k_sag = Actor("k_sag")
k_ust = Actor("k_ust")
k_alt = Actor("k_alt")
t_alt = Actor("t_alt")
t_ust = Actor("t_ust")
t_sag = Actor("t_sag")
t_sol = Actor("t_sol")

# Oyun değişkenleri
mod = 0
m_sayi = random.randint(1,4)
k_sayi = random.randint(1,4)
death = 0
max_death = 6
time_left = 5
left_time = 3600
min_time = 2
base_time = 5
m_hata = 0
k_hata = 0
winner = ""

def draw():
    if mod == 0:
        arkaplan.draw()
        screen.draw.text("Mod seçiniz", center=(WIDTH//2, HEIGHT//2-100), color="black", fontsize=50)
        screen.draw.text("tek kişilik için Q", center=(WIDTH//2, HEIGHT//2), color="black", fontsize=50)
        screen.draw.text("çok kişilik için E", center=(WIDTH//2, HEIGHT//2+100), color="black", fontsize=50)
    
    elif mod == 1:
        if m_sayi == 1: t_ust.draw()
        elif m_sayi == 2: t_sol.draw()
        elif m_sayi == 3: t_sag.draw()
        elif m_sayi == 4: t_alt.draw()
        
        screen.draw.text(f"Skor: {m_score}", topleft=(50, 50), color="black", fontsize=45)
        screen.draw.text(f"Zaman: {time_left}", topleft=(50, 110), color="black", fontsize=45)
        screen.draw.text(f"En Yüksek Skor: {highscore}", topleft=(50, 170), color="black", fontsize=45)
        screen.draw.text(f"Hatalar: {death}/{max_death}", topleft=(50, 230), color="black", fontsize=45)
    
    elif mod == 2:
        arkaplan.draw()
        screen.draw.text("Kaybettiniz", center=(WIDTH//2, HEIGHT//2-120), color="black", fontsize=60)
        screen.draw.text("Başlatmak için SPACE", center=(WIDTH//2, HEIGHT//2), color="black", fontsize=50)
        screen.draw.text(f"Skor: {m_score}", center=(WIDTH//2, HEIGHT//2+100), color="black", fontsize=50)
        screen.draw.text(f"En Yüksek Skor: {highscore}", center=(WIDTH//2, HEIGHT//2+170), color="black", fontsize=50)
        screen.draw.text(f"Hatalar: {death}/{max_death}", center=(WIDTH//2, HEIGHT//2+240), color="black", fontsize=50)
        screen.draw.text(f"Menüye dönmek için: R", center=(WIDTH//2, HEIGHT//2+310), color="black", fontsize=50)
    
    elif mod == 3:
        # 1. Oyuncu
        if m_sayi == 1: m_ust.draw()
        elif m_sayi == 2: m_sol.draw()
        elif m_sayi == 3: m_sag.draw()
        elif m_sayi == 4: m_alt.draw()
        
        # 2. Oyuncu
        if k_sayi == 1:
            k_ust.pos = (1280, 360)
            k_ust.draw()
        elif k_sayi == 2:
            k_sol.pos = (1280, 360)
            k_sol.draw()
        elif k_sayi == 3:
            k_sag.pos = (1280, 360)
            k_sag.draw()
        elif k_sayi == 4:
            k_alt.pos = (1280, 360)
            k_alt.draw()
        
        screen.draw.text(f"Skor: {m_score}", topleft=(50, 50), color="black", fontsize=45)
        screen.draw.text(f"Skor: {k_score}", topleft=(1600, 50), color="black", fontsize=45)
        screen.draw.text(f"Hata: {m_hata}", topleft=(50, 100), color="black", fontsize=45)
        screen.draw.text(f"Hata: {k_hata}", topleft=(1600, 100), color="black", fontsize=45)
        screen.draw.text(f"Zaman: {int(left_time/60)}", center=(WIDTH//2, 50), fontsize=50, color="black")
    
    elif mod == 4:
        arkaplan.draw()
        # Hata oranlarını hesapla (KDA benzeri)
        m_kda = "∞" if m_hata == 0 else f"{m_score/m_hata:.2f}"
        k_kda = "∞" if k_hata == 0 else f"{k_score/k_hata:.2f}"
        screen.draw.text(f"{winner} Kazandı", center=(WIDTH//2, HEIGHT//2-180), color="black", fontsize=60)
        screen.draw.text("Tekrar Oyna: SPACE", center=(WIDTH//2, HEIGHT//2-90), color="black", fontsize=50)
          # 1. Oyuncu istatistikleri
        screen.draw.text(f"1.Oyuncu:", center=(WIDTH//2-300, HEIGHT//2), color="blue", fontsize=45)
        screen.draw.text(f"Skor: {m_score}", center=(WIDTH//2-300, HEIGHT//2+50), color="black", fontsize=40)
        screen.draw.text(f"Hata: {m_hata}", center=(WIDTH//2-300, HEIGHT//2+100), color="black", fontsize=40)
        screen.draw.text(f"Oran: {m_kda}", center=(WIDTH//2-300, HEIGHT//2+150), color="green", fontsize=40)
        
        # 2. Oyuncu istatistikleri
        screen.draw.text(f"2.Oyuncu:", center=(WIDTH//2+300, HEIGHT//2), color="red", fontsize=45)
        screen.draw.text(f"Skor: {k_score}", center=(WIDTH//2+300, HEIGHT//2+50), color="black", fontsize=40)
        screen.draw.text(f"Hata: {k_hata}", center=(WIDTH//2+300, HEIGHT//2+100), color="black", fontsize=40)
        screen.draw.text(f"Oran: {k_kda}", center=(WIDTH//2+300, HEIGHT//2+150), color="green", fontsize=40)
        
        screen.draw.text(f"Menüye dönmek için: R", center=(WIDTH//2, HEIGHT//2+240), color="black", fontsize=50)

def on_key_down(key):
    global mod, m_score, k_score, m_hata, k_hata, m_sayi, k_sayi, death, highscore
    
    if mod == 0:
        if key == keys.Q:
            mod = 1
            reset_single_player()
        elif key == keys.E:
            mod = 3
            reset_multi_player()
    
    elif mod == 1:
        if key == keys.UP and m_sayi == 1:
            m_score += 1
            reset_timer()
        elif key == keys.LEFT and m_sayi == 2:
            m_score += 1
            reset_timer()
        elif key == keys.RIGHT and m_sayi == 3:
            m_score += 1
            reset_timer()
        elif key == keys.DOWN and m_sayi == 4:
            m_score += 1
            reset_timer()
        elif key in (keys.UP, keys.DOWN, keys.LEFT, keys.RIGHT):
            death += 1
            if death >= max_death:
                if m_score > highscore:
                    highscore = m_score
                mod = 2
        m_sayi = random.randint(1,4)
    
    elif mod == 2:
        if key == keys.SPACE:
            reset_single_player()
            mod = 1
        elif key == keys.R:
            mod = 0
    
    elif mod == 3:
        # p1 wasd cart curt
        if key in (keys.W, keys.A, keys.D, keys.S):
            if (key == keys.W and m_sayi == 1) or \
               (key == keys.A and m_sayi == 2) or \
               (key == keys.D and m_sayi == 3) or \
               (key == keys.S and m_sayi == 4):
                m_score += 1
            else:
                m_hata += 1
            
            # Sadece 1. oyuncunun yönü değişsin
            new_m = random.randint(1,4)
            while new_m == m_sayi:
                new_m = random.randint(1,4)
            m_sayi = new_m
        
        # 2. Oyuncu (Yön tuşları)
        elif key in (keys.UP, keys.DOWN, keys.LEFT, keys.RIGHT):
            if (key == keys.UP and k_sayi == 1) or \
               (key == keys.LEFT and k_sayi == 2) or \
               (key == keys.RIGHT and k_sayi == 3) or \
               (key == keys.DOWN and k_sayi == 4):
                k_score += 1
            else:
                k_hata += 1
            
            # Sadece 2. oyuncunun yönü değişsin
            new_k = random.randint(1,4)
            while new_k == k_sayi:
                new_k = random.randint(1,4)
            k_sayi = new_k
    
    elif mod == 4:
        if key == keys.R:
            mod = 0
        elif key == keys.SPACE:
            reset_multi_player()
            mod = 3

def update(dt):
    global mod, time_left, highscore, left_time, winner
    
    if mod == 1:
        if time_left <= 0:
            if m_score > highscore:
                highscore = m_score
            mod = 2
            clock.unschedule(decrease_time)
    
    elif mod == 3:
        if left_time > 0:
            left_time -= 1
        else:
            # Hata sayısı 0 ise 1 yap (bölme hatasını önle)
            m_h = m_hata if m_hata > 0 else 1
            k_h = k_hata if k_hata > 0 else 1
            
            m_ratio = m_score / m_h
            k_ratio = k_score / k_h
            
            if m_ratio > k_ratio:
                winner = "1. Oyuncu"
            elif k_ratio > m_ratio:
                winner = "2. Oyuncu"
            else:
                winner = "Berabere"
            
            mod = 4

def start_timer():
    global time_left
    time_left = base_time
    clock.schedule_interval(decrease_time, 1.0)

def decrease_time():
    global time_left
    if time_left > 0:
        time_left -= 1
    else:
        clock.unschedule(decrease_time)

def reset_timer():
    global time_left
    time_left = base_time

def reset_single_player():
    global m_score, death, time_left
    m_score = 0
    death = 0
    time_left = base_time
    start_timer()

def reset_multi_player():
    global m_score, k_score, m_hata, k_hata, left_time, m_sayi, k_sayi
    m_score = 0
    k_score = 0
    m_hata = 0
    k_hata = 0
    left_time = 3600
    m_sayi = random.randint(1,4)
    k_sayi = random.randint(1,4)

pgzrun.go()