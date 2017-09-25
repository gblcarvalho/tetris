import pygame
import random

LARGURA = 500
ALTURA = 672

NUM_QX = 10
NUM_QY = 16

TAM_QX = LARGURA/NUM_QX
TAM_QY = ALTURA/NUM_QY

TAM_BORDA = 2


class Peca:
    def __init__(self):
        n = random.randint(0, 3)
        if n == 0:
            self.peca = [
                [0, 0, 0],
                [0, 1, 0],
                [1, 1, 1]
            ]
            self.cor = (255, 0, 0)
            self.tamanho = 3
            self.largura = 3
        elif n == 1:
            self.peca = [
                [2, 0, 0],
                [2, 2, 0],
                [0, 2, 0]
            ]
            self.cor = (0, 255, 0)
            self.tamanho = 3
            self.largura = 2
        elif n == 2:
            self.peca = [
                [3, 3],
                [3, 3],
            ]
            self.cor = (0, 0, 255)
            self.tamanho = 2
            self.largura = 2
        elif n == 3:
            self.peca = [
                [4, 0, 0, 0],
                [4, 0, 0, 0],
                [4, 0, 0, 0],
                [4, 0, 0, 0],
            ]
            self.cor = (255, 255, 0)
            self.tamanho = 4
            self.largura = 1

        self.pos_x = (NUM_QX - self.largura) // 2
        self.pos_y = self.tamanho * -1

    def desenhar(self, tela):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.peca[i][j] > 0:
                    x = (j + self.pos_x) * TAM_QX + TAM_BORDA
                    y = (i + self.pos_y) * TAM_QY + TAM_BORDA

                    pygame.draw.rect(tela, self.cor, (x, y, TAM_QX - TAM_BORDA, TAM_QY - TAM_BORDA))


class Grade:

    TEMPO_NORMAL = 500
    TEMPO_TURBINADO = TEMPO_NORMAL / 5
    TEMPO_DESCER = TEMPO_NORMAL
    TEMPO_MOVER = TEMPO_NORMAL / 4

    def __init__(self):
        self.grade = []
        self.tick_descer = 0
        self.tick_mover = 0
        self.peca_atual = self.nova_peca()
        for i in range(NUM_QY):
            self.grade.append([-1] * NUM_QX)

        self.direita = False
        self.esquerda = False
        self.turbinar = False

    def nova_peca(self):
        return Peca()

    def pegar_cor(self, numero):
        if numero == 1:
            return (255, 0, 0)

        if numero == 2:
            return (0, 255, 0)

        if numero == 3:
            return (0, 0, 255)

        if numero == 4:
            return (255, 255, 0)

        return (255, 255, 255)

    def colidiu(self):
        if self.peca_atual.pos_y + self.peca_atual.tamanho > NUM_QY:
            return True

        if self.peca_atual.pos_x < 0:
            return True

        if self.peca_atual.pos_x + self.peca_atual.largura > NUM_QX:
            return True

        y = self.peca_atual.pos_y
        x = self.peca_atual.pos_x
        for linha in self.peca_atual.peca:
            for pedaco in linha:
                if pedaco > 0 and y >= 0 and self.grade[y][x] > 0:
                    return True
                x += 1
            x = self.peca_atual.pos_x
            y += 1

        return False

    def adicionar_peca(self):
        x = self.peca_atual.pos_x
        y = self.peca_atual.pos_y

        for linha in self.peca_atual.peca:
            for pedaco in linha:
                if pedaco > 0 and x >= 0:
                    self.grade[y][x] = pedaco
                x += 1
            x = self.peca_atual.pos_x
            y +=1

    def movimentar_peca(self, tick):
        if self.turbinar:
            self.TEMPO_DESCER = self.TEMPO_TURBINADO
        else:
            self.TEMPO_DESCER = self.TEMPO_NORMAL

        self.tick_descer += tick
        self.tick_mover += tick
        if self.tick_descer >= self.TEMPO_DESCER:
            self.peca_atual.pos_y += 1
            self.tick_descer = 0
            if self.colidiu():
                self.peca_atual.pos_y -= 1
                self.adicionar_peca()
                self.peca_atual = self.nova_peca()

        if self.direita and self.tick_mover >= self.TEMPO_MOVER:
            self.peca_atual.pos_x += 1
            self.tick_mover = 0
            if self.colidiu():
                self.peca_atual.pos_x -= 1

        if self.esquerda and self.tick_mover >= self.TEMPO_MOVER:
            self.peca_atual.pos_x -= 1
            self.tick_mover = 0
            if self.colidiu():
                self.peca_atual.pos_x += 1

    def apagar_linha(self):
        for i, linha in enumerate(self.grade):
            if not list(filter(lambda x : x == -1, self.grade[i])):
                del self.grade[i]
                self.grade.insert(0, [-1] * NUM_QX)

    def atualizar(self, tick):
        self.movimentar_peca(tick)
        self.apagar_linha()

    def desenhar(self, tela):
        for i in range(NUM_QY):
            for j in range(NUM_QX):
                x = j * TAM_QX + TAM_BORDA
                y = i * TAM_QY + TAM_BORDA

                cor = self.pegar_cor(self.grade[i][j])
                pygame.draw.rect(tela, cor, (x, y, TAM_QX - TAM_BORDA, TAM_QY - TAM_BORDA))

        self.peca_atual.desenhar(tela)


if __name__ == '__main__':

    pygame.init()

    tela = pygame.display.set_mode([LARGURA + TAM_BORDA, ALTURA + TAM_BORDA])
    pygame.display.set_caption("Super Tetris 2000!")

    relogio = pygame.time.Clock()

    grade = Grade()

    sair = False

    while not sair:

        # CAPTURAR EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    grade.direita = True
                elif evento.key == pygame.K_LEFT:
                    grade.esquerda = True
                elif evento.key == pygame.K_DOWN:
                    grade.turbinar = True
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_RIGHT:
                    grade.direita = False
                elif evento.key == pygame.K_LEFT:
                    grade.esquerda = False
                elif evento.key == pygame.K_DOWN:
                    grade.turbinar = False

        # ATUALIZACAO
        # PEGAR O TEMPO QUE PASSOU DESDE O ULTIMO TICK
        tick = relogio.get_time()

        grade.atualizar(tick)

        # DESENHAR
        tela.fill([0, 0, 0])

        grade.desenhar(tela)

        pygame.display.flip()

        # CONTROLE DE FPS
        relogio.tick(60)