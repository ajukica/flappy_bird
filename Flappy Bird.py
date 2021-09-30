import pygame, sys, random

from pygame.transform import rotate

def nacrtaj_pod():
    # dva ista tla 
    prikaz.blit(tlo_povrsina,(tlo_x_pos,900))
    prikaz.blit(tlo_povrsina,(tlo_x_pos + 576,900))

def stvori_cijev():
    random_cjev = random.choice(cjevi_visine)
    donja_cjev =  cjevi_povrsina.get_rect(midtop = (650,random_cjev)) 
    gornja_cjev = cjevi_povrsina.get_rect(midbottom = (650,random_cjev - 300)) 
    return donja_cjev, gornja_cjev 

def pomakni_cjevi(cjevi):
    for cjev in cjevi:
        cjev.centerx -= 5
    return cjevi

def nacrtaj_cjevi (cjevi):
    for cjev in cjevi:
        if cjev.bottom >= 1024:
            prikaz.blit(cjevi_povrsina,cjev)
        else:
            okreni_cjev = pygame.transform.flip(cjevi_povrsina,False,True)
            prikaz.blit(okreni_cjev,cjev)

def sudar (cjevi):
    for cjev in cjevi:
        if ptica_pr.colliderect(cjev):
            return False 
    if ptica_pr.top <= -100 or ptica_pr.bottom >= 900:
        return False
    return True

def rotiraj_pticu(ptica):
    nova_ptica = pygame.transform.rotozoom(ptica,-ptica_let * 3,1)
    return nova_ptica

def ptica_animacija():
    nova_ptica = ptica_frames[ptica_index] 
    nova_ptica_pr = nova_ptica.get_rect(center = (100,ptica_pr.centery))
    return nova_ptica,nova_ptica_pr

def prikazi_rezultat(status):
    if status == True:
        rezultat_povrsina = font_igra.render(str(int(rezultat)),True,(255,255,255))
        rezultat_pr = rezultat_povrsina.get_rect(center = (288,100))
        prikaz.blit(rezultat_povrsina,rezultat_pr)
    if status == False:

        rezultat_povrsina = font_igra.render(f'Rezultat: {int(rezultat)}',True,(255,255,255))
        rezultat_pr = rezultat_povrsina.get_rect(center = (288,100))
        prikaz.blit(rezultat_povrsina,rezultat_pr)

        najbolji_rezultat_povrsina = font_igra.render(f'Najbolji Rezultat: {int(najveci_rezultat)}',True,(255,255,255))
        najbolji_rezultat_pr = najbolji_rezultat_povrsina.get_rect(center = (288,850))
        prikaz.blit(najbolji_rezultat_povrsina,najbolji_rezultat_pr)

def osvjezi_najbolji_rezultat(rezultat,najveci_rezultat):
    if rezultat > najveci_rezultat:
        najveci_rezultat = rezultat
    return najveci_rezultat



pygame.init()
prikaz = pygame.display.set_mode((576,1024))
timer = pygame.time.Clock()
font_igra = pygame.font.Font(None,40)

gravitacija = 0.26
ptica_let = 0
igra = True
rezultat = 0
najveci_rezultat = 0

bg_povrsina = pygame.image.load(r'c:/Users/Korisnik/Desktop/Projekti/Flappy Bird/assets/background-day.png')
bg_povrsina = pygame.transform.scale2x(bg_povrsina)


tlo_povrsina = pygame.image.load(r'c:/Users/Korisnik/Desktop/Projekti/Flappy Bird/assets/base.png')
tlo_povrsina = pygame.transform.scale2x(tlo_povrsina)
tlo_x_pos = 0

ptica_downflap = pygame.transform.scale2x(pygame.image.load('c:/Users/Korisnik/Desktop/Projekti/Flappy Bird/assets/bluebird-downflap.png'))
ptica_midflap = pygame.transform.scale2x(pygame.image.load('c:/Users/Korisnik/Desktop/Projekti/Flappy Bird/assets/bluebird-midflap.png'))
ptica_upflap = pygame.transform.scale2x(pygame.image.load('c:/Users/Korisnik/Desktop/Projekti/Flappy Bird/assets/bluebird-upflap.png'))
ptica_frames = [ptica_downflap,ptica_midflap,ptica_upflap]
ptica_index = 0
ptica_povrsina = ptica_frames[ptica_index]
ptica_pr = ptica_povrsina.get_rect(center =(100,512))

PTICAFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PTICAFLAP,200)

cjevi_povrsina = pygame.image.load(r'c:/Users/Korisnik/Desktop/Projekti/Flappy Bird/assets/pipe-green.png')
cjevi_povrsina = pygame.transform.scale2x(cjevi_povrsina)
cjevi_lista = []
STVORICJEV = pygame.USEREVENT
pygame.time.set_timer(STVORICJEV,1200)
cjevi_visine = [400,600,800] 


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and igra:
                ptica_let = 0
                ptica_let -= 8
            if event.key ==pygame.K_SPACE and igra == False:
                cjevi_lista.clear()
                ptica_pr.center = (100,512)
                igra = True
                ptica_let = 0
                rezultat = 0

        if event.type == STVORICJEV:
            cjevi_lista.extend(stvori_cijev())

        if event.type == PTICAFLAP:
            if ptica_index < 2:
                ptica_index += 1
            else: 
                ptica_index = 0
            
            ptica_povrsina,ptica_pr = ptica_animacija()

    prikaz.blit(bg_povrsina,(0,0))

    if igra == True:

        ptica_let += gravitacija
        rotirana_ptica = rotiraj_pticu(ptica_povrsina)
        ptica_pr.centery += ptica_let
        prikaz.blit(rotirana_ptica,ptica_pr)
        igra = sudar(cjevi_lista)

        stvori_cijev()
        cjevi_lista = pomakni_cjevi(cjevi_lista)
        nacrtaj_cjevi(cjevi_lista)
        
        rezultat += 0.01
        prikazi_rezultat(True)
    else:
        najveci_rezultat = osvjezi_najbolji_rezultat(rezultat,najveci_rezultat)
        prikazi_rezultat(False)


    tlo_x_pos -= 1
    nacrtaj_pod()
    if tlo_x_pos <= -576: # kontinuirano tlo (ponavljajuce)
        tlo_x_pos = 0

    pygame.display.update()
    timer.tick(120)