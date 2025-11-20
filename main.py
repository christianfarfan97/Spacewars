import pygame
import sys
from player import Jugador, Score , Vida , Bala
from enemy import Asteroide, Enemigo , Explosion

# pygame setup
pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((600,650))

clock = pygame.time.Clock()
corriendo = True

fondo_menu = pygame.image.load("assets/imagenes/fondo_menu.jpg").convert()
spritesheet_explosion = pygame.image.load("assets/imagenes/explosion.png").convert_alpha()
fondo = pygame.image.load("assets/imagenes/fondo_estrellado.jpg").convert()
fondo = pygame.transform.scale(fondo, (600,650))  
fondo_menu = pygame.transform.scale(fondo_menu, (600, 650))


sonido_disparo = pygame.mixer.Sound("assets/sonidos/disparo_jugador.mp3")
sonido_disparo_enemigo = pygame.mixer.Sound("assets/sonidos/disparo_enemigo.mp3")
sonido_explosion = pygame.mixer.Sound("assets/sonidos/explosion_asteroide.mp3")
pygame.mixer.music.load("assets/sonidos/musica_fondo.mp3")
pygame.mixer.music.play(-1)
sonido_disparo.set_volume(0.3)  
sonido_disparo_enemigo.set_volume(0.5) 
sonido_explosion.set_volume(0.3)


grupo_explosiones = pygame.sprite.Group()
jugador = Jugador(sonido_disparo)
todos_los_sprites = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
todos_los_sprites.add(jugador)
enemigo_principal = Enemigo(sonido_disparo_enemigo)
grupo_enemigos = pygame.sprite.Group()
grupo_enemigos.add(enemigo_principal)
grupo_balas_enemigos = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
todos_los_sprites.add(grupo_balas)
grupo_asteroides = pygame.sprite.Group()
vida_jugador = Vida(jugador, vida_maxima=100)
vida_enemigo = Vida(enemigo_principal, vida_maxima=500)
colisiones_balas_enemigos = pygame.sprite.groupcollide(grupo_balas, grupo_enemigos, True, False)
tiempo_ultimo_disparo = 0
retraso_disparo = 350
tiempo_ultimo_asteroide = 0
retraso_asteroide = 350

fuente = pygame.font.Font("fuentes/starjedi.ttf", 43)
fuente_score = pygame.font.Font("fuentes/starjedi.ttf", 26)  
score = Score(10, 10, fuente_score)  
instrucciones_menu = """       Elimina la nave enemiga    
    Esquiva balas y asteroides
          Si chocas, mueres
    Presiona ENTER para jugar"""


def dibujar_texto_multilinea(pantalla, texto, fuente, color, x, y, espacio):
    lineas = texto.splitlines()  
    for i, linea in enumerate(lineas):
        texto_render = fuente.render(linea, True, color)
        pantalla.blit(texto_render, (x, y + i * espacio))


def menu_inicio():
    seleccionando = True
    while seleccionando:
        pantalla.blit(fondo_menu, (0, 0))  
        titulo = fuente.render("Space Wars", True, (255, 255, 255))
        jugar = fuente.render("Jugar", True, (0, 255, 0))
        instrucciones = fuente_score.render(instrucciones_menu, True, (200, 200, 200))

        pantalla.blit(titulo, (pantalla.get_width() // 2 - titulo.get_width() // 2, 150))
        pantalla.blit(jugar, (pantalla.get_width() // 2 - jugar.get_width() // 2, 300))
        dibujar_texto_multilinea(pantalla, instrucciones_menu, fuente_score, (255, 255, 255), 50, 400, 30)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    seleccionando = False

        clock.tick(60)

menu_inicio()
while corriendo:
        for event in pygame.event.get():
            ahora = pygame.time.get_ticks()
            if event.type == pygame.QUIT:
                corriendo = False

        grupo_balas_enemigos.update()

        
        for enemigo in grupo_enemigos:
            enemigo.update(grupo_balas_jugador, grupo_balas_enemigos)
            


        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]:
            if ahora - tiempo_ultimo_disparo > retraso_disparo:
                    jugador.disparar(grupo_balas,sonido_disparo)
                    tiempo_ultimo_disparo = ahora


            if ahora - tiempo_ultimo_asteroide > retraso_asteroide:
                nuevo_asteroide = Asteroide()
                grupo_asteroides.add(nuevo_asteroide)
                tiempo_ultimo_asteroide = ahora
                        
            
            colisiones = pygame.sprite.groupcollide(grupo_asteroides, grupo_balas, True, True)
            for asteroide in colisiones:
                explosion = Explosion(asteroide.rect.centerx, asteroide.rect.centery, spritesheet_explosion, sonido_explosion)
                grupo_explosiones.add(explosion)
                score.sumar(10)
                jugador.vida.vida_actual -= 1 
                if jugador.vida.vida_actual <= 0:
                   jugador.kill()
                
                   corriendo = False  
            colisiones = pygame.sprite.groupcollide(grupo_balas, grupo_enemigos, True, False)
            for bala, enemigos_impactados in colisiones.items():
                score.sumar(50)
                for enemigo in enemigos_impactados:
                    enemigo.vida.vida_actual -= 10  
                    if enemigo.vida.vida_actual <= 0:
                    
                        enemigo.kill()


        
        vida_jugador.actualizar(grupo_balas_enemigos, grupo_asteroides)
        if vida_jugador.esta_muerto():
            corriendo = False  



            
        
        pantalla.blit(fondo, (0, 0))
        

        for enemigo in grupo_enemigos:
            enemigo.dibujar(pantalla)
        grupo_balas.draw(pantalla)
        grupo_balas_enemigos.draw(pantalla)
        grupo_asteroides.update()
        todos_los_sprites.draw(pantalla)
        grupo_asteroides.draw(pantalla)
        todos_los_sprites.update()
        todos_los_sprites.draw(pantalla)
        grupo_balas.update()
        grupo_balas.draw(pantalla)
        grupo_explosiones.update()
        grupo_explosiones.draw(pantalla)
        score.dibujar(pantalla)
        vida_jugador.dibujar(pantalla)
         
        pygame.display.flip()

        clock.tick(60)

pygame.quit()
