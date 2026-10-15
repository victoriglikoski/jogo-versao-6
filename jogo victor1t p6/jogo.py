
from pyscript import document, when
from random import randint
import asyncio


# ELEMENTOS DA TELA
jogador = document.querySelector("#jogador")
moeda = document.querySelector("#moeda")
inimigo = document.querySelector("#inimigo")

placar = document.querySelector("#placar")
vidas_tela = document.querySelector("#vidas")
tempo_tela = document.querySelector("#tempo")
mensagem = document.querySelector("#mensagem")


# ESTADO DO JOGO
game_over = False


# JOGADOR
x = 100
y = 100
velocidade = 10


def atualizar_jogador():
    jogador.style.left = f"{x}px"
    jogador.style.top = f"{y}px"


# MOEDAS E PONTUAÇÃO
moeda_x = 300
moeda_y = 200
pontos = 0


def mover_moeda():
    global moeda_x, moeda_y

    moeda_x = randint(20, 650)
    moeda_y = randint(20, 410)

    moeda.style.left = f"{moeda_x}px"
    moeda.style.top = f"{moeda_y}px"


def verificar_moeda():
    global pontos

    if game_over:
        return

    distancia_x = abs(x - moeda_x)
    distancia_y = abs(y - moeda_y)

    if distancia_x < 40 and distancia_y < 40:
        pontos += 1
        placar.innerText = str(pontos)

        mensagem.innerText = "🪙 Moeda coletada! +1 ponto!"

        mover_moeda()


# SISTEMA DE VIDAS
vidas = 3
pode_perder_vida = True


def atualizar_vidas():
    vidas_tela.innerText = str(vidas)


async def liberar_vida():
    global pode_perder_vida

    await asyncio.sleep(1)

    pode_perder_vida = True


def perder_vida():
    global vidas, pode_perder_vida, game_over
    global x, y

    if not pode_perder_vida or game_over:
        return

    vidas -= 1
    pode_perder_vida = False

    atualizar_vidas()

    if vidas <= 0:
        game_over = True
        mensagem.innerText = (
            f"💀 GAME OVER! Pontuação final: {pontos}"
        )
    else:
        mensagem.innerText = "💥 Você perdeu uma vida!"

        # Retorna o jogador à posição inicial.
        x = 100
        y = 100
        atualizar_jogador()

        # Aguarda antes de permitir perder outra vida.
        asyncio.create_task(liberar_vida())


# INIMIGO
inimigo_x = 500
inimigo_y = 200
velocidade_inimigo = 5


def verificar_colisao():
    distancia_x = abs(x - inimigo_x)
    distancia_y = abs(y - inimigo_y)

    if distancia_x < 40 and distancia_y < 40:
        perder_vida()


def mover_inimigo():
    global inimigo_x

    inimigo_x -= velocidade_inimigo

    if inimigo_x < 0:
        inimigo_x = 650

    inimigo.style.left = f"{inimigo_x}px"
    inimigo.style.top = f"{inimigo_y}px"

    verificar_colisao()


# CONTROLES DO JOGADOR
@when("keydown", "body")
def tecla_pressionada(evento):
    global x, y

    if game_over:
        return

    if evento.key == "ArrowRight":
        x += velocidade

    elif evento.key == "ArrowLeft":
        x -= velocidade

    elif evento.key == "ArrowDown":
        y += velocidade

    elif evento.key == "ArrowUp":
        y -= velocidade

    else:
        return

    # Mantém o jogador dentro do cenário.
    x = max(0, min(x, 650))
    y = max(0, min(y, 410))

    atualizar_jogador()
    verificar_moeda()
    verificar_colisao()


# CRONÔMETRO
tempo = 60


async def contar_tempo():
    global tempo, game_over

    while tempo > 0 and not game_over:
        await asyncio.sleep(1)

        # Não altera o tempo se a partida já terminou.
        if game_over:
            return

        tempo -= 1
        tempo_tela.innerText = str(tempo)

    if tempo <= 0 and not game_over:
        game_over = True
        mensagem.innerText = (
            f"⏰ TEMPO ESGOTADO! Pontuação final: {pontos}"
        )


# CICLO AUTOMÁTICO DO INIMIGO
async def ciclo_inimigo():
    while True:
        if not game_over:
            mover_inimigo()

        await asyncio.sleep(0.03)


# INICIALIZAÇÃO DO JOGO
atualizar_jogador()
atualizar_vidas()
mover_moeda()

inimigo.style.left = f"{inimigo_x}px"
inimigo.style.top = f"{inimigo_y}px"

asyncio.create_task(ciclo_inimigo())
asyncio.create_task(contar_tempo())