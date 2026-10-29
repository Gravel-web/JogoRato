import random
from pathlib import Path

import pygame


LARGURA = 800
ALTURA = 600
TAMANHO_SPRITE = 56
VELOCIDADE = 260
FPS = 60

PASTA = Path(__file__).resolve().parent
PASTA_SPRITES = PASTA / "sprites"
COR_FUNDO = (234, 245, 220)
COR_TEXTO = (45, 70, 42)


def carregar_sprite(nome: str) -> pygame.Surface:
    caminho = PASTA_SPRITES / nome
    imagem = pygame.image.load(str(caminho)).convert_alpha()
    return pygame.transform.smoothscale(imagem, (TAMANHO_SPRITE, TAMANHO_SPRITE))


def nova_posicao_queijo(
    tamanho: tuple[int, int], rato: pygame.Rect
) -> pygame.Rect:
    largura, altura = tamanho
    while True:
        x = random.randint(0, LARGURA - largura)
        y = random.randint(0, ALTURA - altura)
        queijo = pygame.Rect(x, y, largura, altura)
        if not queijo.colliderect(rato):
            return queijo


def mover_rato(
    rato: pygame.Rect, direcao: pygame.Vector2, segundos: float
) -> None:
    movimento = direcao * VELOCIDADE * segundos
    rato.x += round(movimento.x)
    rato.y += round(movimento.y)
    rato.clamp_ip(pygame.Rect(0, 0, LARGURA, ALTURA))


def main() -> None:
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Rato em busca do queijo")
    relogio = pygame.time.Clock()
    fonte = pygame.font.Font(None, 36)

    imagem_rato = carregar_sprite("rato.png")
    imagem_queijo = carregar_sprite("queijo.png")
    rato = pygame.Rect(
        (LARGURA - TAMANHO_SPRITE) // 2,
        (ALTURA - TAMANHO_SPRITE) // 2,
        TAMANHO_SPRITE,
        TAMANHO_SPRITE,
    )
    queijo = nova_posicao_queijo(imagem_queijo.get_size(), rato)
    pontos = 0
    executando = True

    while executando:
        segundos = relogio.tick(FPS) / 1000
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        teclas = pygame.key.get_pressed()
        direcao = pygame.Vector2(
            teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT],
            teclas[pygame.K_DOWN] - teclas[pygame.K_UP],
        )
        if direcao.length_squared() > 0:
            direcao = direcao.normalize()
        mover_rato(rato, direcao, segundos)

        if rato.colliderect(queijo):
            pontos += 1
            queijo = nova_posicao_queijo(imagem_queijo.get_size(), rato)

        tela.fill(COR_FUNDO)
        tela.blit(imagem_rato, rato)
        tela.blit(imagem_queijo, queijo)
        texto = fonte.render(f"Queijos: {pontos}", True, COR_TEXTO)
        tela.blit(texto, (16, 16))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
