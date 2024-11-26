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

def gameover(screen: pg.Surface) -> None:
    """
    引数：screen
    戻り値：なし
    こうかとんと爆弾が重なったとき
    GameOverを表示しゲームを終了する関数
    """
    kkcry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kkcry_rct1 = kkcry_img.get_rect()
    kkcry_rct1.center = 350, HEIGHT/2
    kkcry_rct2 = kkcry_img.get_rect()
    kkcry_rct2.center = WIDTH-350, HEIGHT/2
    bbg_img = pg.Surface((1100, 650))
    pg.draw.rect(bbg_img, (0,0,0),(0,0,1100,650), 0)
    bbg_img.set_alpha(128)
    GO = pg.font.Font(None, 80)
    txt = GO.render("GameOver", True, (255, 0, 0))
    txt_rect = txt.get_rect(center=(WIDTH/2, HEIGHT/2))

    screen.blit(bbg_img, [0,0])
    screen.blit(txt, txt_rect)
    screen.blit(kkcry_img, kkcry_rct1)
    screen.blit(kkcry_img, kkcry_rct2)
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    accs = [a for a in range(1, 11)]
    bb_imgs = []
    for i in range(1, 11):
        bb_img = pg.Surface((20*i, 20*i))
        pg.draw.circle(bb_img, (255, 0, 0), (10*i, 10*i), 10*i)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return bb_imgs, accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    kk1 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk2 = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9)
    kk3 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9)
    kk3 = pg.transform.flip(kk3, -1, 1)
    kk4 = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9)
    kk4 = pg.transform.flip(kk4, -1, 1)
    kk5 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk5 = pg.transform.flip(kk5, -1, 1)
    kk6 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9)
    kk7 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9)
    kk7 = pg.transform.flip(kk7, -1, 1)
    kk8 = pg.transform.rotozoom(kk3, 180, 1)
    kkk = kk1
    VEC = {(0, 0): kkk, (-5, 0):kk1, (-5, -5):kk2, (0, -5):kk3, (+5, -5):kk4, (+5, 0):kk5, (-5, +5):kk6, (+5, +5):kk7, (0, +5):kk8}
    return VEC[sum_mv]

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = (random.randint(0,WIDTH))
    bb_rct.centery = (random.randint(0,HEIGHT))

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
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
    
        bb_imgs, bb_accs = init_bb_imgs()
        bb_img = bb_imgs[min(tmr//100, 9)]

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_img = get_kk_img((0,0))
        kk_img = get_kk_img(tuple(sum_mv))
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
        avx = vx*bb_accs[min(tmr//100, 9)]
        avy = vy*bb_accs[min(tmr//100, 9)]
        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img, bb_rct)
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
