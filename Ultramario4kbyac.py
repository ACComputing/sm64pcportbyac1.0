import pygame
import math
import sys
import random
import struct
import array
import os

# =======================================================================
# AC'S SM64 PC PORT — PYTHON EDITION 0.1
# (C) 2026 A.C Holdings / Team Flames
# 1:1 SM64 PC Port Recreation in Pure Pygame
# =======================================================================

# --- CONFIGURATION ---
WIDTH, HEIGHT = 960, 720
FPS = 30
FOV = 500
VIEW_DISTANCE = 6000

# SM64 PC Port Lakitu Camera (Third-Person)
CAM_DIST = 600
CAM_HEIGHT = 200
CAM_LERP = 0.08
CAM_ANGLE_SPEED = 0.04
CAM_PITCH_SPEED = 0.025
CAM_PITCH_MIN = -0.6
CAM_PITCH_MAX = 0.8
CAM_ZOOM_MIN = 300
CAM_ZOOM_MAX = 1200
CAM_ZOOM_STEP = 50
LAKITU_YAW_CATCHUP = 0.03

# Movement (SM64-accurate analog stick simulation)
MOVE_ACCEL = 1.6
MOVE_DECEL = 0.92
MAX_WALK_SPEED = 8
MAX_RUN_SPEED = 14
SPRINT_SPEED = 20
JUMP_FORCE = 16
DOUBLE_JUMP_FORCE = 22
TRIPLE_JUMP_FORCE = 30
LONG_JUMP_FORCE_Y = 12
LONG_JUMP_FORCE_XZ = 22
BACKFLIP_FORCE = 26
SIDE_FLIP_FORCE = 24
WALL_KICK_FORCE = 18
GROUND_POUND_SPEED = -28
DIVE_FORCE_Y = 6
DIVE_FORCE_XZ = 18
GRAVITY = 0.9
TERMINAL_VELOCITY = -60
FALL_DAMAGE_THRESHOLD = -40
STAR_TOTAL = 120

# =====================================================================
# SM64 PC PORT COLOR PALETTES (sourced from actual texture/vertex data)
# =====================================================================
# Castle Grounds
CG_GRASS_1 = (0, 154, 0)
CG_GRASS_2 = (0, 120, 0)
CG_PATH = (200, 176, 128)
CG_STONE = (168, 168, 152)
CG_MOAT = (0, 80, 180)
CG_MOAT_DEEP = (0, 50, 140)
CG_CASTLE_WALL = (232, 216, 176)
CG_CASTLE_ROOF = (200, 48, 48)
CG_CASTLE_TRIM = (248, 232, 176)
CG_TREE_TRUNK = (104, 64, 24)
CG_TREE_TOP = (0, 120, 24)
CG_TREE_TOP2 = (0, 88, 8)
CG_BRIDGE = (136, 96, 48)
CG_TOWER = (232, 208, 168)

# Bob-omb Battlefield
BOB_GRASS_1 = (0, 168, 0)
BOB_GRASS_2 = (0, 128, 0)
BOB_DIRT = (184, 136, 72)
BOB_PATH = (200, 176, 120)
BOB_MTN_LOW = (144, 104, 56)
BOB_MTN_MID = (128, 96, 48)
BOB_MTN_TOP = (152, 144, 128)
BOB_WATER = (24, 88, 200)
BOB_FENCE = (168, 136, 80)
BOB_SKY_TOP = (80, 144, 248)
BOB_SKY_BOT = (184, 216, 248)

# Whomp's Fortress
WF_STONE_1 = (184, 176, 160)
WF_STONE_2 = (152, 144, 128)
WF_GRASS = (0, 136, 0)
WF_BRICK = (176, 152, 112)
WF_DIRT = (160, 120, 64)

# Jolly Roger Bay
JRB_WATER = (0, 72, 200)
JRB_WATER_DEEP = (0, 40, 140)
JRB_SAND = (224, 200, 152)
JRB_CAVE = (80, 72, 64)
JRB_SHIP = (120, 80, 40)
JRB_CORAL = (200, 100, 120)
JRB_DOCK = (144, 104, 56)

# Cool Cool Mountain
CCM_SNOW_1 = (240, 248, 255)
CCM_SNOW_2 = (208, 224, 240)
CCM_ICE = (160, 200, 248)
CCM_ROCK = (136, 128, 120)
CCM_CABIN = (120, 72, 32)
CCM_SLIDE = (176, 208, 248)

# Big Boo's Haunt
BBH_WALL = (96, 80, 96)
BBH_FLOOR = (64, 56, 64)
BBH_ROOF = (72, 64, 72)
BBH_BRICK = (112, 96, 80)
BBH_GHOST = (216, 216, 232)
BBH_FENCE = (80, 72, 64)
BBH_GRAVE = (128, 120, 112)
BBH_WINDOW = (120, 168, 80)

# Hazy Maze Cave
HMC_ROCK_1 = (104, 88, 72)
HMC_ROCK_2 = (80, 64, 48)
HMC_TOXIC = (72, 120, 24)
HMC_METAL = (160, 168, 176)
HMC_WATER = (32, 64, 160)

# Lethal Lava Land
LLL_LAVA_1 = (232, 80, 0)
LLL_LAVA_2 = (248, 136, 0)
LLL_STONE = (96, 80, 64)
LLL_METAL = (136, 128, 120)
LLL_VOLCANO = (80, 56, 32)

# Shifting Sand Land
SSL_SAND_1 = (232, 200, 136)
SSL_SAND_2 = (208, 176, 112)
SSL_PYRAMID = (216, 184, 120)
SSL_BRICK = (184, 152, 96)
SSL_QUICKSAND = (192, 160, 88)
SSL_OASIS = (32, 96, 200)
SSL_PALM = (80, 144, 24)

# Dire Dire Docks
DDD_WATER = (0, 48, 160)
DDD_WATER_DEEP = (0, 24, 100)
DDD_DOCK = (144, 104, 56)
DDD_METAL = (144, 152, 168)
DDD_SUB = (112, 120, 128)
DDD_FLOOR = (72, 64, 56)

# Snowman's Land
SL_SNOW_1 = (240, 248, 255)
SL_SNOW_2 = (200, 216, 232)
SL_ICE = (144, 192, 248)
SL_IGLOO = (232, 240, 248)

# Wet-Dry World
WDW_BRICK = (184, 168, 144)
WDW_WATER = (48, 112, 216)
WDW_STONE = (160, 152, 136)
WDW_SWITCH = (168, 48, 200)

# Tall Tall Mountain
TTM_GRASS = (0, 152, 0)
TTM_DIRT = (152, 112, 56)
TTM_ROCK = (128, 120, 104)
TTM_SLIDE = (144, 104, 56)
TTM_WATER = (48, 120, 224)
TTM_MUSH_TOP = (216, 48, 48)
TTM_MUSH_STEM = (232, 216, 176)

# Tiny-Huge Island
THI_GRASS_1 = (0, 168, 0)
THI_GRASS_2 = (0, 120, 16)
THI_WATER = (24, 88, 200)
THI_BEACH = (216, 192, 144)
THI_PIPE = (0, 176, 0)

# Tick Tock Clock
TTC_WOOD = (168, 120, 56)
TTC_GEAR = (200, 176, 56)
TTC_METAL = (176, 184, 192)
TTC_HAND = (80, 72, 64)

# Rainbow Ride
RR_RAINBOW = [(248,56,56),(248,152,40),(248,232,40),(48,200,48),(56,104,248),(152,48,200)]
RR_CLOUD = (248, 248, 255)
RR_CARPET = (152, 48, 200)
RR_HOUSE = (232, 216, 176)

# Bowser levels
BDW_STONE = (80, 64, 80)
BDW_LAVA = (232, 80, 0)
BFS_METAL = (128, 136, 144)
BITS_STONE = (96, 80, 96)

# Universal
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (0, 0, 205)
SKIN = (255, 204, 153)
BROWN = (139, 69, 19)
MUSTACHE_BLACK = (20, 20, 20)
BUTTON_GOLD = (255, 215, 0)
EYE_BLUE = (0, 128, 255)
YELLOW = (255, 255, 0)
METAL_GREY = (160, 170, 180)
ORANGE = (255, 140, 0)
DARK_GREEN = (20, 80, 20)
DARK_GREY = (80, 80, 80)
LIGHT_GREY = (200, 200, 200)
DARK_BROWN = (80, 40, 10)
DARK_STONE = (100, 100, 100)
PURPLE = (120, 40, 180)
PIPE_GREEN = (0, 176, 0)
CARPET_RED = (160, 20, 30)

# Mario Model Colors (SM64 accurate)
MARIO_CAP = (255, 0, 0)
MARIO_SHIRT = (255, 0, 0)
MARIO_OVERALLS = (0, 0, 200)
MARIO_SKIN = (254, 193, 121)
MARIO_HAIR = (80, 32, 0)
MARIO_SHOES = (114, 56, 14)
MARIO_GLOVES = (255, 255, 255)
MARIO_BUTTONS = (255, 215, 0)
MARIO_M_EMBLEM = (255, 255, 255)

# =====================================================================
# SM64 SKY DEFINITIONS (top gradient, bottom gradient, fog color)
# =====================================================================
SM64_SKIES = {
    "castle_grounds": ((80, 152, 248), (184, 224, 248), (200, 220, 248)),
    "castle_f1":      ((48, 40, 32), (80, 72, 56), (60, 52, 40)),
    "castle_basement":((16, 12, 8), (32, 24, 16), (20, 16, 8)),
    "castle_upper":   ((56, 48, 40), (88, 80, 64), (64, 56, 44)),
    "castle_top":     ((160, 192, 248), (224, 236, 248), (200, 220, 248)),
    "c01_bob":        ((80, 144, 248), (184, 216, 248), (160, 200, 240)),
    "c02_whomp":      ((88, 152, 240), (176, 208, 240), (152, 192, 232)),
    "c03_jolly":      ((32, 72, 168), (80, 128, 200), (56, 96, 176)),
    "c04_cool":       ((128, 176, 248), (216, 232, 248), (192, 216, 248)),
    "c05_boo":        ((8, 4, 16), (24, 16, 32), (16, 8, 24)),
    "c06_hazy":       ((16, 16, 16), (32, 28, 24), (24, 20, 16)),
    "c07_lava":       ((40, 8, 0), (80, 24, 0), (56, 16, 0)),
    "c08_sand":       ((168, 152, 112), (216, 200, 160), (192, 176, 136)),
    "c09_dock":       ((16, 32, 96), (48, 72, 144), (32, 48, 120)),
    "c10_snow":       ((128, 176, 240), (208, 224, 248), (176, 200, 240)),
    "c11_wet":        ((104, 144, 200), (176, 200, 232), (144, 176, 216)),
    "c12_tall":       ((72, 136, 240), (168, 208, 248), (128, 176, 240)),
    "c13_tiny":       ((80, 152, 248), (184, 216, 248), (144, 192, 240)),
    "c14_clock":      ((32, 24, 16), (64, 48, 32), (48, 36, 24)),
    "c15_rainbow":    ((72, 112, 248), (160, 192, 248), (120, 152, 248)),
    "s_slide":        ((48, 40, 32), (80, 72, 56), (60, 52, 40)),
    "s_wing":         ((96, 144, 248), (192, 216, 248), (152, 184, 248)),
    "s_metal":        ((8, 8, 8), (24, 20, 16), (16, 12, 8)),
    "s_vanish":       ((16, 24, 48), (40, 56, 96), (28, 40, 72)),
    "s_tower":        ((128, 176, 248), (224, 240, 248), (192, 216, 248)),
    "b1_dark":        ((8, 0, 16), (24, 8, 32), (16, 4, 24)),
    "b2_fire":        ((32, 4, 0), (72, 16, 0), (48, 8, 0)),
    "b3_sky":         ((48, 32, 72), (96, 72, 128), (72, 48, 96)),
}


# =====================================================================
# SM64 PC PORT SOUND ENGINE (Synthesized waveforms)
# =====================================================================
class SM64Audio:
    """SM64 PC Port authentic sound synthesis"""
    def __init__(self):
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
        except:
            self.enabled = False
        self.sounds = {}
        if self.enabled:
            self._generate_sounds()

    def _make_sound(self, freq, duration, wave='square', volume=0.3, decay=True):
        """Generate a sound waveform"""
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = array.array('h', [0] * n_samples)
        for i in range(n_samples):
            t = i / sample_rate
            env = 1.0 - (i / n_samples) if decay else 1.0
            if wave == 'square':
                val = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
            elif wave == 'triangle':
                val = 2.0 * abs(2.0 * (t * freq - math.floor(t * freq + 0.5))) - 1.0
            elif wave == 'noise':
                val = random.uniform(-1, 1)
            else:
                val = math.sin(2 * math.pi * freq * t)
            buf[i] = int(val * volume * env * 32767)
        try:
            sound = pygame.mixer.Sound(buffer=buf)
            return sound
        except:
            return None

    def _generate_sounds(self):
        # SM64 jump sound (ascending chirp)
        s = self._make_sound(520, 0.12, 'triangle', 0.25)
        if s: self.sounds['jump'] = s
        # Double jump (higher)
        s = self._make_sound(680, 0.14, 'triangle', 0.28)
        if s: self.sounds['double_jump'] = s
        # Triple jump (highest + longer)
        s = self._make_sound(880, 0.2, 'triangle', 0.3)
        if s: self.sounds['triple_jump'] = s
        # Coin collect
        s = self._make_sound(988, 0.08, 'square', 0.2)
        if s: self.sounds['coin'] = s
        # Star collect fanfare (arpeggio simulated)
        sr = 22050
        n = int(sr * 0.8)
        buf = array.array('h', [0] * n)
        notes = [523, 659, 784, 1047, 784, 1047, 1319]
        note_len = n // len(notes)
        for ni, freq in enumerate(notes):
            for i in range(note_len):
                idx = ni * note_len + i
                if idx < n:
                    t = i / sr
                    env = 1.0 - (i / note_len) * 0.3
                    val = math.sin(2 * math.pi * freq * t) * 0.4
                    val += (1.0 if math.sin(2 * math.pi * freq * 1.5 * t) >= 0 else -1.0) * 0.15
                    buf[idx] = int(val * env * 32767)
        try:
            self.sounds['star'] = pygame.mixer.Sound(buffer=buf)
        except:
            pass
        # Ground pound
        s = self._make_sound(120, 0.15, 'square', 0.35)
        if s: self.sounds['ground_pound'] = s
        # Long jump
        s = self._make_sound(440, 0.18, 'triangle', 0.25)
        if s: self.sounds['long_jump'] = s
        # Backflip
        s = self._make_sound(600, 0.22, 'triangle', 0.25)
        if s: self.sounds['backflip'] = s
        # Wall kick
        s = self._make_sound(700, 0.1, 'square', 0.2)
        if s: self.sounds['wall_kick'] = s
        # Dive
        s = self._make_sound(300, 0.15, 'noise', 0.15)
        if s: self.sounds['dive'] = s
        # Painting enter (warble)
        sr2 = 22050
        n2 = int(sr2 * 0.5)
        buf2 = array.array('h', [0] * n2)
        for i in range(n2):
            t = i / sr2
            freq2 = 200 + math.sin(t * 30) * 100
            val2 = math.sin(2 * math.pi * freq2 * t) * 0.3 * (1.0 - i / n2)
            buf2[i] = int(val2 * 32767)
        try:
            self.sounds['painting'] = pygame.mixer.Sound(buffer=buf2)
        except:
            pass
        # Menu select
        s = self._make_sound(660, 0.06, 'square', 0.15)
        if s: self.sounds['menu_select'] = s
        # Menu cursor
        s = self._make_sound(440, 0.04, 'square', 0.1)
        if s: self.sounds['menu_cursor'] = s
        # Hurt
        s = self._make_sound(200, 0.2, 'square', 0.3, decay=True)
        if s: self.sounds['hurt'] = s
        # 1-UP
        sr3 = 22050
        n3 = int(sr3 * 0.4)
        buf3 = array.array('h', [0] * n3)
        up_notes = [523, 659, 784, 1047]
        up_len = n3 // len(up_notes)
        for ni, freq in enumerate(up_notes):
            for i in range(up_len):
                idx = ni * up_len + i
                if idx < n3:
                    t = i / sr3
                    val = math.sin(2 * math.pi * freq * t) * 0.3
                    buf3[idx] = int(val * 32767)
        try:
            self.sounds['oneup'] = pygame.mixer.Sound(buffer=buf3)
        except:
            pass

    def play(self, name):
        if self.enabled and name in self.sounds:
            try:
                self.sounds[name].play()
            except:
                pass


# =====================================================================
# 3D ENGINE
# =====================================================================
class Vector3:
    __slots__ = ['x','y','z']
    def __init__(self, x, y, z):
        self.x=x; self.y=y; self.z=z

class Face:
    __slots__ = ['indices','color','avg_z','normal']
    def __init__(self, indices, color):
        self.indices=indices; self.color=color; self.avg_z=0; self.normal=None

class Mesh:
    def __init__(self, x=0, y=0, z=0):
        self.x=x; self.y=y; self.z=z
        self.vertices=[]; self.faces=[]; self.yaw=0

    def add_cube(self, w, h, d, ox, oy, oz, color):
        si = len(self.vertices)
        hw,hh,hd = w/2,h/2,d/2
        for cx,cy,cz in [(-hw,-hh,-hd),(hw,-hh,-hd),(hw,hh,-hd),(-hw,hh,-hd),
                          (-hw,-hh,hd),(hw,-hh,hd),(hw,hh,hd),(-hw,hh,hd)]:
            self.vertices.append(Vector3(cx+ox,cy+oy,cz+oz))
        for fi,fc in [([0,1,2,3],color),([5,4,7,6],color),([4,0,3,7],color),
                       ([1,5,6,2],color),([3,2,6,7],color),([4,5,1,0],color)]:
            shifted=[i+si for i in fi]; face=Face(shifted,fc)
            v0,v1,v2=self.vertices[shifted[0]],self.vertices[shifted[1]],self.vertices[shifted[2]]
            ax,ay,az=v1.x-v0.x,v1.y-v0.y,v1.z-v0.z
            bx,by,bz=v2.x-v0.x,v2.y-v0.y,v2.z-v0.z
            nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
            l=math.sqrt(nx*nx+ny*ny+nz*nz)
            face.normal=(nx/l,ny/l,nz/l) if l!=0 else (0,0,1)
            self.faces.append(face)

    def add_pyramid(self, bw, height, ox, oy, oz, color):
        si=len(self.vertices); hw=bw/2
        for cx,cz in [(-hw,-hw),(hw,-hw),(hw,hw),(-hw,hw)]:
            self.vertices.append(Vector3(cx+ox,oy,cz+oz))
        self.vertices.append(Vector3(ox,oy+height,oz))
        for tri in [(0,1,4),(1,2,4),(2,3,4),(3,0,4)]:
            f=Face([si+t for t in tri],color); f.normal=(0,0.7,0.7); self.faces.append(f)

    def add_slope(self, w, d, h_front, h_back, ox, oy, oz, color):
        si=len(self.vertices); hw,hd=w/2,d/2
        self.vertices.append(Vector3(-hw+ox,oy,-hd+oz))
        self.vertices.append(Vector3( hw+ox,oy,-hd+oz))
        self.vertices.append(Vector3( hw+ox,oy, hd+oz))
        self.vertices.append(Vector3(-hw+ox,oy, hd+oz))
        self.vertices.append(Vector3(-hw+ox,oy+h_back,-hd+oz))
        self.vertices.append(Vector3( hw+ox,oy+h_back,-hd+oz))
        self.vertices.append(Vector3( hw+ox,oy+h_front, hd+oz))
        self.vertices.append(Vector3(-hw+ox,oy+h_front, hd+oz))
        f=Face([si+4,si+5,si+6,si+7],color); f.normal=(0,1,0); self.faces.append(f)
        f=Face([si+3,si+2,si+6,si+7],color); f.normal=(0,0,1); self.faces.append(f)
        f=Face([si+1,si+0,si+4,si+5],color); f.normal=(0,0,-1); self.faces.append(f)
        f=Face([si+0,si+3,si+7,si+4],color); f.normal=(-1,0,0); self.faces.append(f)
        f=Face([si+2,si+1,si+5,si+6],color); f.normal=(1,0,0); self.faces.append(f)

    def add_hill(self, radius, height, ox, oy, oz, color, color2=None, segments=8):
        if color2 is None: color2 = color
        si = len(self.vertices)
        self.vertices.append(Vector3(ox, oy+height, oz))
        for i in range(segments):
            a = 2*math.pi*i/segments
            self.vertices.append(Vector3(ox+math.cos(a)*radius, oy, oz+math.sin(a)*radius))
        for i in range(segments):
            a = 2*math.pi*i/segments
            self.vertices.append(Vector3(ox+math.cos(a)*radius*0.6, oy+height*0.7, oz+math.sin(a)*radius*0.6))
        for i in range(segments):
            j=(i+1)%segments
            f=Face([si, si+1+segments+i, si+1+segments+j], color)
            f.normal=(0,1,0); self.faces.append(f)
        for i in range(segments):
            j=(i+1)%segments
            f=Face([si+1+i, si+1+j, si+1+segments+j, si+1+segments+i], color2)
            f.normal=(0,0.5,0.5); self.faces.append(f)


# =====================================================================
# MARIO CHARACTER — SM64 PC Port Accurate Model + Physics
# =====================================================================
# Action states (matching sm64 action IDs conceptually)
ACT_IDLE = 0
ACT_WALKING = 1
ACT_RUNNING = 2
ACT_JUMP = 3
ACT_DOUBLE_JUMP = 4
ACT_TRIPLE_JUMP = 5
ACT_LONG_JUMP = 6
ACT_BACKFLIP = 7
ACT_SIDE_FLIP = 8
ACT_WALL_KICK = 9
ACT_GROUND_POUND = 10
ACT_GROUND_POUND_LAND = 11
ACT_DIVE = 12
ACT_DIVE_SLIDE = 13
ACT_CROUCH = 14
ACT_CRAWL = 15
ACT_FREEFALL = 16
ACT_SLIDE = 17
ACT_STAR_DANCE = 18
ACT_HURT = 19
ACT_DEATH = 20

class Mario(Mesh):
    def __init__(self, x, y, z):
        super().__init__(x,y,z)
        self.dy = 0
        self.dx = 0
        self.dz = 0
        self.speed = 0
        self.action = ACT_IDLE
        self.action_timer = 0
        self.jump_count = 0  # For triple jump chain
        self.jump_chain_timer = 0
        self.face_yaw = 0  # Direction Mario faces
        self.lives = 4
        self.health = 8
        self.coins = 0
        self.star_count = 0
        self.invincible_timer = 0
        self.anim_frame = 0
        self.anim_timer = 0
        self.ground_pound_started = False
        self._build_model()

    def _build_model(self):
        """Build SM64 Mario model — red cap, blue overalls, skin, shoes"""
        self.vertices = []
        self.faces = []
        # === HEAD ===
        self.add_cube(18, 16, 18, 0, 52, 0, MARIO_SKIN)          # head
        # === CAP ===
        self.add_cube(20, 6, 20, 0, 62, 0, MARIO_CAP)            # cap body
        self.add_cube(10, 3, 6, 0, 56, 12, MARIO_CAP)             # cap brim
        # M emblem on cap
        self.add_cube(5, 5, 1, 0, 63, 11, MARIO_M_EMBLEM)
        # === EYES ===
        self.add_cube(4, 5, 2, -5, 54, 10, WHITE)                 # left eye white
        self.add_cube(4, 5, 2, 5, 54, 10, WHITE)                  # right eye white
        self.add_cube(2, 3, 1, -5, 54, 11, EYE_BLUE)              # left pupil
        self.add_cube(2, 3, 1, 5, 54, 11, EYE_BLUE)               # right pupil
        # === NOSE ===
        self.add_cube(5, 4, 5, 0, 50, 11, MARIO_SKIN)
        # === MUSTACHE ===
        self.add_cube(12, 3, 2, 0, 47, 10, MUSTACHE_BLACK)
        # === HAIR (back/sides) ===
        self.add_cube(20, 8, 4, 0, 52, -10, MARIO_HAIR)
        self.add_cube(4, 12, 16, -10, 50, -2, MARIO_HAIR)         # left sideburn
        self.add_cube(4, 12, 16, 10, 50, -2, MARIO_HAIR)          # right sideburn
        # === TORSO ===
        self.add_cube(16, 14, 10, 0, 36, 0, MARIO_SHIRT)          # red shirt
        self.add_cube(16, 10, 10, 0, 24, 0, MARIO_OVERALLS)       # blue overalls
        # Overall straps
        self.add_cube(3, 14, 4, -5, 36, 0, MARIO_OVERALLS)        # left strap
        self.add_cube(3, 14, 4, 5, 36, 0, MARIO_OVERALLS)         # right strap
        # Buttons
        self.add_cube(2, 2, 2, -4, 32, 6, MARIO_BUTTONS)
        self.add_cube(2, 2, 2, 4, 32, 6, MARIO_BUTTONS)
        # === ARMS ===
        self.add_cube(6, 12, 6, -13, 36, 0, MARIO_SHIRT)          # left upper arm
        self.add_cube(6, 12, 6, 13, 36, 0, MARIO_SHIRT)           # right upper arm
        # Gloves
        self.add_cube(5, 6, 5, -13, 26, 0, MARIO_GLOVES)          # left glove
        self.add_cube(5, 6, 5, 13, 26, 0, MARIO_GLOVES)           # right glove
        # === LEGS ===
        self.add_cube(6, 12, 6, -5, 12, 0, MARIO_OVERALLS)        # left leg
        self.add_cube(6, 12, 6, 5, 12, 0, MARIO_OVERALLS)         # right leg
        # === SHOES ===
        self.add_cube(7, 5, 9, -5, 3, 1, MARIO_SHOES)             # left shoe
        self.add_cube(7, 5, 9, 5, 3, 1, MARIO_SHOES)              # right shoe

    def is_airborne(self):
        return self.action in (ACT_JUMP, ACT_DOUBLE_JUMP, ACT_TRIPLE_JUMP,
                               ACT_LONG_JUMP, ACT_BACKFLIP, ACT_SIDE_FLIP,
                               ACT_WALL_KICK, ACT_GROUND_POUND, ACT_DIVE,
                               ACT_FREEFALL)

    def is_on_ground(self):
        return not self.is_airborne()

    def do_jump(self, audio):
        """SM64 jump chain: single -> double -> triple"""
        if self.action == ACT_CROUCH:
            # Backflip from crouch
            self.action = ACT_BACKFLIP
            self.dy = BACKFLIP_FORCE
            self.jump_count = 0
            audio.play('backflip')
            return

        if self.jump_chain_timer > 0 and self.speed > 4:
            self.jump_count += 1
        else:
            self.jump_count = 1

        if self.jump_count >= 3 and self.speed > 8:
            self.action = ACT_TRIPLE_JUMP
            self.dy = TRIPLE_JUMP_FORCE
            audio.play('triple_jump')
            self.jump_count = 0
        elif self.jump_count == 2 and self.speed > 4:
            self.action = ACT_DOUBLE_JUMP
            self.dy = DOUBLE_JUMP_FORCE
            audio.play('double_jump')
        else:
            self.action = ACT_JUMP
            self.dy = JUMP_FORCE
            self.jump_count = 1
            audio.play('jump')
        self.jump_chain_timer = 12

    def do_long_jump(self, audio):
        self.action = ACT_LONG_JUMP
        self.dy = LONG_JUMP_FORCE_Y
        forward_x = -math.sin(self.face_yaw)
        forward_z = -math.cos(self.face_yaw)
        self.dx = forward_x * LONG_JUMP_FORCE_XZ
        self.dz = forward_z * LONG_JUMP_FORCE_XZ
        audio.play('long_jump')

    def do_ground_pound(self, audio):
        if self.is_airborne() and self.action != ACT_GROUND_POUND:
            self.action = ACT_GROUND_POUND
            self.dy = 8  # Brief upward before slam
            self.dx = 0
            self.dz = 0
            self.ground_pound_started = False
            self.action_timer = 8
            audio.play('ground_pound')

    def do_dive(self, audio):
        if self.is_airborne():
            self.action = ACT_DIVE
            forward_x = -math.sin(self.face_yaw)
            forward_z = -math.cos(self.face_yaw)
            self.dy = DIVE_FORCE_Y
            self.dx = forward_x * DIVE_FORCE_XZ
            self.dz = forward_z * DIVE_FORCE_XZ
            audio.play('dive')

    def do_side_flip(self, audio):
        self.action = ACT_SIDE_FLIP
        self.dy = SIDE_FLIP_FORCE
        self.face_yaw += math.pi
        audio.play('backflip')

    def take_damage(self, audio, amount=1):
        if self.invincible_timer > 0:
            return
        self.health = max(0, self.health - amount)
        self.invincible_timer = 60
        audio.play('hurt')
        if self.health <= 0:
            self.action = ACT_DEATH
            self.lives -= 1

    def update(self, floor_y=0):
        self.anim_timer += 1
        if self.anim_timer >= 8:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.jump_chain_timer > 0:
            self.jump_chain_timer -= 1

        if self.action_timer > 0:
            self.action_timer -= 1

        # Ground pound hover then slam
        if self.action == ACT_GROUND_POUND:
            if self.action_timer > 0:
                self.dy = max(0, self.dy - 2)
            else:
                if not self.ground_pound_started:
                    self.ground_pound_started = True
                    self.dy = GROUND_POUND_SPEED

        # Gravity
        if self.is_airborne():
            self.dy -= GRAVITY
            if self.dy < TERMINAL_VELOCITY:
                self.dy = TERMINAL_VELOCITY

        self.y += self.dy

        # Ground collision
        if self.y <= floor_y:
            # Fall damage check
            if self.dy < FALL_DAMAGE_THRESHOLD and self.action != ACT_GROUND_POUND:
                self.health = max(0, self.health - 1)

            self.y = floor_y
            if self.is_airborne():
                if self.action == ACT_GROUND_POUND:
                    self.action = ACT_GROUND_POUND_LAND
                    self.action_timer = 15
                elif self.action == ACT_DIVE:
                    self.action = ACT_DIVE_SLIDE
                    self.action_timer = 30
                elif self.action == ACT_LONG_JUMP:
                    self.action = ACT_IDLE
                    self.dx *= 0.3
                    self.dz *= 0.3
                else:
                    self.action = ACT_IDLE
                self.dy = 0

        # Dive slide friction
        if self.action == ACT_DIVE_SLIDE:
            self.dx *= 0.94
            self.dz *= 0.94
            self.x += self.dx
            self.z += self.dz
            if self.action_timer <= 0 or (abs(self.dx) < 0.5 and abs(self.dz) < 0.5):
                self.action = ACT_IDLE

        # Ground pound land lockout
        if self.action == ACT_GROUND_POUND_LAND:
            if self.action_timer <= 0:
                self.action = ACT_IDLE

        # Long jump / dive forward momentum
        if self.action in (ACT_LONG_JUMP, ACT_DIVE):
            self.x += self.dx
            self.z += self.dz
            self.dx *= 0.98
            self.dz *= 0.98

        # Star dance
        if self.action == ACT_STAR_DANCE:
            self.face_yaw += 0.15

        self.speed = math.sqrt(self.dx*self.dx + self.dz*self.dz)


# =====================================================================
# COLLECTIBLES
# =====================================================================
class Star(Mesh):
    def __init__(self, x, y, z, sid=0):
        super().__init__(x,y,z); self.star_id=sid; self.collected=False
        self.add_cube(10,40,10,0,0,0,YELLOW)
        self.add_cube(40,10,10,0,0,0,YELLOW)
        self.add_cube(10,10,40,0,0,0,YELLOW)
        # Star sparkle tips
        self.add_cube(6,6,6, 0,24,0, WHITE)
        self.add_cube(6,6,6, 0,-24,0, WHITE)
        self.add_cube(6,6,6, 24,0,0, WHITE)
        self.add_cube(6,6,6, -24,0,0, WHITE)

class Coin(Mesh):
    def __init__(self, x, y, z):
        super().__init__(x,y,z); self.collected=False
        self.add_cube(8,12,3,0,0,0,YELLOW)
        self.add_cube(4,8,4,0,0,0,BUTTON_GOLD)

class RedCoin(Mesh):
    def __init__(self, x, y, z):
        super().__init__(x,y,z); self.collected=False
        self.add_cube(8,12,3,0,0,0,RED)
        self.add_cube(4,8,4,0,0,0,(180,20,20))

class BlueCoin(Mesh):
    def __init__(self, x, y, z):
        super().__init__(x,y,z); self.collected=False
        self.add_cube(8,12,3,0,0,0,BLUE)
        self.add_cube(4,8,4,0,0,0,(60,60,200))


# =====================================================================
# SM64 PC PORT LEVEL BUILDERS — AUTHENTIC OUTDOOR GEOMETRY
# =====================================================================

def build_castle_grounds():
    m = Mesh()
    tile = 240
    for x in range(-8,8):
        for z in range(-8,8):
            c = CG_GRASS_1 if (x+z)%2==0 else CG_GRASS_2
            h = math.sin(x*0.5)*4 + math.cos(z*0.7)*3
            m.add_cube(tile,12,tile, x*tile, -6+h, z*tile, c)
    for z in range(-6,0):
        m.add_cube(160,4,tile, 0,0,z*tile, CG_PATH)
    for i in range(-4,5):
        for side in [-1,1]:
            m.add_cube(tile,8,tile, i*tile,-4, side*900, CG_MOAT)
            m.add_cube(tile,8,tile, side*900,-4, i*tile, CG_MOAT)
    m.add_cube(400,4,400, 0,-8, -900, CG_MOAT_DEEP)
    m.add_cube(180,16,480, 0,4,-640, CG_BRIDGE)
    for side in [-80,80]:
        for z in range(-3,3):
            m.add_cube(12,40,12, side,24,-640+z*80, CG_BRIDGE)
        m.add_cube(12,8,480, side,44,-640, CG_BRIDGE)
    m.add_cube(640,360,80, 0,180,-1050, CG_CASTLE_WALL)
    for tx in [-380,380]:
        m.add_cube(120,480,120, tx,240,-1050, CG_TOWER)
        m.add_pyramid(140,100, tx,480,-1050, CG_CASTLE_ROOF)
        m.add_cube(30,40,5, tx,360,-988, (120,180,248))
        m.add_cube(30,40,5, tx,280,-988, (120,180,248))
    m.add_cube(160,520,120, 0,260,-1100, CG_CASTLE_WALL)
    m.add_pyramid(180,120, 0,520,-1100, CG_CASTLE_ROOF)
    m.add_cube(100,160,8, 0,80,-1008, (104,72,32))
    m.add_cube(120,20,12, 0,160,-1008, CG_CASTLE_TRIM)
    m.add_cube(80,96,5, 0,320,-1008, (248,180,200))
    for wx in [-160,160]:
        m.add_cube(48,56,5, wx,280,-1008, (120,180,248))
    m.add_cube(640,20,200, 0,360,-1090, CG_CASTLE_ROOF)
    m.add_cube(680,20,100, 0,10,-1050, CG_STONE)
    m.add_hill(400,180, -1200,0,200, CG_GRASS_1, CG_GRASS_2)
    m.add_hill(500,220, 1200,0,200, CG_GRASS_2, CG_GRASS_1)
    m.add_hill(600,160, 0,0,1400, CG_GRASS_1, CG_GRASS_2)
    m.add_hill(350,140, -800,0,-400, CG_GRASS_2, CG_GRASS_1)
    m.add_hill(300,120, 900,0,-300, CG_GRASS_1, CG_GRASS_2)
    tree_pos = [(-500,200),(500,200),(-500,-200),(500,-200),
                (-700,600),(700,600),(-300,800),(300,800),
                (-900,100),(900,100),(-600,-500),(600,-500)]
    for tx,tz in tree_pos:
        m.add_cube(24,80,24, tx,40,tz, CG_TREE_TRUNK)
        m.add_hill(56,40, tx,80,tz, CG_TREE_TOP, CG_TREE_TOP2, 6)
    m.add_cube(32,8,32, -600,4,700, DARK_GREY)
    m.add_cube(24,24,24, -600,16,700, METAL_GREY)
    m.add_cube(80,200,16, 420,100,-1060, (120,180,248))
    m.add_cube(100,8,60, 420,0,-1060, CG_MOAT)
    m.add_cube(8,36,8, -800,18,-600, DARK_GREY)
    m.add_cube(28,28,28, -800,48,-600, (32,32,32))
    stars = [Star(0, 540, -1100, 0)]
    coins = [Coin(x*120,10,z*120) for x,z in [(-1,1),(1,1),(0,2),(-2,0),(2,0)]]
    return m, stars, coins

def build_castle_interior_f1():
    m = Mesh()
    tile = 200
    for x in range(-5,5):
        for z in range(-5,5):
            c = (180,170,150) if (x+z)%2==0 else (160,150,130)
            m.add_cube(tile,10,tile, x*tile,-5, z*tile, c)
    for z in range(-4,4):
        m.add_cube(120,2,tile, 0,1, z*tile, CARPET_RED)
    for w_z in [-1000,1000]:
        m.add_cube(2000,400,40, 0,200,w_z, CG_CASTLE_WALL)
    for w_x in [-1000,1000]:
        m.add_cube(40,400,2000, w_x,200,0, CG_CASTLE_WALL)
    m.add_cube(2000,20,2000, 0,400,0, CG_CASTLE_WALL)
    for px,pz in [(-400,-400),(400,-400),(-400,400),(400,400)]:
        m.add_cube(56,400,56, px,200,pz, WHITE)
        m.add_cube(72,24,72, px,400,pz, CG_CASTLE_TRIM)
    for i in range(8):
        m.add_cube(300,20,60, 0,i*25,-600-i*60, CG_STONE)
    m.add_cube(100,200,20, -800,100,0, BUTTON_GOLD)
    m.add_cube(100,200,20, 800,100,0, BUTTON_GOLD)
    m.add_cube(200,200,20, 0,100,-980, BUTTON_GOLD)
    for px,py,pz,c in [(-978,140,-300,BOB_GRASS_1),(-978,140,-500,WF_STONE_1),
                        (-978,140,-700,JRB_WATER),(978,140,-300,CCM_SNOW_1),(978,140,-500,BBH_WALL)]:
        m.add_cube(80,80,8, px,py,pz, (160,120,40))
        m.add_cube(70,70,4, px,py,pz-3 if px<0 else pz+3, c)
    m.add_cube(150,5,150, 600,-2,600, DARK_GREY)
    m.add_cube(100,100,5, 0,320,-998, (248,180,200))
    for tx,tz in [(-200,200),(200,-300),(-400,0)]:
        m.add_cube(20,30,20, tx,15,tz, WHITE)
        m.add_cube(24,12,24, tx,38,tz, RED)
    return m, [], []

def build_castle_basement():
    m = Mesh()
    for x in range(-6,6):
        for z in range(-6,6):
            c = (72,64,56) if (x+z)%2==0 else (56,48,40)
            m.add_cube(200,10,200, x*200,-5,z*200, c)
    m.add_cube(2400,300,40, 0,150,-1200, HMC_ROCK_2)
    m.add_cube(2400,300,40, 0,150,1200, HMC_ROCK_2)
    m.add_cube(40,300,2400, -1200,150,0, HMC_ROCK_2)
    m.add_cube(40,300,2400, 1200,150,0, HMC_ROCK_2)
    m.add_cube(2400,20,2400, 0,300,0, HMC_ROCK_2)
    m.add_cube(40,200,600, -400,100,-300, HMC_ROCK_1)
    m.add_cube(40,200,600, 400,100,300, HMC_ROCK_1)
    m.add_cube(600,200,40, 0,100,-400, HMC_ROCK_1)
    m.add_cube(400,4,400, -600,-3,-600, LLL_LAVA_1)
    m.add_cube(400,2,400, -600,-1,-600, LLL_LAVA_2)
    for px,py,pz,c in [(-1178,100,-400,HMC_ROCK_1),(-1178,100,-600,LLL_LAVA_1),
                        (-1178,100,-800,SSL_SAND_1),(1178,100,-400,DDD_WATER)]:
        m.add_cube(80,80,8, px,py,pz, (160,120,40))
        m.add_cube(70,70,4, px,py,pz, c)
    m.add_cube(50,30,50, 800,15,800, PIPE_GREEN)
    m.add_cube(80,80,10, 600,60,-1178, (0,200,200))
    return m, [], []

def build_castle_upper():
    m = Mesh()
    for x in range(-4,4):
        for z in range(-4,4):
            c = (180,170,150) if (x+z)%2==0 else (160,150,130)
            m.add_cube(200,10,200, x*200,-5,z*200, c)
    m.add_cube(1600,350,40, 0,175,-800, CG_CASTLE_WALL)
    m.add_cube(1600,350,40, 0,175,800, CG_CASTLE_WALL)
    m.add_cube(40,350,1600, -800,175,0, CG_CASTLE_WALL)
    m.add_cube(40,350,1600, 800,175,0, CG_CASTLE_WALL)
    m.add_cube(1600,20,1600, 0,350,0, CG_CASTLE_WALL)
    for px,py,pz,c in [(-778,100,-300,SL_ICE),(-778,100,-500,WDW_WATER),
                        (778,100,-300,TTM_GRASS),(778,100,-500,THI_GRASS_1),
                        (0,60,-778,TTC_GEAR),(0,75,-790,(248,56,56))]:
        m.add_cube(80,80,8, px,py,pz, (160,120,40))
        m.add_cube(70,70,4, px,py,pz, c)
    for i in range(6):
        m.add_cube(200,20,60, 0,i*30,-500-i*60, CG_STONE)
    return m, [], []

def build_castle_top():
    m = Mesh()
    for x in range(-2,2):
        for z in range(-2,2):
            m.add_cube(200,10,200, x*200,-5,z*200, (180,170,150))
    m.add_cube(800,300,40, 0,150,-400, CG_CASTLE_WALL)
    m.add_cube(800,300,40, 0,150,400, CG_CASTLE_WALL)
    m.add_cube(40,300,800, -400,150,0, CG_CASTLE_WALL)
    m.add_cube(40,300,800, 400,150,0, CG_CASTLE_WALL)
    m.add_cube(100,300,100, 0,150,0, (255,255,200))
    m.add_cube(60,20,60, 0,10,0, RED)
    m.add_cube(40,40,40, 0,30,0, YELLOW)
    return m, [], []

# === 15 MAIN COURSES (SM64 PC Port Authentic) ===

def build_bob_omb_battlefield():
    m = Mesh()
    for x in range(-7,7):
        for z in range(-7,7):
            c = BOB_GRASS_1 if (x+z)%2==0 else BOB_GRASS_2
            h = math.sin(x*0.4)*8 + math.cos(z*0.5)*6
            m.add_cube(200,14,200, x*200,-7+h,z*200, c)
    path_pts = [(0,-400),(100,-200),(200,0),(100,200),(0,400),(-100,200)]
    for px,pz in path_pts:
        m.add_cube(100,4,200, px,2,pz, BOB_PATH)
    m.add_cube(480,160,480, 0,80,0, BOB_MTN_LOW)
    m.add_cube(360,120,360, 0,240,0, BOB_MTN_MID)
    m.add_cube(240,80,240, 0,360,0, BOB_MTN_MID)
    m.add_cube(140,60,140, 0,440,0, BOB_MTN_TOP)
    m.add_cube(100,12,100, 0,480,0, BOB_MTN_TOP)
    m.add_slope(200,200, 80,40, -240,80,0, BOB_DIRT)
    m.add_slope(160,200, 60,30, 0,240,-180, BOB_DIRT)
    m.add_cube(120,10,120, 0,492,0, DARK_GREY)
    m.add_cube(8,40,8, -440,20,-240, DARK_GREY)
    m.add_cube(32,32,32, -440,52,-240, (24,24,24))
    m.add_cube(4,4,60, -440,36,-210, DARK_GREY)
    m.add_cube(240,10,36, -200,48,-320, BOB_FENCE)
    m.add_cube(240,10,36, 200,48,320, BOB_FENCE)
    for bx,bz in [(-200,-320),(200,320)]:
        for side in [-16,16]:
            m.add_cube(4,20,36, bx+side,60,bz, BOB_FENCE)
    for cx,cz in [(560,-440),(-560,440)]:
        m.add_cube(28,12,28, cx,6,cz, DARK_GREY)
        m.add_cube(12,24,12, cx,18,cz, METAL_GREY)
    m.add_cube(400,6,240, 440,-3,320, BOB_WATER)
    m.add_cube(280,6,160, 440,-3,200, BOB_WATER)
    m.add_cube(8,56,80, -320,28,-120, BOB_FENCE)
    m.add_cube(8,56,80, 320,28,120, BOB_FENCE)
    for tx,tz in [(-640,240),(640,-240),(-240,560),(320,-560),(-480,-480),(480,480)]:
        m.add_cube(20,64,20, tx,32,tz, CG_TREE_TRUNK)
        m.add_hill(48,32, tx,64,tz, CG_TREE_TOP, CG_TREE_TOP2, 6)
    m.add_hill(360,140, -1000,0,-600, BOB_GRASS_1, BOB_GRASS_2)
    m.add_hill(440,180, 1000,0,600, BOB_GRASS_2, BOB_GRASS_1)
    m.add_hill(300,100, -800,0,800, BOB_GRASS_1, BOB_GRASS_2)
    for bx,bz in [(200,-200),(-300,100),(400,200)]:
        m.add_cube(16,16,16, bx,10,bz, BLACK)
        m.add_cube(6,10,6, bx,22,bz, (180,180,180))
    stars = [Star(0,502,0,0), Star(560,20,-440,1), Star(-440,60,-240,2),
             Star(-640,40,240,3), Star(440,10,320,4)]
    coins = [Coin(px,10,pz) for px,pz in path_pts]
    coins += [Coin(x*80,10,z*80) for x,z in [(-3,3),(3,3),(-3,-3),(3,-3),(0,5)]]
    return m, stars, coins

def build_whomps_fortress():
    m = Mesh()
    m.add_cube(640,24,640, 0,-8,0, WF_STONE_1)
    m.add_cube(600,4,600, 0,4,0, WF_GRASS)
    for i in range(6):
        w = 540-i*72
        m.add_cube(w,36,w, 0,i*56+20,0, WF_STONE_2 if i%2==0 else WF_BRICK)
    m.add_slope(80,200, 56,0, -200,20,-100, WF_STONE_1)
    m.add_slope(80,200, 56,0, 200,76,100, WF_STONE_1)
    m.add_cube(56,96,20, 0,360,0, WF_STONE_2)
    m.add_cube(36,20,20, -28,380,0, WF_STONE_2)
    m.add_cube(36,20,20, 28,380,0, WF_STONE_2)
    m.add_cube(12,12,4, -16,400,-8, BLACK)
    m.add_cube(12,12,4, 16,400,-8, BLACK)
    m.add_cube(48,48,48, 200,80,100, DARK_GREY)
    m.add_cube(8,8,4, 186,100,78, RED)
    m.add_cube(8,8,4, 214,100,78, RED)
    m.add_cube(120,8,36, 100,120,200, WF_DIRT)
    for px,pz in [(160,-200),(-160,200)]:
        m.add_cube(28,36,28, px,18,pz, PIPE_GREEN)
        m.add_cube(20,12,20, px,42,pz, RED)
    m.add_cube(80,200,80, -260,100,-260, WF_STONE_1)
    m.add_cube(100,16,100, -260,200,-260, CG_CASTLE_ROOF)
    m.add_cube(24,16,24, 300,-4,300, DARK_GREY)
    m.add_cube(16,20,16, 300,12,300, (32,32,32))
    m.add_hill(500,200, -1200,0,800, WF_GRASS, (0,104,0))
    m.add_hill(400,160, 1200,0,-800, WF_GRASS, (0,104,0))
    stars = [Star(0,380,0,0), Star(-260,220,-260,1), Star(300,20,300,2)]
    coins = [Coin(i*56-140,40+i*10,i*36) for i in range(6)]
    return m, stars, coins

def build_jolly_roger_bay():
    m = Mesh()
    for x in range(-4,4):
        for z in range(-2,2):
            m.add_cube(200,10,200, x*200,-5,z*200-600, JRB_SAND)
    for x in range(-6,6):
        for z in range(-4,6):
            m.add_cube(200,6,200, x*200,-3,z*200, JRB_WATER)
    for x in range(-6,6):
        for z in range(-4,6):
            m.add_cube(200,10,200, x*200,-200,z*200, JRB_CAVE)
    m.add_cube(100,56,280, 200,-120,200, JRB_SHIP)
    m.add_cube(80,36,200, 200,-84,200, (96,64,32))
    m.add_cube(8,80,8, 200,-40,200, JRB_SHIP)
    m.add_cube(200,100,200, -400,-80,-300, JRB_CAVE)
    m.add_cube(180,80,180, -400,-60,-300, (64,56,48))
    for cx,cz in [(100,-100),(-200,0),(300,100)]:
        m.add_cube(28,8,28, cx,-192,cz, LIGHT_GREY)
        m.add_cube(24,16,12, cx,-182,cz, JRB_CORAL)
    m.add_cube(280,10,56, -200,5,-520, JRB_DOCK)
    m.add_cube(16,28,16, -340,18,-520, JRB_DOCK)
    m.add_cube(16,28,16, -60,18,-520, JRB_DOCK)
    m.add_cube(80,80,40, 500,-100,400, BLACK)
    m.add_hill(300,80, -600,0,-700, JRB_SAND, (200,176,128))
    m.add_hill(250,60, 600,0,-700, JRB_SAND, (200,176,128))
    stars = [Star(200,-60,200,0), Star(-400,-40,-300,1), Star(-200,20,-520,2)]
    coins = [Coin(x*80,-180,z*80) for x,z in [(-1,0),(0,1),(1,0),(0,-1),(1,1)]]
    return m, stars, coins

def build_cool_cool_mountain():
    m = Mesh()
    for x in range(-5,5):
        for z in range(-5,5):
            c = CCM_SNOW_1 if (x+z)%2==0 else CCM_SNOW_2
            m.add_cube(200,10,200, x*200,-5,z*200, c)
    for i in range(10):
        w = 220+i*56; c = CCM_SNOW_1 if i%2==0 else CCM_SNOW_2
        m.add_cube(w,20,w, 0,600-i*56,0, c)
    m.add_cube(100,40,100, -80,640,0, CCM_ROCK)
    m.add_cube(36,56,36, 0,660,0, (96,64,24))
    for i in range(18):
        a = i*0.38; r = 180+i*28
        sx = math.cos(a)*r; sz = math.sin(a)*r
        m.add_cube(72,8,72, sx,560-i*30,sz, CCM_SLIDE)
    m.add_cube(120,72,120, -300,36,-400, CCM_CABIN)
    m.add_cube(132,8,132, -300,72,-400, CG_CASTLE_ROOF)
    m.add_cube(40,56,4, -300,28,-338, (72,48,16))
    m.add_cube(24,24,4, -260,48,-338, (120,180,248))
    m.add_cube(56,56,56, 200,28,300, CCM_SNOW_1)
    m.add_cube(40,40,40, 200,72,300, CCM_SNOW_1)
    m.add_cube(16,8,16, 200,88,272, ORANGE)
    m.add_cube(8,8,4, 188,96,270, BLACK)
    m.add_cube(8,8,4, 212,96,270, BLACK)
    m.add_cube(200,8,36, -200,150,0, CCM_ICE)
    m.add_cube(16,28,16, -48,628,48, BLACK)
    m.add_cube(16,8,16, -48,640,48, WHITE)
    m.add_hill(600,300, -1200,0,800, CCM_SNOW_2, CCM_ROCK)
    m.add_hill(500,240, 1200,0,-600, CCM_SNOW_1, CCM_ROCK)
    stars = [Star(0,680,0,0), Star(-300,88,-400,1), Star(200,100,300,2)]
    coins = [Coin(math.cos(i*0.38)*(180+i*28),570-i*30,math.sin(i*0.38)*(180+i*28)) for i in range(0,18,3)]
    return m, stars, coins

def build_big_boos_haunt():
    m = Mesh()
    for x in range(-4,4):
        for z in range(-4,4):
            c = BBH_FLOOR if (x+z)%2==0 else (48,40,48)
            m.add_cube(200,10,200, x*200,-5,z*200, c)
    m.add_cube(400,280,400, 0,140,0, BBH_WALL)
    m.add_pyramid(450,140, 0,280,0, BBH_ROOF)
    for wx,wy in [(-120,200),(120,200),(-120,100),(120,100)]:
        m.add_cube(48,36,4, wx,wy,-200, BBH_WINDOW)
    m.add_cube(56,112,4, 0,56,-200, (80,56,32))
    m.add_cube(350,10,350, 0,-2,0, BBH_FLOOR)
    for gx,gz in [(-500,-200),(-500,-400),(-600,-300),(500,200),(500,400)]:
        m.add_cube(28,40,8, gx,20,gz, BBH_GRAVE)
        m.add_cube(36,4,12, gx,-2,gz, (72,64,48))
    m.add_cube(36,36,36, 100,100,300, BBH_GHOST)
    m.add_cube(8,6,4, 86,106,282, BLACK)
    m.add_cube(8,6,4, 114,106,282, BLACK)
    m.add_cube(80,2,80, -100,240,0, (180,180,180))
    m.add_cube(200,10,56, 0,200,-230, BBH_FLOOR)
    m.add_cube(200,5,200, 0,-100,300, BBH_FLOOR)
    m.add_cube(100,28,100, 0,-86,300, (80,56,32))
    for tx,tz in [(-600,0),(600,0),(0,600)]:
        m.add_cube(16,80,16, tx,40,tz, (64,48,32))
        m.add_cube(8,24,48, tx,80,tz, (80,64,48))
    stars = [Star(0,300,0,0), Star(100,120,300,1), Star(0,-72,300,2)]
    coins = [Coin(gx,30,gz) for gx,gz in [(-500,-200),(500,200),(-200,0),(200,0)]]
    return m, stars, coins

def build_hazy_maze_cave():
    m = Mesh()
    for x in range(-6,6):
        for z in range(-6,6):
            c = HMC_ROCK_1 if (x+z)%2==0 else HMC_ROCK_2
            m.add_cube(200,10,200, x*200,-5,z*200, c)
    m.add_cube(2400,20,2400, 0,280,0, HMC_ROCK_2)
    walls = [(-400,0,800,40),(-400,0,40,800),(400,0,800,40),(400,0,40,800),
             (0,-400,40,400),(0,400,40,400),(200,200,400,40),(-200,-200,400,40)]
    for wx,wz,ww,wd in walls:
        m.add_cube(ww,200,wd, wx,100,wz, HMC_ROCK_1)
    m.add_cube(600,4,600, -400,-3,-400, HMC_TOXIC)
    m.add_cube(200,10,200, 500,-2,500, HMC_METAL)
    m.add_cube(40,40,40, 500,20,500, BUTTON_GOLD)
    m.add_cube(500,6,500, 0,-3,0, HMC_WATER)
    m.add_cube(80,36,120, 0,18,0, (0,152,0))
    m.add_cube(28,28,36, 0,48,48, (0,136,0))
    for sx,sz in [(100,200),(-200,100),(300,-100),(-100,-300)]:
        m.add_cube(20,56,20, sx,252,sz, HMC_ROCK_2)
    stars = [Star(500,40,500,0), Star(0,56,0,1), Star(-400,10,-400,2)]
    coins = [Coin(x*150,10,z*150) for x,z in [(0,0),(1,1),(-1,-1),(2,0)]]
    return m, stars, coins

def build_lethal_lava_land():
    m = Mesh()
    for x in range(-6,6):
        for z in range(-6,6):
            c = LLL_LAVA_1 if (x+z)%2==0 else LLL_LAVA_2
            m.add_cube(200,6,200, x*200,-3,z*200, c)
    platforms = [(0,0,200),(300,0,140),(-300,0,140),(0,0,400),(500,0,96),
                 (-500,0,96),(200,0,280),(-200,0,280),(0,0,-200),(0,0,-480)]
    for px,py,ps in platforms:
        m.add_cube(ps,20,ps, px,10+py,py, LLL_STONE)
    m.add_cube(300,200,300, 0,100,0, LLL_VOLCANO)
    m.add_cube(200,100,200, 0,250,0, DARK_GREY)
    m.add_cube(100,8,100, 0,300,0, LLL_LAVA_2)
    m.add_cube(80,8,80, 0,148,0, LLL_STONE)
    m.add_cube(56,8,56, 48,196,0, LLL_STONE)
    m.add_cube(16,16,200, -200,18,-100, (96,64,24))
    m.add_cube(100,8,100, 400,18,400, LLL_METAL)
    m.add_cube(100,8,100, -400,18,-400, LLL_METAL)
    for fx,fz in [(150,150),(-150,-150),(300,-200)]:
        m.add_cube(16,36,16, fx,28,fz, ORANGE)
        m.add_cube(24,8,24, fx,48,fz, (248,200,0))
    stars = [Star(0,310,0,0), Star(-400,36,-400,1), Star(500,28,0,2)]
    coins = [Coin(px,28,py) for px,py,ps in platforms[:5]]
    return m, stars, coins

def build_shifting_sand_land():
    m = Mesh()
    for x in range(-7,7):
        for z in range(-7,7):
            c = SSL_SAND_1 if (x+z)%2==0 else SSL_SAND_2
            h = math.sin(x*0.6)*6 + math.cos(z*0.4)*4
            m.add_cube(200,12,200, x*200,-6+h,z*200, c)
    m.add_cube(400,280,400, 0,140,0, SSL_PYRAMID)
    m.add_pyramid(420,100, 0,280,0, SSL_BRICK)
    m.add_cube(300,200,300, 0,100,0, (120,88,48))
    m.add_cube(80,8,80, 0,200,0, (88,72,40))
    m.add_cube(300,4,300, -500,-3,-500, SSL_QUICKSAND)
    m.add_cube(200,4,200, 500,-1,500, SSL_OASIS)
    m.add_cube(20,56,20, 520,28,520, CG_TREE_TRUNK)
    m.add_cube(56,8,56, 520,56,520, SSL_PALM)
    m.add_cube(48,6,48, 520,50,520, (0,120,0))
    for px,pz in [(-300,300),(300,-300),(-300,-300),(300,300)]:
        m.add_cube(36,120,36, px,60,pz, SSL_SAND_1)
        m.add_cube(48,12,48, px,120,pz, SSL_BRICK)
    m.add_cube(56,56,56, 200,28,-200, DARK_GREY)
    m.add_cube(56,56,56, -200,28,200, DARK_GREY)
    m.add_cube(20,72,20, -500,36,200, CG_TREE_TRUNK)
    m.add_cube(28,8,48, -500,76,200, (96,72,24))
    m.add_hill(500,100, -1200,0,0, SSL_SAND_2, SSL_SAND_1)
    m.add_hill(600,120, 1200,0,0, SSL_SAND_1, SSL_SAND_2)
    m.add_hill(400,80, 0,0,1400, SSL_SAND_2, SSL_SAND_1)
    stars = [Star(0,390,0,0), Star(500,16,500,1), Star(-500,8,-500,2)]
    coins = [Coin(x*200,10,z*200) for x,z in [(1,1),(-1,-1),(2,-2),(-2,2),(0,3)]]
    return m, stars, coins

def build_dire_dire_docks():
    m = Mesh()
    for x in range(-3,3):
        m.add_cube(200,10,200, x*200,-5,-600, DDD_DOCK)
    for x in range(-6,6):
        for z in range(-4,6):
            m.add_cube(200,6,200, x*200,-3,z*200, DDD_WATER)
    for x in range(-6,6):
        for z in range(-4,6):
            m.add_cube(200,10,200, x*200,-200,z*200, DDD_FLOOR)
    m.add_cube(120,56,380, 0,-60,200, DDD_SUB)
    m.add_cube(80,36,96, 0,-28,380, DDD_METAL)
    m.add_cube(8,56,8, 0,0,380, DDD_METAL)
    m.add_cube(200,200,16, 0,100,800, DDD_METAL)
    m.add_cube(8,200,8, -88,100,800, DARK_GREY)
    m.add_cube(8,200,8, 88,100,800, DARK_GREY)
    m.add_cube(96,4,96, -400,-1,400, (32,48,144))
    for px,pz in [(300,0),(-300,0),(0,600)]:
        m.add_cube(8,140,8, px,-120,pz, DDD_METAL)
    m.add_cube(80,6,120, 200,-80,300, (48,48,96))
    stars = [Star(0,-20,200,0), Star(0,10,800,1), Star(-400,10,400,2)]
    coins = [Coin(x*96,-80,z*96) for x,z in [(0,0),(1,2),(-1,3),(2,1)]]
    return m, stars, coins

def build_snowmans_land():
    m = Mesh()
    for x in range(-6,6):
        for z in range(-6,6):
            c = SL_SNOW_1 if (x+z)%2==0 else SL_SNOW_2
            m.add_cube(200,10,200, x*200,-5,z*200, c)
    m.add_cube(300,200,300, 0,100,0, SL_SNOW_1)
    m.add_cube(200,140,200, 0,270,0, SL_SNOW_2)
    m.add_cube(120,96,120, 0,388,0, SL_SNOW_1)
    m.add_cube(80,72,80, 0,472,0, SL_SNOW_1)
    m.add_cube(16,16,16, 0,484,-36, ORANGE)
    m.add_cube(8,8,4, -12,496,-34, BLACK)
    m.add_cube(8,8,4, 12,496,-34, BLACK)
    m.add_cube(200,6,36, -200,148,0, SL_ICE)
    m.add_cube(100,56,100, -400,28,-300, SL_IGLOO)
    m.add_cube(36,36,8, -400,18,-348, (80,56,24))
    m.add_cube(300,4,300, 400,-1,400, SL_ICE)
    m.add_cube(28,28,28, 200,18,400, BLACK)
    m.add_cube(6,16,6, 200,40,400, METAL_GREY)
    m.add_cube(140,8,140, 0,96,500, SL_ICE)
    for tx,tz in [(-500,200),(500,-200),(-200,500)]:
        m.add_cube(16,56,16, tx,28,tz, CG_TREE_TRUNK)
        m.add_hill(44,28, tx,56,tz, SL_ICE, SL_SNOW_2, 6)
    m.add_hill(500,200, -1200,0,600, SL_SNOW_2, CCM_ROCK)
    m.add_hill(600,260, 1200,0,-400, SL_SNOW_1, CCM_ROCK)
    stars = [Star(0,520,0,0), Star(-400,56,-300,1), Star(0,112,500,2)]
    coins = [Coin(x*120,10,z*120) for x,z in [(2,2),(-2,-2),(3,0),(0,3)]]
    return m, stars, coins

def build_wet_dry_world():
    m = Mesh()
    for x in range(-4,4):
        for z in range(-4,4):
            c = WDW_BRICK if (x+z)%2==0 else WDW_STONE
            m.add_cube(200,10,200, x*200,-5,z*200, c)
    m.add_cube(1600,4,1600, 0,48,0, WDW_WATER)
    m.add_cube(200,280,200, -300,140,0, WDW_BRICK)
    m.add_cube(200,200,200, 300,100,-200, WDW_BRICK)
    m.add_cube(150,240,150, 0,120,300, WDW_STONE)
    for sx,sz in [(-300,300),(300,-300),(0,0)]:
        m.add_cube(28,28,28, sx,18,sz, WDW_SWITCH)
    m.add_cube(56,56,56, -100,28,-200, METAL_GREY)
    m.add_cube(56,56,56, 200,28,200, METAL_GREY)
    m.add_cube(100,96,100, -500,48,-400, METAL_GREY)
    m.add_cube(600,8,400, 0,-100,-500, (56,48,40))
    m.add_cube(100,72,100, -200,-64,-500, WDW_BRICK)
    m.add_cube(100,72,100, 200,-64,-500, WDW_BRICK)
    stars = [Star(-300,290,0,0), Star(0,260,300,1), Star(-200,-50,-500,2)]
    coins = [Coin(x*96,56,z*96) for x,z in [(0,0),(1,1),(-1,-1),(2,-2)]]
    return m, stars, coins

def build_tall_tall_mountain():
    m = Mesh()
    for x in range(-5,5):
        for z in range(-5,5):
            c = TTM_GRASS if (x+z)%2==0 else (0,120,0)
            m.add_cube(200,10,200, x*200,-5,z*200, c)
    m.add_cube(500,280,500, 0,140,0, TTM_DIRT)
    m.add_cube(400,240,400, 0,400,0, TTM_ROCK)
    m.add_cube(300,200,300, 0,640,0, DARK_GREY)
    m.add_cube(200,140,200, 0,840,0, (96,88,80))
    m.add_cube(120,80,120, 0,980,0, (80,72,64))
    m.add_pyramid(140,56, 0,1020,0, DARK_STONE)
    for i in range(22):
        a = i*0.32; r = 280+48*math.sin(i*0.5)
        px = math.cos(a)*r; pz = math.sin(a)*r
        m.add_cube(72,8,72, px,i*44+16,pz, TTM_ROCK)
    m.add_cube(56,380,16, -260,190,-200, TTM_WATER)
    m.add_cube(80,8,48, -260,4,-200, TTM_WATER)
    for mx,mz,mh in [(400,200,56),(400,300,96),(-400,-200,72)]:
        m.add_cube(16,mh,16, mx,mh/2,mz, TTM_MUSH_STEM)
        m.add_cube(52,12,52, mx,mh,mz, TTM_MUSH_TOP)
    m.add_cube(96,8,96, 200,380,-200, TTM_GRASS)
    m.add_cube(36,36,36, 0,1052,0, (96,64,24))
    m.add_hill(500,200, -1200,0,800, TTM_GRASS, (0,104,0))
    m.add_hill(600,280, 1200,0,-600, TTM_GRASS, (0,88,0))
    stars = [Star(0,1060,0,0), Star(200,400,-200,1), Star(-400,88,-200,2)]
    coins = [Coin(math.cos(i*0.32)*280,i*44+24,math.sin(i*0.32)*280) for i in range(0,22,4)]
    return m, stars, coins

def build_tiny_huge_island():
    m = Mesh()
    for x in range(-5,5):
        for z in range(-5,5):
            dist = math.sqrt(x*x+z*z)
            if dist < 5:
                c = THI_GRASS_1 if (x+z)%2==0 else THI_GRASS_2
                h = max(0,36-dist*7)
                m.add_cube(200,10+h,200, x*200,h/2,z*200, c)
    for x in range(-6,6):
        for z in range(-6,6):
            if math.sqrt(x*x+z*z)>=4:
                m.add_cube(200,6,200, x*200,-3,z*200, THI_WATER)
    m.add_cube(300,200,300, 0,100,0, TTM_DIRT)
    m.add_cube(200,100,200, 0,250,0, TTM_ROCK)
    m.add_cube(36,28,36, -300,48,-300, THI_PIPE)
    m.add_cube(72,56,72, 300,56,300, THI_PIPE)
    m.add_cube(56,112,56, -200,56,200, (144,136,120))
    m.add_cube(8,72,8, -200,128,168, (96,64,24))
    m.add_cube(72,8,8, -200,168,166, (96,64,24))
    m.add_cube(280,6,96, 0,-2,-500, THI_BEACH)
    for px,pz in [(100,100),(-100,-100),(200,-200)]:
        m.add_cube(20,28,20, px,46,pz, THI_PIPE)
        m.add_cube(16,10,16, px,62,pz, RED)
    m.add_cube(56,56,16, 0,240,-96, BLACK)
    m.add_hill(500,160, -1200,0,400, THI_GRASS_1, THI_GRASS_2)
    m.add_hill(400,120, 1000,0,-600, THI_GRASS_2, THI_GRASS_1)
    stars = [Star(0,300,0,0), Star(-200,128,200,1), Star(0,10,-500,2)]
    coins = [Coin(x*96,48,z*96) for x,z in [(0,1),(1,0),(-1,0),(0,-1),(1,1)]]
    return m, stars, coins

def build_tick_tock_clock():
    m = Mesh()
    m.add_cube(300,20,300, 0,-5,0, TTC_WOOD)
    m.add_cube(40,1200,600, -300,600,0, TTC_WOOD)
    m.add_cube(40,1200,600, 300,600,0, TTC_WOOD)
    m.add_cube(600,1200,40, 0,600,-300, TTC_WOOD)
    m.add_cube(600,1200,40, 0,600,300, TTC_WOOD)
    heights = [72,168,280,400,520,640,760,880,1000,1120]
    for i,h in enumerate(heights):
        a = i*0.7; px=math.cos(a)*96; pz=math.sin(a)*96
        w = 96 if i%2==0 else 72
        m.add_cube(w,8,w, px,h,pz, TTC_METAL)
    m.add_cube(8,200,8, -96,500,0, TTC_HAND)
    m.add_cube(8,280,8, 96,600,0, TTC_HAND)
    for gh in [200,480,760]:
        m.add_cube(72,8,72, -200,gh,96, TTC_GEAR)
        m.add_cube(56,8,56, 200,gh,-96, TTC_GEAR)
    m.add_cube(48,48,48, 0,380,0, DARK_GREY)
    m.add_cube(200,6,36, 0,680,0, TTC_GEAR)
    m.add_cube(200,6,36, 0,840,0, TTC_GEAR)
    m.add_cube(200,16,200, 0,1180,0, BUTTON_GOLD)
    stars = [Star(0,1200,0,0), Star(-200,500,96,1), Star(0,690,0,2)]
    coins = [Coin(math.cos(i*0.7)*96,heights[i]+12,math.sin(i*0.7)*96) for i in range(0,10,2)]
    return m, stars, coins

def build_rainbow_ride():
    m = Mesh()
    m.add_cube(200,16,200, 0,-5,0, RR_CLOUD)
    for i in range(32):
        c = RR_RAINBOW[i%6]
        a = i*0.14; px=i*76; pz=math.sin(a)*200; py=i*18
        m.add_cube(56,6,56, px,py,pz, c)
    m.add_cube(72,4,72, -200,96,-200, RR_CARPET)
    for i in range(12):
        m.add_cube(56,6,56, -200-i*96,96+i*28,-200-i*76, RR_CARPET)
    m.add_cube(200,112,200, 800,192,0, RR_HOUSE)
    m.add_cube(220,8,220, 800,248,0, CG_CASTLE_ROOF)
    m.add_cube(36,72,8, 800,192,-96, (104,72,32))
    for i in range(5):
        for j in range(3):
            m.add_cube(72,6,72, 400+i*96,280+j*56,-280+j*96, RR_CLOUD)
    for sx in range(-96,400,140):
        m.add_cube(56,6,56, sx,72,-400, METAL_GREY)
    m.add_cube(48,6,48, 500,96,280, ORANGE)
    m.add_cube(48,6,48, 600,120,340, ORANGE)
    m.add_cube(8,200,8, 1000,280,0, METAL_GREY)
    for i in range(4):
        m.add_cube(96,6,96, -400+i*56,192+i*36,280+i*56, RR_RAINBOW[0])
    for cx,cz in [(1200,200),(1200,-200),(1400,0)]:
        m.add_cube(96,16,96, cx,384,cz, RR_CLOUD)
    m.add_cube(120,16,120, 1400,400,0, BUTTON_GOLD)
    stars = [Star(1400,420,0,0), Star(800,264,0,1), Star(-200-11*96,96+11*28,-200-11*76,2)]
    coins = [Coin(i*76,i*18+8,math.sin(i*0.14)*200) for i in range(0,32,5)]
    return m, stars, coins


# === SECRET LEVELS ===

def build_princess_secret_slide():
    m = Mesh()
    m.add_cube(200,16,200, 0,580,0, CG_CASTLE_WALL)
    for i in range(25):
        a=i*0.3; r=96+i*14; px=math.cos(a)*r; pz=math.sin(a)*r
        m.add_cube(56,6,56, px,560-i*20,pz, CCM_SLIDE)
    ep = (math.cos(24*0.3)*(96+24*14), math.sin(24*0.3)*(96+24*14))
    m.add_cube(200,16,200, ep[0],40,ep[1], CG_CASTLE_WALL)
    stars = [Star(ep[0],60,ep[1],0)]
    return m, stars, []

def build_wing_mario_rainbow():
    m = Mesh()
    m.add_cube(140,16,140, 0,-5,0, RR_CLOUD)
    for i in range(20):
        c=RR_RAINBOW[i%6]; a=i*0.3; r=200+i*36
        m.add_cube(72,6,72, math.cos(a)*r,i*28+8,math.sin(a)*r, c)
    for cx,cz in [(600,300),(-400,500),(200,-400)]:
        m.add_cube(112,16,112, cx,192,cz, RR_CLOUD)
    m.add_cube(36,36,36, 0,8,0, RED)
    stars = [Star(600,212,300,0)]
    coins = [Coin(math.cos(i*0.3)*(200+i*36),i*28+16,math.sin(i*0.3)*(200+i*36)) for i in range(0,20,4)]
    return m, stars, coins

def build_metal_cap_cavern():
    m = Mesh()
    for x in range(-4,4):
        for z in range(-4,4):
            c = HMC_ROCK_1 if (x+z)%2==0 else HMC_ROCK_2
            m.add_cube(200,10,200, x*200,-5,z*200, c)
    m.add_cube(1600,20,1600, 0,240,0, HMC_ROCK_2)
    m.add_cube(800,4,800, 0,-1,0, HMC_WATER)
    m.add_cube(56,16,56, 0,8,0, PIPE_GREEN)
    m.add_cube(36,36,36, 0,24,0, METAL_GREY)
    m.add_cube(96,192,16, 300,96,-400, (48,96,192))
    for i in range(5):
        m.add_cube(72,8,72, -200+i*96,4,200-i*72, HMC_ROCK_1)
    stars = [Star(0,44,0,0)]
    return m, stars, []

def build_vanish_cap():
    m = Mesh()
    m.add_cube(200,16,200, 0,192,0, HMC_ROCK_1)
    for i in range(15):
        m.add_cube(96,8,96, i*76,176-i*11,0, SL_ICE if i%2==0 else (0,184,184))
    m.add_cube(56,16,56, 1140,8,0, (0,184,184))
    m.add_cube(36,36,36, 1140,24,0, BLUE)
    for i in range(8):
        m.add_cube(56,8,56, 600+i*72,56+i*8,i*36-140, HMC_ROCK_1)
    stars = [Star(1140,44,0,0)]
    return m, stars, []

def build_tower_wing_cap():
    m = Mesh()
    m.add_cube(280,16,280, 0,-5,0, RR_CLOUD)
    m.add_cube(56,380,56, 0,192,0, (144,136,120))
    m.add_cube(96,16,96, 0,380,0, RR_CLOUD)
    m.add_cube(36,36,36, 0,400,0, RED)
    for i in range(8):
        a=i*math.pi/4
        m.add_cube(96,8,96, math.cos(a)*380,192,math.sin(a)*380, RR_CLOUD)
    stars = [Star(0,420,0,0)]
    coins = [Coin(math.cos(i*math.pi/4)*380,204,math.sin(i*math.pi/4)*380) for i in range(8)]
    return m, stars, coins


# === BOWSER LEVELS ===

def build_bowser_dark_world():
    m = Mesh()
    m.add_cube(200,16,200, 0,-5,0, BDW_STONE)
    path = [(200,0),(400,40),(600,80),(600,160),(400,240),(200,240),
            (0,320),(200,400),(400,400),(600,480),(800,480),(1000,400)]
    for px,pz in path:
        m.add_cube(112,16,112, px,8,pz, (96,72,96))
    for fx,fz in [(400,40),(600,160),(200,240)]:
        m.add_cube(8,8,72, fx,28,fz, ORANGE)
    m.add_cube(400,16,400, 1000,8,400, BDW_STONE)
    m.add_cube(56,72,56, 1000,52,400, DARK_GREEN)
    m.add_cube(36,36,36, 1000,108,400, (0,176,0))
    m.add_cube(16,16,8, 1000,124,372, RED)
    for i in range(8):
        a=i*math.pi/4; bx=1000+math.cos(a)*172; bz=400+math.sin(a)*172
        m.add_cube(16,16,16, bx,24,bz, BLACK)
    stars = [Star(1000,112,400,0)]
    return m, stars, []

def build_bowser_fire_sea():
    m = Mesh()
    for x in range(-6,6):
        for z in range(-6,6):
            c = LLL_LAVA_1 if (x+z)%2==0 else LLL_LAVA_2
            m.add_cube(200,6,200, x*200,-3,z*200, c)
    m.add_cube(200,16,200, 0,8,0, BFS_METAL)
    pp = [(0,0),(140,200),(280,400),(140,600),(0,800),
          (-200,1000),(-400,1000),(-400,800),(-200,600),(0,400)]
    for i,(px,pz) in enumerate(pp):
        m.add_cube(96,16,96, px,8+i*4,pz, BFS_METAL)
    m.add_cube(200,6,36, 200,16,200, (96,64,24))
    m.add_cube(200,6,36, -200,16,800, (96,64,24))
    m.add_cube(8,192,8, -400,96,1000, BFS_METAL)
    m.add_cube(480,16,480, 0,52,1200, BDW_STONE)
    m.add_cube(72,96,72, 0,100,1200, DARK_GREEN)
    m.add_cube(48,48,48, 0,168,1200, (0,152,0))
    m.add_cube(24,16,8, 0,184,1160, RED)
    m.add_cube(84,24,84, 0,68,1200, (88,56,24))
    stars = [Star(0,168,1200,0)]
    return m, stars, []

def build_bowser_sky():
    m = Mesh()
    m.add_cube(200,16,200, 0,-5,0, BITS_STONE)
    sp = []
    for i in range(25):
        a=i*0.24; r=200+i*18; px=math.cos(a)*r; pz=math.sin(a)*r; py=i*36
        sp.append((px,py,pz))
        c = [BITS_STONE,(80,56,80),DARK_GREY,BFS_METAL][i%4]
        m.add_cube(96,12,96, px,py,pz, c)
    for i in range(0,25,3):
        px,py,pz = sp[i]
        m.add_cube(8,8,56, px+36,py+16,pz, ORANGE)
    last = sp[-1]
    ax,ay,az = last[0],last[1]+36,last[2]
    m.add_cube(560,16,560, ax,ay,az, BITS_STONE)
    for i in range(12):
        a=i*math.pi/6; bx=ax+math.cos(a)*260; bz=az+math.sin(a)*260
        m.add_cube(16,16,16, bx,ay+16,bz, BLACK)
    m.add_cube(96,112,96, ax,ay+72,az, DARK_GREEN)
    m.add_cube(56,56,56, ax,ay+168,az, (0,168,0))
    m.add_cube(36,24,8, ax,ay+188,az-44, RED)
    for sx,sz in [(-28,0),(28,0),(0,-28),(0,28)]:
        m.add_cube(12,20,12, ax+sx,ay+120,az+sz, (88,56,24))
    stars = [Star(ax,ay+208,az,0)]
    return m, stars, []


# =====================================================================
# LEVEL REGISTRY
# =====================================================================
LEVELS = {
    "castle_grounds": {"name":"Castle Grounds","builder":build_castle_grounds,"req":0},
    "castle_f1": {"name":"Castle Interior","builder":build_castle_interior_f1,"req":0},
    "castle_basement": {"name":"Castle Basement","builder":build_castle_basement,"req":8},
    "castle_upper": {"name":"Castle Upper Floor","builder":build_castle_upper,"req":30},
    "castle_top": {"name":"Castle Top","builder":build_castle_top,"req":50},
    "c01_bob": {"name":"Bob-omb Battlefield","builder":build_bob_omb_battlefield,"req":0},
    "c02_whomp": {"name":"Whomp's Fortress","builder":build_whomps_fortress,"req":1},
    "c03_jolly": {"name":"Jolly Roger Bay","builder":build_jolly_roger_bay,"req":3},
    "c04_cool": {"name":"Cool, Cool Mountain","builder":build_cool_cool_mountain,"req":3},
    "c05_boo": {"name":"Big Boo's Haunt","builder":build_big_boos_haunt,"req":12},
    "c06_hazy": {"name":"Hazy Maze Cave","builder":build_hazy_maze_cave,"req":8},
    "c07_lava": {"name":"Lethal Lava Land","builder":build_lethal_lava_land,"req":8},
    "c08_sand": {"name":"Shifting Sand Land","builder":build_shifting_sand_land,"req":8},
    "c09_dock": {"name":"Dire, Dire Docks","builder":build_dire_dire_docks,"req":30},
    "c10_snow": {"name":"Snowman's Land","builder":build_snowmans_land,"req":30},
    "c11_wet": {"name":"Wet-Dry World","builder":build_wet_dry_world,"req":30},
    "c12_tall": {"name":"Tall, Tall Mountain","builder":build_tall_tall_mountain,"req":30},
    "c13_tiny": {"name":"Tiny-Huge Island","builder":build_tiny_huge_island,"req":30},
    "c14_clock": {"name":"Tick Tock Clock","builder":build_tick_tock_clock,"req":50},
    "c15_rainbow": {"name":"Rainbow Ride","builder":build_rainbow_ride,"req":50},
    "s_slide": {"name":"Princess's Secret Slide","builder":build_princess_secret_slide,"req":1},
    "s_wing": {"name":"Wing Mario Over Rainbow","builder":build_wing_mario_rainbow,"req":10},
    "s_metal": {"name":"Metal Cap Cavern","builder":build_metal_cap_cavern,"req":8},
    "s_vanish": {"name":"Vanish Cap Moat","builder":build_vanish_cap,"req":8},
    "s_tower": {"name":"Tower of Wing Cap","builder":build_tower_wing_cap,"req":10},
    "b1_dark": {"name":"Bowser Dark World","builder":build_bowser_dark_world,"req":8},
    "b2_fire": {"name":"Bowser Fire Sea","builder":build_bowser_fire_sea,"req":30},
    "b3_sky": {"name":"Bowser in the Sky","builder":build_bowser_sky,"req":70},
}

CASTLE_F1_PAINTINGS = [
    {"pos":(-978,140,-300),"level":"c01_bob"},{"pos":(-978,140,-500),"level":"c02_whomp"},
    {"pos":(-978,140,-700),"level":"c03_jolly"},{"pos":(978,140,-300),"level":"c04_cool"},
    {"pos":(978,140,-500),"level":"c05_boo"},
]
BASEMENT_PAINTINGS = [
    {"pos":(-1178,100,-400),"level":"c06_hazy"},{"pos":(-1178,100,-600),"level":"c07_lava"},
    {"pos":(-1178,100,-800),"level":"c08_sand"},{"pos":(1178,100,-400),"level":"c09_dock"},
]
UPPER_PAINTINGS = [
    {"pos":(-778,100,-300),"level":"c10_snow"},{"pos":(-778,100,-500),"level":"c11_wet"},
    {"pos":(778,100,-300),"level":"c12_tall"},{"pos":(778,100,-500),"level":"c13_tiny"},
    {"pos":(0,60,-778),"level":"c14_clock"},{"pos":(0,75,-790),"level":"c15_rainbow"},
]


# =====================================================================
# RENDERER (SM64 PC port third-person Lakitu camera + distance fog)
# =====================================================================
def render_mesh(screen, mesh, cam_x, cam_y, cam_z, cam_yaw, cam_pitch, cx, cy, is_menu=False):
    render_list = []
    c_cos = math.cos(-cam_yaw); c_sin = math.sin(-cam_yaw)
    p_cos = math.cos(-cam_pitch); p_sin = math.sin(-cam_pitch)
    m_cos = math.cos(mesh.yaw); m_sin = math.sin(mesh.yaw)
    menu_tilt = 0.2
    wiggle = math.sin(pygame.time.get_ticks()/500.0)*10 if is_menu else 0

    for face in mesh.faces:
        transformed = []; avg_z = 0; valid = True
        for i in face.indices:
            v = mesh.vertices[i]
            rx = v.x*m_cos - v.z*m_sin
            rz = v.x*m_sin + v.z*m_cos
            ry = v.y
            if is_menu:
                ry_t = ry*math.cos(menu_tilt)-rz*math.sin(menu_tilt)
                rz = ry*math.sin(menu_tilt)+rz*math.cos(menu_tilt)
                ry = ry_t + wiggle
            wx=rx+mesh.x; wy=ry+mesh.y; wz=rz+mesh.z
            dcx=wx-cam_x; dcy=wy-cam_y; dcz=wz-cam_z
            if not is_menu:
                xx=dcx*c_cos-dcz*c_sin; zz=dcx*c_sin+dcz*c_cos; yy=dcy
                yy2=yy*p_cos-zz*p_sin; zz2=yy*p_sin+zz*p_cos
                xx,yy,zz = xx,yy2,zz2
            else:
                xx=dcx; yy=dcy; zz=dcz
            if zz < 5:
                valid = False; break
            transformed.append((xx,yy,zz)); avg_z += zz
        if not valid: continue
        screen_points = []
        for xx,yy,zz in transformed:
            s = FOV/zz
            screen_points.append((int(xx*s+cx), int(-yy*s+cy)))
        if len(screen_points)>=3:
            area = 0
            for i in range(len(screen_points)):
                j=(i+1)%len(screen_points)
                area+=(screen_points[j][0]-screen_points[i][0])*(screen_points[j][1]+screen_points[i][1])
            if area > 0:
                render_list.append({'poly':screen_points,'depth':avg_z/len(transformed),'color':face.color})
    return render_list


# =====================================================================
# SM64 PC PORT TITLE SCREEN MARIO HEAD
# =====================================================================
def create_menu_head():
    m = Mesh()
    # SM64 PC port accurate Mario head
    m.add_cube(40,36,40,0,0,0,MARIO_SKIN)              # head
    m.add_cube(44,12,44,0,20,0,MARIO_CAP)               # cap
    m.add_cube(52,4,52,0,15,10,MARIO_CAP)                # brim
    m.add_cube(8,8,2,0,22,22, MARIO_M_EMBLEM)            # M logo
    m.add_cube(10,10,10,0,-2,22,MARIO_SKIN)              # nose
    m.add_cube(24,6,4,0,-10,21,MUSTACHE_BLACK)           # mustache
    m.add_cube(10,12,2,-12,6,20,WHITE)                    # L eye white
    m.add_cube(10,12,2,12,6,20,WHITE)                     # R eye white
    m.add_cube(4,6,3,-12,6,21,EYE_BLUE)                   # L pupil
    m.add_cube(4,6,3,12,6,21,EYE_BLUE)                    # R pupil
    m.add_cube(42,24,10,0,0,-18,MARIO_HAIR)              # hair back
    m.add_cube(6,16,30, -22,0,0, MARIO_HAIR)              # L sideburn
    m.add_cube(6,16,30, 22,0,0, MARIO_HAIR)               # R sideburn
    # Ears
    m.add_cube(4,10,8, -22,4,8, MARIO_SKIN)
    m.add_cube(4,10,8, 22,4,8, MARIO_SKIN)
    return m


# =====================================================================
# SAVE FILE SYSTEM (SM64 has 4 save slots)
# =====================================================================
class SaveFile:
    def __init__(self, slot):
        self.slot = slot
        self.stars = set()
        self.coins = 0
        self.lives = 4
        self.exists = False

    def star_count(self):
        return len(self.stars)


# =====================================================================
# MAIN LOOP — AC'S SM64 PC PORT PY EDITION 0.1
# =====================================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AC'S SM64 PC PORT — PY EDITION 0.1  |  (C) 2026 A.C Holdings")
    clock = pygame.time.Clock()

    audio = SM64Audio()

    try:
        font_title = pygame.font.Font(None, 80)
        font_subtitle = pygame.font.Font(None, 36)
        font_menu = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 22)
        font_hud = pygame.font.SysFont('Arial', 22, bold=True)
        font_hud_big = pygame.font.SysFont('Arial', 28, bold=True)
        font_big = pygame.font.Font(None, 52)
        font_star_get = pygame.font.Font(None, 64)
        font_action = pygame.font.Font(None, 20)
    except:
        font_title = pygame.font.SysFont('Arial',60,bold=True)
        font_subtitle = pygame.font.SysFont('Arial',28,bold=True)
        font_menu = pygame.font.SysFont('Arial',24,bold=True)
        font_small = pygame.font.SysFont('Arial',16)
        font_hud = font_small
        font_hud_big = font_menu
        font_big = font_menu
        font_star_get = font_title
        font_action = font_small

    # === GAME STATES ===
    STATE_TITLE = 0
    STATE_FILE_SELECT = 1
    STATE_GAME = 2
    STATE_LEVEL_SELECT = 3
    STATE_PAUSE = 4
    STATE_STAR_GET = 5
    STATE_PAINTING_WARP = 6

    current_state = STATE_TITLE

    # Save files
    save_files = [SaveFile(i) for i in range(4)]
    current_save = 0

    # Menu state
    menu_head = create_menu_head()
    title_selected = 0
    file_selected = 0
    title_timer = 0

    level_keys = list(LEVELS.keys())
    level_select_idx = 0

    # Game state
    mario = None
    current_level_mesh = None
    current_level_stars = []
    current_level_coins = []
    current_level_id = None

    # SM64 Lakitu Camera
    cam_x = cam_y = cam_z = 0.0
    cam_yaw = 0.0
    cam_pitch = 0.15   # Slight downward look (SM64 default)
    cam_dist = CAM_DIST
    cam_mode = 0        # 0 = Lakitu, 1 = Mario (close)

    vel_x = vel_z = 0.0
    cx, cy = WIDTH // 2, HEIGHT // 2
    collected_stars = set()
    total_coins = 0
    star_flash = 0
    coin_flash = 0
    level_name_timer = 0
    level_display_name = ""
    star_get_timer = 0
    star_get_name = ""
    painting_warp_timer = 0
    painting_warp_target = ""
    level_coin_count = 0   # Per-level coin counter (SM64 resets per level)

    # Action display
    action_display = ""
    action_display_timer = 0

    def show_action(name):
        nonlocal action_display, action_display_timer
        action_display = name
        action_display_timer = 40

    def load_level(level_id):
        nonlocal mario, current_level_mesh, current_level_stars, current_level_coins
        nonlocal current_level_id, cam_x, cam_y, cam_z, cam_yaw, cam_pitch, cam_dist
        nonlocal vel_x, vel_z, level_name_timer, level_display_name, level_coin_count
        info = LEVELS[level_id]
        current_level_id = level_id
        level_display_name = info["name"]
        level_name_timer = 180
        level_coin_count = 0
        result = info["builder"]()
        if isinstance(result, tuple):
            if len(result) == 3:
                current_level_mesh, current_level_stars, current_level_coins = result
            elif len(result) == 2:
                current_level_mesh, current_level_stars = result
                current_level_coins = []
            else:
                current_level_mesh = result[0]
                current_level_stars = []
                current_level_coins = []
        else:
            current_level_mesh = result
            current_level_stars = []
            current_level_coins = []
        mario = Mario(0, 50, 400)
        mario.face_yaw = math.pi
        cam_yaw = math.pi
        cam_pitch = 0.15
        cam_dist = CAM_DIST
        cam_x = mario.x
        cam_y = mario.y + CAM_HEIGHT
        cam_z = mario.z + cam_dist
        vel_x = vel_z = 0.0

    def start_painting_warp(target_level):
        nonlocal current_state, painting_warp_timer, painting_warp_target
        current_state = STATE_PAINTING_WARP
        painting_warp_timer = 60
        painting_warp_target = target_level
        audio.play('painting')

    def draw_sm64_sky(level_id):
        sky = SM64_SKIES.get(level_id, ((80,144,248),(184,216,248),(160,200,240)))
        top, bot, fog = sky
        # Optimized: draw every 2nd line for speed
        for y in range(0, HEIGHT, 2):
            t = y / HEIGHT
            r = int(top[0]*(1-t) + bot[0]*t)
            g = int(top[1]*(1-t) + bot[1]*t)
            b = int(top[2]*(1-t) + bot[2]*t)
            c = (max(0,min(255,r)), max(0,min(255,g)), max(0,min(255,b)))
            pygame.draw.line(screen, c, (0, y), (WIDTH, y))
            if y + 1 < HEIGHT:
                pygame.draw.line(screen, c, (0, y+1), (WIDTH, y+1))
        return fog

    def draw_sm64_hud():
        """SM64 PC Port HUD — transparent bar, power meter, star/coin/lives"""
        nonlocal star_flash, coin_flash
        if not mario:
            return
        # Bottom HUD bar
        bar = pygame.Surface((WIDTH, 56))
        bar.set_alpha(160)
        bar.fill((0, 0, 0))
        screen.blit(bar, (0, HEIGHT - 56))
        pygame.draw.line(screen, (100, 100, 100), (0, HEIGHT - 56), (WIDTH, HEIGHT - 56), 2)

        # === STAR COUNTER (top-left, SM64 style) ===
        sc = YELLOW if star_flash <= 0 else WHITE
        star_text = font_hud_big.render(f"\u2605 x {len(collected_stars)}", True, sc)
        screen.blit(star_text, (20, 12))

        # === COIN COUNTER (top-left under stars) ===
        cc = YELLOW if coin_flash <= 0 else WHITE
        coin_text = font_hud.render(f"\u25CF x {level_coin_count}", True, cc)
        screen.blit(coin_text, (20, 42))

        # === LIVES COUNTER (bottom-left) ===
        # SM64 Mario head icon (simple)
        pygame.draw.circle(screen, MARIO_SKIN, (30, HEIGHT - 28), 10)
        pygame.draw.circle(screen, MARIO_CAP, (30, HEIGHT - 32), 8)
        lives_text = font_hud_big.render(f"x {mario.lives}", True, WHITE)
        screen.blit(lives_text, (46, HEIGHT - 40))

        # === POWER METER (SM64 pie wedge — bottom-right) ===
        pm_x = WIDTH - 70
        pm_y = HEIGHT - 32
        pm_r = 22
        # Background circle
        pygame.draw.circle(screen, (40, 40, 40), (pm_x, pm_y), pm_r)
        pygame.draw.circle(screen, (80, 80, 80), (pm_x, pm_y), pm_r, 2)
        # Health wedges (8 segments = full health)
        if mario.health > 0:
            for i in range(mario.health):
                angle_start = math.pi / 2 + (i * math.pi * 2 / 8)
                angle_end = math.pi / 2 + ((i + 1) * math.pi * 2 / 8)
                # Color ramp: green -> yellow -> red
                if mario.health >= 6:
                    wc = (0, 200, 0)
                elif mario.health >= 4:
                    wc = (200, 200, 0)
                elif mario.health >= 2:
                    wc = (200, 120, 0)
                else:
                    wc = (220, 20, 20)
                points = [(pm_x, pm_y)]
                for a in range(6):
                    ang = angle_start + (angle_end - angle_start) * a / 5
                    points.append((pm_x + math.cos(ang) * (pm_r - 3),
                                   pm_y - math.sin(ang) * (pm_r - 3)))
                if len(points) >= 3:
                    pygame.draw.polygon(screen, wc, points)

        # === FPS COUNTER ===
        fps_text = font_small.render(f"FPS:{int(clock.get_fps())}", True, (0, 200, 0))
        screen.blit(fps_text, (WIDTH - 80, 8))

        # === LEVEL NAME (bottom center) ===
        if current_level_id:
            n = font_small.render(LEVELS[current_level_id]["name"], True, WHITE)
            screen.blit(n, (WIDTH // 2 - n.get_width() // 2, HEIGHT - 40))

        # === CAMERA MODE INDICATOR ===
        cam_label = "LAKITU CAM" if cam_mode == 0 else "MARIO CAM"
        cam_text = font_small.render(cam_label, True, (180, 180, 180))
        screen.blit(cam_text, (WIDTH - 100, HEIGHT - 18))

        # === ACTION STATE (SM64 PC port debug-style) ===
        if action_display_timer > 0:
            a_alpha = min(255, action_display_timer * 8)
            at = font_action.render(action_display, True, YELLOW)
            screen.blit(at, (WIDTH // 2 - at.get_width() // 2, HEIGHT - 76))

        star_flash = max(0, star_flash - 1)
        coin_flash = max(0, coin_flash - 1)

    def draw_level_intro():
        nonlocal level_name_timer
        if level_name_timer > 0:
            a = min(255, level_name_timer * 3)
            ov = pygame.Surface((WIDTH, 80))
            ov.set_alpha(a)
            ov.fill(BLACK)
            screen.blit(ov, (0, HEIGHT // 2 - 40))
            t = font_big.render(level_display_name, True, YELLOW)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 20))
            # Course number
            if current_level_id and current_level_id.startswith("c"):
                try:
                    cnum = int(current_level_id[1:3])
                    ct = font_menu.render(f"COURSE {cnum}", True, WHITE)
                    screen.blit(ct, (WIDTH // 2 - ct.get_width() // 2, HEIGHT // 2 - 38))
                except:
                    pass
            level_name_timer -= 1

    def draw_painting_warp():
        """SM64 painting warp ripple effect"""
        nonlocal painting_warp_timer, current_state
        if painting_warp_timer > 0:
            # Expanding ripple circles
            progress = 1.0 - painting_warp_timer / 60.0
            for r in range(int(progress * 20)):
                radius = int(r * 30 * progress + progress * 100)
                alpha = max(0, 255 - r * 20)
                color_idx = r % 6
                rc = RR_RAINBOW[color_idx]
                try:
                    pygame.draw.circle(screen, rc, (WIDTH // 2, HEIGHT // 2), radius, 3)
                except:
                    pass
            # White flash at end
            if painting_warp_timer < 10:
                flash = pygame.Surface((WIDTH, HEIGHT))
                flash.set_alpha(int((10 - painting_warp_timer) * 25))
                flash.fill(WHITE)
                screen.blit(flash, (0, 0))
            painting_warp_timer -= 1
            if painting_warp_timer <= 0:
                load_level(painting_warp_target)
                current_state = STATE_GAME

    def draw_star_get():
        """SM64 star collection screen"""
        nonlocal star_get_timer, current_state
        # Dark overlay
        ov = pygame.Surface((WIDTH, HEIGHT))
        ov.set_alpha(180)
        ov.fill(BLACK)
        screen.blit(ov, (0, 0))
        # Rotating star
        star_angle = star_get_timer * 0.1
        sx = WIDTH // 2 + math.cos(star_angle) * 20
        sy = HEIGHT // 2 - 60 + math.sin(star_get_timer * 0.05) * 10
        # Big star shape
        star_size = 40 + math.sin(star_get_timer * 0.15) * 8
        for i in range(5):
            a1 = math.pi / 2 + i * 2 * math.pi / 5
            a2 = math.pi / 2 + (i + 0.5) * 2 * math.pi / 5
            x1 = sx + math.cos(a1) * star_size
            y1 = sy - math.sin(a1) * star_size
            x2 = sx + math.cos(a2) * star_size * 0.4
            y2 = sy - math.sin(a2) * star_size * 0.4
            try:
                pygame.draw.line(screen, YELLOW, (sx, sy), (x1, y1), 4)
                pygame.draw.line(screen, BUTTON_GOLD, (x1, y1), (x2, y2), 3)
            except:
                pass
        # Star sparkles
        for i in range(8):
            sa = i * math.pi / 4 + star_angle * 2
            sr = 60 + math.sin(star_get_timer * 0.2 + i) * 20
            sparkle_x = sx + math.cos(sa) * sr
            sparkle_y = sy + math.sin(sa) * sr
            pygame.draw.circle(screen, WHITE, (int(sparkle_x), int(sparkle_y)), 2)
        # Text
        t1 = font_star_get.render("STAR GET!", True, YELLOW)
        screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 + 20))
        t2 = font_menu.render(star_get_name, True, WHITE)
        screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 + 72))
        total = font_menu.render(f"Total Stars: {len(collected_stars)}/{STAR_TOTAL}", True, BUTTON_GOLD)
        screen.blit(total, (WIDTH // 2 - total.get_width() // 2, HEIGHT // 2 + 108))
        star_get_timer -= 1
        if star_get_timer <= 0:
            current_state = STATE_GAME

    # ========================================================
    # MAIN GAME LOOP
    # ========================================================
    running = True
    while running:
        dt = clock.tick(FPS)
        time_sec = pygame.time.get_ticks() / 1000.0

        if action_display_timer > 0:
            action_display_timer -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # === TITLE SCREEN ===
            if current_state == STATE_TITLE:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        audio.play('menu_select')
                        current_state = STATE_FILE_SELECT

            # === FILE SELECT ===
            elif current_state == STATE_FILE_SELECT:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_TITLE
                    elif event.key == pygame.K_UP:
                        file_selected = (file_selected - 1) % 5
                        audio.play('menu_cursor')
                    elif event.key == pygame.K_DOWN:
                        file_selected = (file_selected + 1) % 5
                        audio.play('menu_cursor')
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        audio.play('menu_select')
                        if file_selected < 4:
                            current_save = file_selected
                            sf = save_files[current_save]
                            collected_stars = sf.stars.copy()
                            total_coins = sf.coins
                            sf.exists = True
                            current_state = STATE_GAME
                            load_level("castle_grounds")
                        else:
                            # Level select
                            current_state = STATE_LEVEL_SELECT
                            level_select_idx = 0

            # === LEVEL SELECT ===
            elif current_state == STATE_LEVEL_SELECT:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_FILE_SELECT
                    elif event.key == pygame.K_UP:
                        level_select_idx = (level_select_idx - 1) % len(level_keys)
                        audio.play('menu_cursor')
                    elif event.key == pygame.K_DOWN:
                        level_select_idx = (level_select_idx + 1) % len(level_keys)
                        audio.play('menu_cursor')
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        audio.play('menu_select')
                        current_state = STATE_GAME
                        load_level(level_keys[level_select_idx])

            # === IN-GAME ===
            elif current_state == STATE_GAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_PAUSE
                    elif event.key == pygame.K_SPACE and mario:
                        if mario.is_on_ground() and mario.action not in (ACT_GROUND_POUND_LAND, ACT_DIVE_SLIDE, ACT_STAR_DANCE):
                            keys = pygame.key.get_pressed()
                            if keys[pygame.K_LSHIFT] and mario.speed > 6:
                                mario.do_long_jump(audio)
                                show_action("LONG JUMP")
                            else:
                                mario.do_jump(audio)
                                if mario.action == ACT_TRIPLE_JUMP:
                                    show_action("TRIPLE JUMP!")
                                elif mario.action == ACT_DOUBLE_JUMP:
                                    show_action("DOUBLE JUMP")
                                elif mario.action == ACT_BACKFLIP:
                                    show_action("BACKFLIP!")
                                else:
                                    show_action("JUMP")
                    elif event.key == pygame.K_z and mario and mario.is_airborne():
                        mario.do_ground_pound(audio)
                        show_action("GROUND POUND!")
                    elif event.key == pygame.K_x and mario and mario.is_airborne():
                        mario.do_dive(audio)
                        show_action("DIVE!")
                    elif event.key == pygame.K_c and mario and mario.is_on_ground():
                        if mario.action != ACT_CROUCH:
                            mario.action = ACT_CROUCH
                            show_action("CROUCH")
                    elif event.key == pygame.K_r and mario:
                        # Camera mode toggle (SM64 R button)
                        cam_mode = 1 - cam_mode
                        if cam_mode == 0:
                            cam_dist = CAM_DIST
                        else:
                            cam_dist = 250
                    elif event.key == pygame.K_e:
                        # Level transitions (painting warps)
                        if current_level_id == "castle_grounds":
                            if mario and abs(mario.x) < 100 and mario.z < -900:
                                start_painting_warp("castle_f1")
                        elif current_level_id == "castle_f1":
                            entered = False
                            if mario:
                                for p in CASTLE_F1_PAINTINGS:
                                    if abs(mario.x - p["pos"][0]) < 150 and abs(mario.z - p["pos"][2]) < 150:
                                        start_painting_warp(p["level"])
                                        entered = True
                                        break
                                if not entered:
                                    if abs(mario.x - 600) < 100 and abs(mario.z - 600) < 100:
                                        start_painting_warp("castle_basement")
                                    elif abs(mario.x) < 200 and mario.z < -800:
                                        start_painting_warp("castle_upper")
                                    elif abs(mario.x) < 200 and mario.z > 800:
                                        start_painting_warp("castle_grounds")
                                    elif abs(mario.x) < 100 and abs(mario.z) < 100 and mario.y > 50:
                                        start_painting_warp("s_slide")
                        elif current_level_id == "castle_basement":
                            entered = False
                            if mario:
                                for p in BASEMENT_PAINTINGS:
                                    if abs(mario.x - p["pos"][0]) < 150 and abs(mario.z - p["pos"][2]) < 150:
                                        start_painting_warp(p["level"])
                                        entered = True
                                        break
                                if not entered:
                                    if abs(mario.x - 800) < 100 and abs(mario.z - 800) < 100:
                                        start_painting_warp("s_metal")
                                    elif abs(mario.x - 600) < 100 and abs(mario.z + 1178) < 100:
                                        start_painting_warp("s_vanish")
                                    elif abs(mario.x) < 200 and mario.z > 1000:
                                        start_painting_warp("castle_f1")
                                    elif abs(mario.x) < 100 and abs(mario.z + 600) < 100:
                                        start_painting_warp("b1_dark")
                        elif current_level_id == "castle_upper":
                            entered = False
                            if mario:
                                for p in UPPER_PAINTINGS:
                                    if abs(mario.x - p["pos"][0]) < 150 and abs(mario.z - p["pos"][2]) < 150:
                                        start_painting_warp(p["level"])
                                        entered = True
                                        break
                                if not entered:
                                    if abs(mario.x) < 200 and mario.z < -600:
                                        start_painting_warp("castle_top")
                                    elif abs(mario.x) < 200 and mario.z > 600:
                                        start_painting_warp("castle_f1")
                                    elif abs(mario.x - 600) < 200 and abs(mario.z) < 200:
                                        start_painting_warp("b2_fire")
                        elif current_level_id == "castle_top":
                            if mario:
                                if abs(mario.x) < 100 and abs(mario.z) < 100:
                                    start_painting_warp("s_tower")
                                elif abs(mario.x) < 200 and mario.z > 300:
                                    start_painting_warp("castle_upper")
                                elif mario.y > 100:
                                    start_painting_warp("b3_sky")
                        else:
                            start_painting_warp("castle_f1")
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_c and mario:
                        if mario.action == ACT_CROUCH:
                            mario.action = ACT_IDLE

            # === PAUSE ===
            elif current_state == STATE_PAUSE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_GAME
                    elif event.key == pygame.K_q:
                        current_state = STATE_FILE_SELECT
                    elif event.key == pygame.K_r:
                        if current_level_id:
                            load_level(current_level_id)
                            current_state = STATE_GAME

        # ============ UPDATE ============

        if current_state == STATE_GAME and mario:
            keys = pygame.key.get_pressed()

            # === SM64 LAKITU CAMERA CONTROLS ===
            # Arrow keys = C-buttons (rotate camera around Mario)
            if keys[pygame.K_LEFT]:
                cam_yaw -= CAM_ANGLE_SPEED
            if keys[pygame.K_RIGHT]:
                cam_yaw += CAM_ANGLE_SPEED
            if keys[pygame.K_UP]:
                cam_pitch = min(CAM_PITCH_MAX, cam_pitch + CAM_PITCH_SPEED)
            if keys[pygame.K_DOWN]:
                cam_pitch = max(CAM_PITCH_MIN, cam_pitch - CAM_PITCH_SPEED)
            # Zoom (R = toggle handled in events, +/- for fine control)
            if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:
                cam_dist = max(CAM_ZOOM_MIN, cam_dist - CAM_ZOOM_STEP * 0.5)
            if keys[pygame.K_MINUS]:
                cam_dist = min(CAM_ZOOM_MAX, cam_dist + CAM_ZOOM_STEP * 0.5)

            # === SM64-STYLE MOVEMENT ===
            if mario.action not in (ACT_STAR_DANCE, ACT_DEATH, ACT_GROUND_POUND_LAND, ACT_DIVE_SLIDE):
                # Movement relative to camera (SM64 analog stick)
                fwd_x = -math.sin(cam_yaw)
                fwd_z = -math.cos(cam_yaw)
                right_x = math.cos(cam_yaw)
                right_z = -math.sin(cam_yaw)
                accel_x = accel_z = 0
                moving = False

                if mario.action == ACT_CROUCH:
                    # Crawling (slower)
                    speed_mult = 0.3
                else:
                    speed_mult = 1.0

                if keys[pygame.K_w]:
                    accel_x += fwd_x * MOVE_ACCEL * speed_mult
                    accel_z += fwd_z * MOVE_ACCEL * speed_mult
                    moving = True
                if keys[pygame.K_s]:
                    accel_x -= fwd_x * MOVE_ACCEL * 0.5 * speed_mult
                    accel_z -= fwd_z * MOVE_ACCEL * 0.5 * speed_mult
                    moving = True
                if keys[pygame.K_a]:
                    accel_x -= right_x * MOVE_ACCEL * 0.7 * speed_mult
                    accel_z -= right_z * MOVE_ACCEL * 0.7 * speed_mult
                    moving = True
                if keys[pygame.K_d]:
                    accel_x += right_x * MOVE_ACCEL * 0.7 * speed_mult
                    accel_z += right_z * MOVE_ACCEL * 0.7 * speed_mult
                    moving = True

                vel_x = (vel_x + accel_x) * MOVE_DECEL
                vel_z = (vel_z + accel_z) * MOVE_DECEL
                speed = math.sqrt(vel_x * vel_x + vel_z * vel_z)

                # Sprint
                sprint = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
                max_spd = SPRINT_SPEED if sprint else MAX_RUN_SPEED
                if speed > max_spd:
                    vel_x *= max_spd / speed
                    vel_z *= max_spd / speed
                    speed = max_spd

                # Move Mario
                mario.x += vel_x
                mario.z += vel_z

                # Face direction of movement (SM64 style)
                if moving and speed > 1.0:
                    target_yaw = math.atan2(-vel_x, -vel_z)
                    # Smooth rotation (SM64 style lerp)
                    diff = target_yaw - mario.face_yaw
                    while diff > math.pi: diff -= 2 * math.pi
                    while diff < -math.pi: diff += 2 * math.pi
                    mario.face_yaw += diff * 0.25
                    mario.yaw = mario.face_yaw

                # Update action state
                if mario.is_on_ground() and mario.action not in (ACT_CROUCH, ACT_GROUND_POUND_LAND, ACT_DIVE_SLIDE):
                    if speed > 10:
                        mario.action = ACT_RUNNING
                    elif speed > 2:
                        mario.action = ACT_WALKING
                    else:
                        mario.action = ACT_IDLE

                mario.speed = speed

            mario.update()

            # === SM64 LAKITU CAMERA POSITIONING ===
            # Camera orbits behind Mario at cam_dist, cam_height offset
            target_cam_x = mario.x + math.sin(cam_yaw) * cam_dist
            target_cam_z = mario.z + math.cos(cam_yaw) * cam_dist
            target_cam_y = mario.y + CAM_HEIGHT + math.sin(cam_pitch) * cam_dist * 0.5

            cam_x += (target_cam_x - cam_x) * CAM_LERP
            cam_y += (target_cam_y - cam_y) * CAM_LERP
            cam_z += (target_cam_z - cam_z) * CAM_LERP

            # Lakitu auto-yaw catchup (camera slowly follows Mario's facing)
            if cam_mode == 0 and speed > 5:
                target_auto_yaw = mario.face_yaw + math.pi
                diff = target_auto_yaw - cam_yaw
                while diff > math.pi: diff -= 2 * math.pi
                while diff < -math.pi: diff += 2 * math.pi
                cam_yaw += diff * LAKITU_YAW_CATCHUP

            # === COLLECTIBLES ===
            for star in current_level_stars:
                if not star.collected:
                    star.yaw += 0.05
                    dx = mario.x - star.x
                    dy = mario.y - star.y
                    dz = mario.z - star.z
                    if math.sqrt(dx*dx + dy*dy + dz*dz) < 60:
                        star.collected = True
                        star_key = f"{current_level_id}_{star.star_id}"
                        collected_stars.add(star_key)
                        star_flash = 30
                        audio.play('star')
                        # Star get cutscene
                        star_get_timer = 120
                        star_get_name = f"{LEVELS[current_level_id]['name']} - Star {star.star_id + 1}"
                        mario.action = ACT_STAR_DANCE
                        current_state = STATE_STAR_GET
                        # Save
                        sf = save_files[current_save]
                        sf.stars = collected_stars.copy()
                        sf.coins = total_coins

            for coin in current_level_coins:
                if not coin.collected:
                    coin.yaw += 0.08
                    dx = mario.x - coin.x
                    dy = mario.y - coin.y
                    dz = mario.z - coin.z
                    if math.sqrt(dx*dx + dy*dy + dz*dz) < 40:
                        coin.collected = True
                        total_coins += 1
                        level_coin_count += 1
                        coin_flash = 15
                        audio.play('coin')
                        mario.health = min(8, mario.health + 1)
                        # 1-UP at 50 coins
                        if level_coin_count % 50 == 0:
                            mario.lives += 1
                            audio.play('oneup')

        # ============ RENDER ============

        if current_state == STATE_TITLE:
            # SM64 PC Port title screen
            for y in range(HEIGHT):
                t = y / HEIGHT
                r = int(20 * (1 - t))
                g = int(10 * (1 - t))
                b = int(60 * (1 - t) + 20)
                pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
            # Rotating Mario head
            menu_head.yaw += 0.02
            polys = render_mesh(screen, menu_head, 0, 0, 200, 0, 0, cx, cy, is_menu=True)
            polys.sort(key=lambda x: x['depth'], reverse=True)
            for p in polys:
                pygame.draw.polygon(screen, p['color'], p['poly'])
                pygame.draw.polygon(screen, BLACK, p['poly'], 1)
            # Title text (SM64 PC port style)
            ly = 40 + math.sin(time_sec) * 5
            # Shadow
            ts = font_title.render("SUPER MARIO 64", True, (180, 20, 20))
            screen.blit(ts, (WIDTH // 2 - ts.get_width() // 2 + 3, ly + 3))
            ts = font_title.render("SUPER MARIO 64", True, YELLOW)
            screen.blit(ts, (WIDTH // 2 - ts.get_width() // 2, ly))
            # Subtitle
            sub1 = font_subtitle.render("AC'S SM64 PC PORT — PY EDITION 0.1", True, WHITE)
            screen.blit(sub1, (WIDTH // 2 - sub1.get_width() // 2, ly + 70))
            # Copyright
            copy_text = font_small.render("(C) 2026 A.C Holdings / Team Flames", True, LIGHT_GREY)
            screen.blit(copy_text, (WIDTH // 2 - copy_text.get_width() // 2, ly + 100))
            # Press start
            if int(time_sec * 2) % 2 == 0:
                start = font_menu.render("PRESS START", True, WHITE)
                screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT - 100))
            # Bottom text
            ver = font_small.render("All 15 Courses + 5 Secret + 3 Bowser | SM64 PC Port Authentic", True, METAL_GREY)
            screen.blit(ver, (WIDTH // 2 - ver.get_width() // 2, HEIGHT - 30))

        elif current_state == STATE_FILE_SELECT:
            # SM64 File Select screen
            screen.fill((16, 8, 32))
            # Header
            t = font_big.render("SELECT FILE", True, YELLOW)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 30))
            # File slots A-D
            slot_labels = ["A", "B", "C", "D"]
            for i in range(4):
                y_pos = 100 + i * 100
                sel = i == file_selected
                # Box
                box_color = YELLOW if sel else (80, 80, 80)
                pygame.draw.rect(screen, box_color, (120, y_pos, WIDTH - 240, 80), 3 if sel else 1)
                if sel:
                    pygame.draw.rect(screen, (30, 20, 50), (123, y_pos + 3, WIDTH - 246, 74))
                # Mario icon
                pygame.draw.circle(screen, MARIO_SKIN if save_files[i].exists else DARK_GREY,
                                   (160, y_pos + 40), 16)
                pygame.draw.circle(screen, MARIO_CAP if save_files[i].exists else (60, 60, 60),
                                   (160, y_pos + 32), 12)
                # File label
                label = font_menu.render(f"FILE {slot_labels[i]}", True, WHITE if sel else LIGHT_GREY)
                screen.blit(label, (200, y_pos + 10))
                # Star count
                sf = save_files[i]
                if sf.exists:
                    stars_text = font_menu.render(f"\u2605 x {sf.star_count()}", True, YELLOW)
                    screen.blit(stars_text, (200, y_pos + 44))
                else:
                    empty = font_small.render("- EMPTY -", True, (100, 100, 100))
                    screen.blit(empty, (200, y_pos + 48))
            # Level Select option
            ls_y = 100 + 4 * 100
            ls_sel = file_selected == 4
            pygame.draw.rect(screen, YELLOW if ls_sel else (80, 80, 80), (120, ls_y, WIDTH - 240, 50), 3 if ls_sel else 1)
            ls_text = font_menu.render("LEVEL SELECT", True, WHITE if ls_sel else LIGHT_GREY)
            screen.blit(ls_text, (WIDTH // 2 - ls_text.get_width() // 2, ls_y + 12))
            # Controls
            ctrl = font_small.render("UP/DOWN: Navigate | ENTER: Select | ESC: Back", True, METAL_GREY)
            screen.blit(ctrl, (WIDTH // 2 - ctrl.get_width() // 2, HEIGHT - 30))

        elif current_state == STATE_LEVEL_SELECT:
            screen.fill((8, 8, 24))
            t = font_big.render("LEVEL SELECT", True, YELLOW)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 16))
            vs = max(0, level_select_idx - 14)
            ve = min(len(level_keys), vs + 20)
            y = 64
            for i in range(vs, ve):
                k = level_keys[i]
                info = LEVELS[k]
                sel = i == level_select_idx
                c = YELLOW if sel else WHITE
                pfx = "\u25B6 " if sel else "  "
                if k.startswith("castle"):
                    dc = CG_CASTLE_WALL
                elif k.startswith("c"):
                    dc = BOB_GRASS_1
                elif k.startswith("s"):
                    dc = (0, 200, 200)
                else:
                    dc = LLL_LAVA_1
                screen.blit(font_menu.render(f"{pfx}{info['name']}", True, c), (36, y))
                screen.blit(font_small.render(f"Req:{info['req']}\u2605", True, dc), (640, y + 4))
                pygame.draw.circle(screen, dc, (22, y + 12), 5)
                y += 30
            screen.blit(font_small.render("UP/DOWN: Navigate | ENTER: Play | ESC: Back", True, METAL_GREY),
                        (WIDTH // 2 - 180, HEIGHT - 28))

        elif current_state == STATE_GAME:
            fog_color = draw_sm64_sky(current_level_id)

            # === RENDER SCENE ===
            all_polys = []
            if current_level_mesh:
                all_polys.extend(render_mesh(screen, current_level_mesh,
                                             cam_x, cam_y, cam_z, cam_yaw, cam_pitch, cx, cy))
            # Render Mario (third-person — visible!)
            if mario:
                mario_polys = render_mesh(screen, mario,
                                          cam_x, cam_y, cam_z, cam_yaw, cam_pitch, cx, cy)
                # Invincibility flash
                if mario.invincible_timer > 0 and int(time_sec * 10) % 2 == 0:
                    for mp in mario_polys:
                        mp['color'] = WHITE
                all_polys.extend(mario_polys)

            for star in current_level_stars:
                if not star.collected:
                    all_polys.extend(render_mesh(screen, star,
                                                  cam_x, cam_y, cam_z, cam_yaw, cam_pitch, cx, cy))
            for coin in current_level_coins:
                if not coin.collected:
                    all_polys.extend(render_mesh(screen, coin,
                                                  cam_x, cam_y, cam_z, cam_yaw, cam_pitch, cx, cy))

            all_polys.sort(key=lambda x: x['depth'], reverse=True)

            for item in all_polys:
                depth = item['depth']
                fog = min(1.0, depth / VIEW_DISTANCE)
                r, g, b = item['color']
                fr = int(r + (fog_color[0] - r) * fog)
                fg = int(g + (fog_color[1] - g) * fog)
                fb = int(b + (fog_color[2] - b) * fog)
                pygame.draw.polygon(screen,
                                    (max(0, min(255, fr)), max(0, min(255, fg)), max(0, min(255, fb))),
                                    item['poly'])

            draw_sm64_hud()
            draw_level_intro()

            # Context hint
            hint = ""
            if current_level_id and "castle" in current_level_id:
                hint = "E: Enter Door/Painting"
            elif current_level_id:
                hint = "E: Exit Level"
            if hint:
                screen.blit(font_small.render(hint, True, YELLOW), (WIDTH // 2 - 60, 8))

            # Controls reminder
            ctrl_hint = font_small.render(
                "WASD:Move  SPACE:Jump  Z:GroundPound  X:Dive  C:Crouch  SHIFT+SPACE:LongJump  R:Camera",
                True, (120, 120, 120))
            screen.blit(ctrl_hint, (10, HEIGHT - 72))

        elif current_state == STATE_PAUSE:
            # Draw game behind pause
            if current_level_id:
                fog_color = draw_sm64_sky(current_level_id)
            ov = pygame.Surface((WIDTH, HEIGHT))
            ov.set_alpha(180)
            ov.fill(BLACK)
            screen.blit(ov, (0, 0))
            # SM64 pause menu
            pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 160, 100, 320, 400), 3)
            screen.blit(font_big.render("PAUSE", True, YELLOW), (WIDTH // 2 - 50, 120))
            pause_items = [
                ("ESC - Continue", WHITE),
                ("R - Restart Level", WHITE),
                ("Q - Quit to Menu", WHITE),
                ("", WHITE),
                (f"\u2605 Stars: {len(collected_stars)}/{STAR_TOTAL}", YELLOW),
                (f"\u25CF Coins: {level_coin_count} (Total: {total_coins})", YELLOW),
                (f"\u2665 Lives: {mario.lives if mario else 4}", RED),
                (f"\u2764 Health: {mario.health if mario else 8}/8", (0, 200, 0)),
                ("", WHITE),
                (f"Level: {level_display_name}", WHITE),
            ]
            for i, (t, c) in enumerate(pause_items):
                if t:
                    screen.blit(font_menu.render(t, True, c), (WIDTH // 2 - 130, 176 + i * 32))

        elif current_state == STATE_STAR_GET:
            if current_level_id:
                draw_sm64_sky(current_level_id)
            draw_star_get()

        elif current_state == STATE_PAINTING_WARP:
            if current_level_id:
                draw_sm64_sky(current_level_id)
            draw_painting_warp()

        # SM64 CRT scanline effect (subtle, every 4th line)
        for y in range(0, HEIGHT, 4):
            pygame.draw.line(screen, (0, 0, 0), (0, y), (WIDTH, y), 1)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
