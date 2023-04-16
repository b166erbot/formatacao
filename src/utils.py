from pathlib import Path


def pegar_entrada(texto, opcoes):
    resposta = ''
    while resposta not in opcoes:
        print(texto)
        resposta = input('>>> ')
    return resposta


def corrigir_caminho(caminho):
    if caminho.endswith('*.*'):
        caminho = caminho[:-3]
        extensao = '*.*'
    elif caminho.endswith('*'):
        caminho = caminho[:-1]
        extensao = '*'
    else:
        extensao = ''
    if caminho.startswith('~'):
        caminho = Path(caminho).expanduser()
    else:
        caminho = Path(caminho)
    return caminho, extensao