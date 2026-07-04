import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()

# ══════════════════════════════════════════
#  EKRAN & SABITLƏR
# ══════════════════════════════════════════
GENISLIK, HUNDURLUQ = 400, 700
ekran = pygame.display.set_mode((GENISLIK, HUNDURLUQ))
pygame.display.set_caption("🚀 Kosmik Müharibə - V2.0")

saat = pygame.time.Clock()
font_b = pygame.font.SysFont("Arial", 26, bold=True)
font_k = pygame.font.SysFont("Arial", 20)
font_bas = pygame.font.SysFont("Arial", 50, bold=True)

# ══════════════════════════════════════════
#  RƏNGLƏR
# ══════════════════════════════════════════
QA    = (0,   0,   0  )
AG    = (255, 255, 255)
YASI  = (255, 255, 0  )
QIRM  = (255, 50,  50 )
YASI2 = (50,  255, 50 )
MAVI  = (50,  150, 255)
CYAN  = (0,   255, 255)
NARN  = (255, 165, 0  )
BZK   = (100, 200, 255)

# ══════════════════════════════════════════
#  SƏS EFFEKTLƏRİ
# ══════════════════════════════════════════
try:
    atesh_sesi = pygame.mixer.Sound("laser.wav")
    partlayis_sesi = pygame.mixer.Sound("explosion.wav")
    powerup_sesi = pygame.mixer.Sound("powerup.wav")
    gameover_sesi = pygame.mixer.Sound("gameover.wav")
except:
    atesh_sesi = partlayis_sesi = powerup_sesi = gameover_sesi = None

# ══════════════════════════════════════════
#  YÜKSƏK SKOR (HIGH SCORE) FUNKSİYASI
# ══════════════════════════════════════════
def skor_oxu():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def skor_yaz(skor):
    with open("highscore.txt", "w") as f:
        f.write(str(skor))

# ══════════════════════════════════════════
#  ŞƏKİLLƏRİ YÜKLƏ
# ══════════════════════════════════════════
def yukle_sekil(ad, olcu):
    try:
        img = pygame.image.load(ad)
        return pygame.transform.scale(img, olcu)
    except:
        # Əgər şəkil tapılmazsa, ehtiyat (fallback) yaşıl gəmi yaradır
        s = pygame.Surface(olcu, pygame.SRCALPHA)
        pygame.draw.ellipse(s, (0, 220, 100), (0, 0, olcu[0], olcu[1]))
        pygame.draw.ellipse(s, (150, 255, 200), (olcu[0]//3, olcu[1]//3, olcu[0]//3, olcu[1]//3))
        return s

# ================================================================
# SİZİN GÖNDƏRDİYİNİZ ŞƏKİL BURADA İŞLƏDİLİR (ADI: uzay_gemisi.png)
# ================================================================
GEMI_IMG = yukle_sekil("uzay_gemisi.png", (54, 54))

def dushman_sekli_yarat(renk=(200,0,0)):
    s = pygame.Surface((44, 44), pygame.SRCALPHA)
    pygame.draw.ellipse(s, renk, (2, 14, 40, 20))
    pygame.draw.ellipse(s, (255, 180, 0), (14, 5, 16, 14))
    pygame.draw.circle(s, (255,50,50), (7, 26), 4)
    pygame.draw.circle(s, (255,50,50), (37, 26), 4)
    return s

def boss_sekli_yarat():
    s = pygame.Surface((110, 90), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (220, 180, 0), (5, 20, 100, 50))
    pygame.draw.ellipse(s, (255, 230, 50), (30, 5, 50, 35))
    pygame.draw.circle(s, (255, 80, 0), (10, 45), 10)
    pygame.draw.circle(s, (255, 80, 0), (100, 45), 10)
    pygame.draw.circle(s, (255, 0, 0), (55, 35), 10)
    pygame.draw.circle(s, (0, 0, 0), (55, 35), 5)
    return s

def guelle_sekli_yarat(renk, gen=6, hund=14):
    s = pygame.Surface((gen, hund), pygame.SRCALPHA)
    pygame.draw.ellipse(s, renk, (0, 0, gen, hund))
    pygame.draw.ellipse(s, AG, (gen//4, 1, gen//2, hund//4))
    return s

# Power-up şəkilləri
def powerup_sekli(renk, isare):
    s = pygame.Surface((24, 24), pygame.SRCALPHA)
    pygame.draw.circle(s, renk, (12, 12), 12)
    pygame.draw.circle(s, AG, (12, 12), 10, 2)
    label = font_k.render(isare, True, QA)
    s.blit(label, (8, 3))
    return s

PWR_TRIPLE = powerup_sekli(CYAN, "3")
PWR_HEAL   = powerup_sekli(YASI2, "+")
PWR_SHIELD = powerup_sekli(BZK, "S")

# ══════════════════════════════════════════
#  ULDUZLU ARXA FON
# ══════════════════════════════════════════
class Ulduz:
    def __init__(self):
        self.x = random.randint(0, GENISLIK)
        self.y = random.randint(0, HUNDURLUQ)
        self.olcu = random.choice([1, 1, 1, 2, 2, 3])
        self.surat = random.uniform(0.4, 2.0)

    def guncelle(self):
        self.y += self.surat
        if self.y > HUNDURLUQ:
            self.y = -5
            self.x = random.randint(0, GENISLIK)

    def ciz(self, sth):
        pygame.draw.circle(sth, AG, (int(self.x), int(self.y)), self.olcu)

ulduzlar = [Ulduz() for _ in range(180)]

# ══════════════════════════════════════════
#  PARTLAYIŞ
# ══════════════════════════════════════════
def patlayis_animasyonu_yarat():
    frames = []
    for i in range(12):
        r = int(8 + i * 3.5)
        s = pygame.Surface((r*2+4, r*2+4), pygame.SRCALPHA)
        alpha = max(0, 255 - i * 20)
        renk1 = (255, 180 - i*12, 0, alpha)
        renk2 = (255, 80,  0, max(0, alpha - 60))
        pygame.draw.circle(s, renk1, (r+2, r+2), r)
        if r > 8:
            pygame.draw.circle(s, renk2, (r+2, r+2), r - 5)
        frames.append(s)
    return frames

PATL_FRAMES = patlayis_animasyonu_yarat()

class Patlayis:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.frame = 0
        if partlayis_sesi: partlayis_sesi.play()

    def ciz(self, sth):
        if self.frame < len(PATL_FRAMES):
            img = PATL_FRAMES[self.frame]
            r = img.get_width() // 2
            sth.blit(img, (self.cx - r, self.cy - r))
            self.frame += 1
            return True
        return False

# ══════════════════════════════════════════
#  POWER-UP SINIFI
# ══════════════════════════════════════════
class PowerUp:
    def __init__(self, x, y, nov):
        self.x = x
        self.y = y
        self.nov = nov
        self.rect = pygame.Rect(x, y, 24, 24)
        self.speed = 2

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, sth):
        if self.nov == "triple":
            sth.blit(PWR_TRIPLE, (self.x, self.y))
        elif self.nov == "heal":
            sth.blit(PWR_HEAL, (self.x, self.y))
        elif self.nov == "shield":
            sth.blit(PWR_SHIELD, (self.x, self.y))

# ══════════════════════════════════════════
#  OYUN SEKILLERI
# ══════════════════════════════════════════
GUELLE_IMG  = guelle_sekli_yarat(YASI)
EB_IMG      = guelle_sekli_yarat(QIRM)
BOSS_IMG    = boss_sekli_yarat()

# ══════════════════════════════════════════
#  MENYU
# ══════════════════════════════════════════
def metn_ciz(sth, metn, font, renk, mx, my):
    g = font.render(metn, True, renk)
    sth.blit(g, (mx - g.get_width()//2, my))

def ana_menyu():
    high_score = skor_oxu()
    while True:
        ekran.fill((10, 0, 20))
        for ul in ulduzlar:
            ul.guncelle()
            ul.ciz(ekran)
        
        metn_ciz(ekran, "KOSMİK MÜHARİBƏ", font_bas, CYAN, GENISLIK//2, 200)
        metn_ciz(ekran, f"ƏN YÜKSƏK SKOR: {high_score}", font_b, YASI, GENISLIK//2, 300)
        metn_ciz(ekran, "START (ENTER)", font_b, YASI2, GENISLIK//2, 400)
        pygame.display.flip()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                return True

# ══════════════════════════════════════════
#  OYUN DƏYİŞKƏNLƏRİ
# ══════════════════════════════════════════
def oyun_reset():
    global x, y, health, score, level_speed, wave_count, enemies_killed
    global enemies, bullets, enemy_bullets, patlayislar, boss, powerups
    global atesh_gec, boss_atesh_gec, screen_shake, shake_timer
    global triple_shot_timer, shield_active, paused, wave_display_timer
    
    x, y = 173, 600
    health = 7
    score = 0
    level_speed = 2
    wave_count = 1
    enemies_killed = 0
    
    enemies = []
    bullets = []
    enemy_bullets = []
    patlayislar = []
    powerups = []
    boss = None
    atesh_gec = 0
    boss_atesh_gec = 0
    screen_shake = 0
    shake_timer = 0
    
    triple_shot_timer = 0
    shield_active = False
    paused = False
    wave_display_timer = 0 # Dalğa yazısını göstərmək üçün

# ══════════════════════════════════════════
#  ƏSAS DÖNGÜ
# ══════════════════════════════════════════

if not ana_menyu():
    pygame.quit()
    exit()

oyun_reset()
run = True
oyun_bitti_ekran = False
high_score = skor_oxu()

while run:
    saat.tick(60)

    # ── Hadisələr ──
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False
        if oyun_bitti_ekran and ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_r:
                oyun_reset()
                oyun_bitti_ekran = False
        # Fasilə (Pause) üçün ESC
        if not oyun_bitti_ekran and ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                paused = not paused

    if oyun_bitti_ekran:
        ekran.fill((10, 0, 20))
        for ul in ulduzlar:
            ul.guncelle(); ul.ciz(ekran)
        if gameover_sesi: gameover_sesi.play()
        metn_ciz(ekran, "OYUN BİTDİ", font_bas, QIRM, GENISLIK//2, 200)
        metn_ciz(ekran, f"Xal: {score}", font_b, YASI, GENISLIK//2, 270)
        metn_ciz(ekran, f"Ən Yüksək Skor: {high_score}", font_k, CYAN, GENISLIK//2, 310)
        metn_ciz(ekran, "Yenidən başlamaq üçün R bas", font_k, AG, GENISLIK//2, 350)
        pygame.display.flip()
        continue

    # ── PAUSA (FASİLƏ) ──
    if paused:
        # Pausa zamanı ekranı tündləşdir
        s = pygame.Surface((GENISLIK, HUNDURLUQ))
        s.set_alpha(150)
        s.fill((0,0,0))
        ekran.blit(s, (0,0))
        metn_ciz(ekran, "OYUN DAYANDI", font_bas, MAVI, GENISLIK//2, HUNDURLUQ//2)
        metn_ciz(ekran, "Davam etmək üçün ESC basın", font_k, AG, GENISLIK//2, HUNDURLUQ//2 + 60)
        pygame.display.flip()
        continue

    # ── MƏNTIQ ──
    level_speed = 2 + (score // 200)
    if triple_shot_timer > 0: triple_shot_timer -= 1
    
    # Dalğa dəyişikliyi yoxlaması
    if wave_display_timer > 0: wave_display_timer -= 1

    # Düşmən yaranması (Dalğa Sistemi)
    # Hər 10 düşmən öldürüləndə yeni dalğa
    if enemies_killed >= wave_count * 10:
        wave_count += 1
        level_speed += 0.5
        wave_display_timer = 90  # 1.5 saniyə yazını göstər
        enemies_killed = 0

    # Düşmən yarat (XƏTANI DÜZƏLTDİK: int() funksiyası əlavə edildi)
    dogulma_ehtimal = int(max(20, 60 - level_speed * 4))
    if random.randint(1, dogulma_ehtimal) == 1:
        nov = random.choice(["normal", "zigzag", "fast"])
        hp = 1
        sur = level_speed
        renk = (200,0,0)
        
        if nov == "zigzag":
            sur = level_speed - 1
            renk = (180, 30, 180)
        elif nov == "fast":
            sur = level_speed + 2
            renk = (0, 140, 200)
            
        enemies.append({
            "rect": pygame.Rect(random.randint(0, GENISLIK - 44), -54, 44, 44),
            "hp": hp,
            "type": nov,
            "speed": sur,
            "atesh": 0,
            "img": dushman_sekli_yarat(renk),
            "zig_x": 0
        })

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]  and x > 0:            x -= 5
    if keys[pygame.K_RIGHT] and x < GENISLIK - 54: x += 5
    if keys[pygame.K_UP]    and y > HUNDURLUQ//2:  y -= 4
    if keys[pygame.K_DOWN]  and y < HUNDURLUQ - 54:y += 4

    atesh_gec -= 1
    if keys[pygame.K_SPACE] and atesh_gec <= 0:
        if triple_shot_timer > 0:
            bullets.append(pygame.Rect(x + 24, y, 6, 14))
            bullets.append(pygame.Rect(x + 10, y + 10, 6, 14))
            bullets.append(pygame.Rect(x + 38, y + 10, 6, 14))
        else:
            bullets.append(pygame.Rect(x + 24, y, 6, 14))
        atesh_gec = 10
        if atesh_sesi: atesh_sesi.play()

    gemi_rect = pygame.Rect(x, y, 54, 54)

    # ── Boss ──
    if score >= 500 and boss is None:
        boss = {
            "rect": pygame.Rect(145, 30, 110, 90),
            "health": 20 + (score // 500) * 5,
            "max_health": 20 + (score // 500) * 5,
            "dx": 2,
            "time": 0,     # Hücum nümunəsini dəyişmək üçün
            "pattern": 0
        }

    boss_atesh_gec -= 1
    if boss:
        boss["rect"].x += boss["dx"]
        if boss["rect"].left < 0 or boss["rect"].right > GENISLIK:
            boss["dx"] *= -1
            
        boss["time"] += 1
        
        # Hər 3 saniyədə (180 frame) hücum nümunəsini dəyiş
        if boss["time"] % 180 == 0:
            boss["pattern"] = (boss["pattern"] + 1) % 3

        # YENİ BOSS HÜCUM NÜMUNƏLƏRİ
        if boss_atesh_gec <= 0:
            cx = boss["rect"].centerx
            cy = boss["rect"].bottom
            
            if boss["pattern"] == 0:  # 1. Dairəvi atəş
                for i in range(8):
                    angle = i * 45
                    rad = math.radians(angle)
                    enemy_bullets.append(pygame.Rect(cx + math.cos(rad)*30 - 5, cy + math.sin(rad)*30 - 5, 10, 10))
            elif boss["pattern"] == 1: # 2. Ardıcıl atəş
                for i in range(5):
                    enemy_bullets.append(pygame.Rect(cx - 5 + (i*20), cy, 10, 18))
            elif boss["pattern"] == 2: # 3. Dalğavari atəş
                enemy_bullets.append(pygame.Rect(cx - 50, cy, 10, 18))
                enemy_bullets.append(pygame.Rect(cx + 40, cy, 10, 18))
            
            boss_atesh_gec = max(8, 20 - score // 300)

        if boss["health"] <= 0:
            patlayislar.append(Patlayis(boss["rect"].centerx, boss["rect"].centery))
            score += 500
            boss = None
            shake_timer = 20

    # ── Düşmənlər ──
    for e in enemies[:]:
        if e["type"] == "zigzag":
            e["zig_x"] += 10
            e["rect"].x += math.sin(e["zig_x"] * 0.05) * 2
        elif e["type"] == "fast":
            e["rect"].y += e["speed"] * 1.5
        else:
            e["rect"].y += e["speed"]

        if e["rect"].colliderect(gemi_rect):
            if not shield_active:
                health -= 1
            patlayislar.append(Patlayis(e["rect"].centerx, e["rect"].centery))
            enemies.remove(e)
            shake_timer = 8
            continue

        if e["rect"].y > HUNDURLUQ:
            enemies.remove(e)
            continue

        e["atesh"] -= 1
        if e["atesh"] <= 0:
            cx = e["rect"].centerx
            cy = e["rect"].bottom
            enemy_bullets.append(pygame.Rect(cx - 4, cy, 8, 14))
            e["atesh"] = random.randint(60, 120)

    # ── Güllələr ──
    for b in bullets[:]:
        b.y -= 9
        vurulan = False

        for e in enemies[:]:
            if b.colliderect(e["rect"]) and not vurulan:
                e["hp"] -= 1
                if e["hp"] <= 0:
                    patlayislar.append(Patlayis(e["rect"].centerx, e["rect"].centery))
                    score += 10
                    enemies_killed += 1 # Dalğa üçün sayğac
                    if random.random() < 0.15:
                        p_tipi = random.choice(["triple", "heal", "shield"])
                        powerups.append(PowerUp(e["rect"].centerx, e["rect"].centery, p_tipi))
                    enemies.remove(e)
                bullets.remove(b)
                vurulan = True
                break

        if vurulan: continue
        if boss and b.colliderect(boss["rect"]):
            boss["health"] -= 1
            bullets.remove(b)
            continue
        if b.y < -14: bullets.remove(b)

    # ── Düşmən güllələri ──
    for eb in enemy_bullets[:]:
        eb.y += 6
        if eb.colliderect(gemi_rect):
            if not shield_active:
                health -= 1
            patlayislar.append(Patlayis(eb.centerx, eb.centery))
            enemy_bullets.remove(eb)
            shake_timer = 8
            continue
        if eb.y > HUNDURLUQ:
            enemy_bullets.remove(eb)

    # ── Power-uplar ──
    for p in powerups[:]:
        p.move()
        if p.rect.colliderect(gemi_rect):
            if p.nov == "triple":
                triple_shot_timer = 600
            elif p.nov == "heal":
                health = min(7, health + 2)
            elif p.nov == "shield":
                shield_active = True
            if powerup_sesi: powerup_sesi.play()
            powerups.remove(p)
        elif p.y > HUNDURLUQ:
            powerups.remove(p)

    if health <= 0:
        oyun_bitti_ekran = True
        # Yüksək skoru yadda saxla
        if score > high_score:
            high_score = score
            skor_yaz(high_score)
        continue

    # ══════════════════════════════════════
    #  ÇİZMƏ
    # ══════════════════════════════════════
    if shake_timer > 0:
        shake_timer -= 1
        ox, oy = random.randint(-5, 5), random.randint(-5, 5)
    else:
        ox, oy = 0, 0

    ekran.fill((5, 0, 15))
    for ul in ulduzlar:
        ul.guncelle(); ul.ciz(ekran)

    if boss:
        ekran.blit(BOSS_IMG, (boss["rect"].x + ox, boss["rect"].y + oy))
        bar_x, bar_y = boss["rect"].x, boss["rect"].top - 14
        pct = boss["health"] / boss["max_health"]
        pygame.draw.rect(ekran, (80,0,0), (bar_x+ox, bar_y+oy, boss["rect"].width, 8))
        pygame.draw.rect(ekran, (255,50,50), (bar_x+ox, bar_y+oy, int(boss["rect"].width*pct), 8))

    for e in enemies:
        ekran.blit(e["img"], (e["rect"].x + ox, e["rect"].y + oy))

    for b in bullets: ekran.blit(GUELLE_IMG, (b.x + ox, b.y + oy))
    for eb in enemy_bullets: ekran.blit(EB_IMG, (eb.x - 1 + ox, eb.y + oy))

    for p in powerups: p.draw(ekran)

    # ================================================================
    # SİZİN GÖNDƏRDİYİNİZ ŞƏKİL (UZAY GƏMİSİ) BURADA EKRANA ÇİZİLİR
    # ================================================================
    ekran.blit(GEMI_IMG, (x + ox, y + oy))
    
    if shield_active:
        pygame.draw.circle(ekran, (100, 200, 255), (x+27+ox, y+27+oy), 35, 3)

    for p in patlayislar[:]:
        if not p.ciz(ekran): patlayislar.remove(p)

    # ── HUD ──
    for i in range(7):
        renk = (220, 30, 60) if i < health else (50, 50, 80)
        pygame.draw.circle(ekran, renk, (22 + i * 26, 22), 9)
        if i < health: pygame.draw.circle(ekran, (255, 100, 120), (17 + i*26, 16), 4)

    xal_m = font_b.render(f"XAL: {score}", True, YASI)
    ekran.blit(xal_m, (GENISLIK - xal_m.get_width() - 10, 10))
    
    if triple_shot_timer > 0:
        metn_ciz(ekran, f"🔥 ÜÇLÜ ATƏŞ ({triple_shot_timer//60}s)", font_k, CYAN, GENISLIK//2, 45)

    # ── DALĞA EKRANI ──
    if wave_display_timer > 0:
        metn_ciz(ekran, f"— DALĞA {wave_count} —", font_bas, YASI, GENISLIK//2, HUNDURLUQ//2)

    pygame.display.flip()

pygame.quit()
