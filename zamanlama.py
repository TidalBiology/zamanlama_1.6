import pygame
import pgzero
import random
import pgzrun

pgzero.game.show_default_icon = lambda: None

WIDTH = 1920
HEIGHT = 1080
m_score = 0
k_score = 0
highscore = 0  # En yüksek skoru tutacak değişken
TITLE = "Zamanlama"  # Oyunun Adı
FPS = 60  # Saniyedeki Kare Sayısı

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
mod = 0
m_sayi = random.randint(1,4)
k_sayi = random.randint(1,4)
death = 0  # Hata sayısı
max_death = 6  # Maksimum hata sayısı
time_left = 5  # Oyuncunun kalan süresi
left_time = 3600
min_time = 2  # Süre 2 saniyenin altına düşmesin
base_time = 5  # Süre sıfırlandığında geri döneceği değer


def draw():
    if mod == 0:
        arkaplan.draw()
        screen.draw.text("Mod seçiniz", center=(WIDTH // 2, HEIGHT // 2 - 100), color="black", fontsize=50)
        screen.draw.text("tek kişilik için Q", center=(WIDTH // 2, HEIGHT // 2 ), color="black", fontsize=50)
        screen.draw.text("çok kişilik için E", center=(WIDTH // 2, HEIGHT // 2 + 100), color="black", fontsize=50)
    elif mod == 1:
        if m_sayi == 1:
            t_ust.draw()
        elif m_sayi == 2:
            t_sol.draw()
        elif m_sayi == 3:
            t_sag.draw()
        elif m_sayi == 4:
            t_alt.draw()
        # Skor, Zaman, En Yüksek Skor, ve Hatalar bölümlerinin konumları
        screen.draw.text(f"Skor: {m_score}", topleft=(50, 50), color="black", fontsize=45)
        screen.draw.text(f"Zaman: {time_left}", topleft=(50, 110), color="black", fontsize=45)
        screen.draw.text(f"En Yüksek Skor: {highscore}", topleft=(50, 170), color="black", fontsize=45)
        screen.draw.text(f"Hatalar: {death}/{max_death}", topleft=(50, 230), color="black", fontsize=45)  # Hata sayısı
    elif mod == 2:
        arkaplan.draw()
        screen.draw.text("Kaybettiniz", center=(WIDTH // 2, HEIGHT // 2 - 120), color="black", fontsize=60)
        screen.draw.text("Başlatmak için SPACE", center=(WIDTH // 2, HEIGHT // 2), color="black", fontsize=50)
        screen.draw.text(f"Skor: {m_score}", center=(WIDTH // 2, HEIGHT // 2 + 100), color="black", fontsize=50)
        screen.draw.text(f"En Yüksek Skor: {highscore}", center=(WIDTH // 2, HEIGHT // 2 + 170), color="black", fontsize=50)
        screen.draw.text(f"Hatalar: {death}/{max_death}", center=(WIDTH // 2, HEIGHT // 2 + 240), color="black", fontsize=50)  # Oyun sonunda hata sayısı
        screen.draw.text(f"Menüye dönmek için: R", center=(WIDTH // 2, HEIGHT // 2 + 310), color="black", fontsize=50)
    elif mod == 3:
        if m_sayi == 1:
            m_ust.draw()
        elif m_sayi == 2:
            m_sol.draw()
        elif m_sayi == 3:
            m_sag.draw()
        elif m_sayi == 4:
            m_alt.draw()
        
        if k_sayi == 1:
            k_ust.x = 1280
            k_ust.y= 360
            k_ust.draw()
        elif k_sayi == 2:
            k_sol.x = 1280
            k_sol.y= 360
            k_sol.draw()
        elif k_sayi == 3:
            k_sag.x = 1280
            k_sag.y= 360
            k_sag.draw()
        elif k_sayi == 4:
            k_alt.x = 1280
            k_alt.y= 360
            k_alt.draw()                    
        screen.draw.text(f"Skor: {m_score}", topleft=(50, 50), color="black", fontsize=45)
        screen.draw.text(f"Skor: {k_score}", topleft=(1600, 50), color="black", fontsize=45)  
        screen.draw.text(f"Zaman: {int(left_time/ 60) }", (840, 50), fontsize=50, color="black") 
    


def on_key_down(key):
    global m_score, m_sayi, death, mod, time_left, highscore , k_sayi , k_score

    if mod == 0 and keyboard.Q:
        mod = 1
        start_timer()  # Zamanlayıcı başlat
    elif mod == 0 and keyboard.E:
        mod = 3    
       
    elif mod == 2 :
        if keyboard.space:
            mod = 1
            reset_game()  # Oyunu sıfırla
        elif keyboard.R:
            mod = 0    

    if mod == 1:
        if keyboard.up or keyboard.right or keyboard.left or keyboard.down :

            if m_sayi == 1 and keyboard.up:
                m_score += 1
                m_sayi = random.randint(1, 4)
                reset_timer()  # Doğru tuş basılınca zamanı sıfırla
            elif m_sayi == 2 and keyboard.left:
                m_score += 1
                m_sayi = random.randint(1, 4)
                reset_timer()  # Doğru tuş basılınca zamanı sıfırla
            elif m_sayi == 3 and keyboard.right:
                m_score += 1
                m_sayi = random.randint(1, 4)
                reset_timer()  # Doğru tuş basılınca zamanı sıfırla
            elif m_sayi == 4 and keyboard.down:
                m_score += 1
                m_sayi = random.randint(1, 4)
                reset_timer()  # Doğru tuşa basılınca zamanı sıfırla
            else:
                if keyboard.space:
                    m_sayi = random.randint(1, 4)  # Hata olsa bile yeni bir yön ver
                else:
                    death += 1  # Hata sayısını artır
                    m_sayi = random.randint(1, 4)
                    if death >= max_death:  # Maksimum hataya ulaşıldığında oyunu bitir
                        if m_score > highscore:  # En yüksek skor kaydedilsin
                            highscore = m_score
                            mod = 2
        elif keyboard.space:
            m_sayi = random.randint(1, 4)                 

        # Her 30 skorda bir zaman azalması
        if  m_score % 30 == 0 and m_score != 0:
            decrease_base_time()


    if mod == 3:
        if keyboard.W or keyboard.A or keyboard.S or keyboard.D :

            if m_sayi == 1 and keyboard.W:
                m_score += 1 
                m_sayi = random.randint(1,4)  
            elif m_sayi == 2 and keyboard.A:
                m_score += 1
                m_sayi = random.randint(1,4)  
            elif m_sayi == 3 and keyboard.D:
                m_score += 1
                m_sayi = random.randint(1,4)  
            elif m_sayi == 4 and keyboard.S:
                m_score += 1
                m_sayi = random.randint(1,4)  
               
        elif keyboard.up or keyboard.right or keyboard.left or keyboard.down:
            if k_sayi == 1 and keyboard.up:
                k_score += 1
                k_sayi = random.randint(1,4)
            elif k_sayi == 2 and keyboard.left:
                k_score += 1
                k_sayi = random.randint(1,4)
            elif k_sayi == 3 and keyboard.right:
                k_score += 1
                k_sayi = random.randint(1,4)    
            elif k_sayi == 4 and keyboard.down:
                k_score += 1
                k_sayi = random.randint(1,4)  
                      



def update(dt):
    global mod, time_left, highscore ,left_time

    if mod == 1:
        if time_left <= 0:
            mod = 2
            # Skoru kontrol et ve highscore'u güncelle
            if m_score > highscore:
                highscore = m_score
            clock.unschedule(decrease_time)  # Zamanlayıcıyı durdur
    elif mod == 3:
        if left_time > 0:
            left_time -=1
                
            


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
    global m_score, death, base_time, time_left
    m_score = 0
    death = 0
    base_time = 5  # Süreyi sıfırlayınca tekrar 5'e dön
    start_timer()  # Zamanı tekrar başlat

def stop_timer():
    global left_time
    left_time = 0
clock.schedule(stop_timer, 3600)    

pgzrun.go()
