import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct):
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：横方向・縦方向の真理値タプル（True：画面内／False：画面外）
    Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False

    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0,0,0))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = (random.randint(0,WIDTH))
    bb_rct.centery = (random.randint(0,HEIGHT))
    clock = pg.time.Clock()
    tmr = 0
    vx = +5
    vy = +5
    DELTA = {pg.K_UP:(0, -5), pg.K_DOWN:(0, +5), pg.K_LEFT:(-5, 0), pg.K_RIGHT:(+5, 0)}
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        #爆弾のyoko,tateのTrue,Falseを読み取る変数bb_TF
        bb_TF = check_bound(bb_rct)
        if bb_TF[0] == False:
            vx *= -1
        if bb_TF[1] == False:
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        if kk_rct.colliderect(bb_rct):
            return -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
