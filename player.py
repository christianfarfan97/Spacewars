import pygame


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad, color):
        super().__init__()
        self.image = pygame.Surface((5, 20))  # Tamaño ancho=5, alto=10 píxeles
        self.image.fill(color)  # Color rojo (RGB)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad = velocidad  # La bala va hacia arriba

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0 or self.rect.top > 650:
            self.kill()  # Elimina la bala fuera de la pantalla




class Jugador(pygame.sprite.Sprite):
    def __init__(self,sonido_disparo):
        super().__init__()
        self.image = pygame.image.load("assets/imagenes/jugador.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (120, 130))
        self.rect = self.image.get_rect()
        self.sonido_disparo = sonido_disparo
        self.rect.centerx = 600   # Posición inicial (centro horizontal)
        self.rect.bottom = 620    # Posición inicial (abajo de la pantalla)
        self.velocidad = 4
        self.vida = Vida(self, vida_maxima=100)
        self.invencible = False  # para controlar la invencibilidad
        self.tiempo_invencible = 1000  # duración invencibilidad en ms
        self.tiempo_ultimo_daño = 0  # timestamp del último daño recibido


    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < 600:
            self.rect.x += self.velocidad

    def disparar(self, grupo_balas,sonido_disparo):
        bala = Bala(self.rect.centerx, self.rect.top, -5,(75,182,196))
        grupo_balas.add(bala)
        sonido_disparo.play()


class Score:
    def __init__(self, x, y, fuente, color=(255, 255, 255)):
        self.puntaje = 0
        self.x = x
        self.y = y
        self.fuente = fuente
        self.color = color
        self.image = None
        self.rect = None
        self.actualizar_imagen()

    def sumar(self, puntos):
        self.puntaje += puntos
        self.actualizar_imagen()

    def actualizar_imagen(self):
        texto = f"Score: {self.puntaje}"
        self.image = self.fuente.render(texto, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)

import pygame

class Vida:
    def __init__(self, jugador, vida_maxima=100):
        self.jugador = jugador
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_maxima
        self.barra_ancho = jugador.rect.width
        self.barra_alto = 5

    def actualizar(self, grupo_balas_enemigas=None, grupo_asteroides=None):
        if grupo_balas_enemigas:
            col_balas = pygame.sprite.spritecollide(self.jugador, grupo_balas_enemigas, True)
            for _ in col_balas:
                self.vida_actual -= 10  # daño por bala

        if grupo_asteroides:
            col_asteroides = pygame.sprite.spritecollide(self.jugador, grupo_asteroides, False)
            for _ in col_asteroides:
                self.vida_actual -= 20  # daño por asteroide

        if self.vida_actual < 0:
            self.vida_actual = 0

    def dibujar(self, pantalla):
        x = self.jugador.rect.x
        y = self.jugador.rect.y - self.barra_alto - 5  # 5 píxeles arriba del enemigo
        ancho_total = self.barra_ancho
        alto = self.barra_alto

        # Fondo rojo (vida total)
        pygame.draw.rect(pantalla, (255, 0, 0), (x, y, ancho_total, alto))

        # Vida actual en verde, según proporción de vida
        ancho_vida = int(ancho_total * (self.vida_actual / self.vida_maxima))
        pygame.draw.rect(pantalla, (0, 255, 0), (x, y, ancho_vida, alto))


    def esta_muerto(self):
        return self.vida_actual <= 0

