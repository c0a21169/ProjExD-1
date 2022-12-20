import pygame as pg
import random
import sys

key_delta = {
    pg.K_UP:    [0, -1],
    pg.K_DOWN:  [0, +1],
    pg.K_LEFT:  [-1, 0],
    pg.K_RIGHT: [+1, 0],
}


class Screen:
    def __init__(self, title, whtpl, bgfile):
        self.title = title
        self.whtpl = whtpl
        pg.display.set_caption(self.title)
        self.sfc = pg.display.set_mode(self.whtpl)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(bgfile)
        self.bgi_rct = self.bgi_sfc.get_rect()
 
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0], }

    def __init__(self, figfile, zoom, center):
        self.sfc = pg.image.load(figfile)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = center

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr):
        key_dct = pg.key.get_pressed()
        for key, delta in key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
            # 練習7
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        scr.sfc.blit(self.sfc, self.rct) # 練習3


class Bomb:
    def __init__(self, colortpl, radius, speedtpl, scr):
        self.sfc = pg.Surface((20, 20)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, colortpl, (radius, radius), radius)
        self.rct = self.sfc.get_rect()
        inx = random.randint(0, scr.rct.width)
        iny = random.randint(0, scr.rct.height)
        self.rct.centerx = inx
        self.rct.centery = iny
        scr.sfc.blit(self.sfc, self.rct)
        self.vx, self.vy = speedtpl

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)
    

    def update(self, scr):
        self.rct.move_ip(self.vx, self.vy)
        scr.sfc.blit(self.sfc, self.rct) 
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate


def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    time = 0

    clock =pg.time.Clock()

    scr = Screen("逃げろ！こうかとん", (1600, 900), "fig/pg_bg.jpg")
    scr.blit()

    ttb = Bird("fig/6.png", 2.0, (900, 400))
    ttb.blit(scr)

    bombs = []
    vx = random.choice([-1, +1])
    vy = random.choice([-1, +1])
    bombs.append(Bomb("red", 10, (vx, vy), scr))

    while True:
        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        ttb.update(scr)

        if time % 1000 == 0:
            vx = random.choice([-1, +1])
            vy = random.choice([-1, +1])
            bombs.append(Bomb("red", 10, (vx, vy), scr))

        for bom in bombs:
            bom.update(scr)

            if ttb.rct.colliderect(bom.rct):
                return

        pg.display.update()
        time += 1
        clock.tick(1000)

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()