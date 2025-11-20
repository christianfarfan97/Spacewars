import pygame
import random
from player import Bala 
from player import Vida
class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/imagenes/asteroide.png").convert_alpha()  # Usá tu sprite de asteroide
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajustá tamaño si querés
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 600 - self.rect.width)  # Posición horizontal aleatoria (suponiendo ancho 600)
        self.rect.y = -self.rect.height  # Empieza justo arriba de la ventana
        self.velocidad = random.randint(2, 5)  # Velocidad aleatoria hacia abajo
        self.vida_asteroide = 50

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > 650:
            self.kill()  # Se elimina si sale de la pantalla abajo


class Enemigo(pygame.sprite.Sprite):
    def __init__(self, sonido_disparo_enemigo):
        super().__init__()
        self.image = pygame.image.load("assets/imagenes/enemigo.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (120, 130))
        self.rect = self.image.get_rect()
        self.sonido_disparo = sonido_disparo_enemigo
        self.rect.centerx = 300   # Posición inicial
        self.rect.bottom = 140    # Posición inicial
        self.velocidad = 5
        self.tiempo_ultimo_disparo = 0
        self.retraso_disparo = 1000
        self.velocidad_x = 5   # para movimiento horizontal
        self.velocidad = 3 
        self.vida = Vida(self, vida_maxima=100)

    
    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)      # dibujar enemigo
        self.vida.dibujar(pantalla)

    def disparar(self, grupo_balas_enemigos):
        bala = Bala(self.rect.centerx, self.rect.bottom, 3, (90,38,94))
        grupo_balas_enemigos.add(bala)
        self.sonido_disparo.play()

    def update(self, grupo_balas_jugador, grupo_balas_enemigos=None):
        # Movimiento vertical
        self.rect.x += self.velocidad_x

        # Cambiar dirección si toca los bordes
        if self.rect.left <= 0 or self.rect.right >= 600:
            self.velocidad_x = -self.velocidad_x  # invertir velocidad

        # Esquivar balas del jugador
        for bala in grupo_balas_jugador:
            if self.rect.top - 50 < bala.rect.bottom < self.rect.bottom + 50:
                if bala.rect.centerx < self.rect.centerx:
                    self.rect.x += self.velocidad  # esquivar derecha
                else:
                    self.rect.x -= self.velocidad   # mover izquierda

                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.right > 600:
                    self.rect.right = 600

            

        # Disparo automático con temporizador
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_disparo > self.retraso_disparo:
            self.disparar(grupo_balas_enemigos)
            self.tiempo_ultimo_disparo = ahora
        # Ahora definir un nuevo retraso aleatorio para el próximo disparo
            self.retraso_disparo = random.randint(500, 2000)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet, sonido, cols=4, rows=4):
        super().__init__()
        self.frames = []
        self.current_frame = 0
        self.frame_width = spritesheet.get_width() // cols
        self.frame_height = spritesheet.get_height() // rows
        self.load_frames(spritesheet, cols, rows)
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 25  # ms por frame
        self.sonido = sonido
        self.sonido.play()

    def load_frames(self, spritesheet, cols, rows):
        for row in range(rows):
            for col in range(cols):
                frame = spritesheet.subsurface(
                    pygame.Rect(col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height))
                self.frames.append(frame)

    def update(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.last_update > self.frame_rate:
            self.last_update = ahora
            self.current_frame += 1
            if self.current_frame == len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.current_frame]



    