from pathlib import Path
import json
from shutil import copy, copytree
from pwd import getpwnam
import re
from itertools import chain
from argparse import ArgumentParser

try:
    from src.utils import corrigir_caminho, pegar_entrada
except ModuleNotFoundError:
    from utils import corrigir_caminho, pegar_entrada


def remover_arquivos(caminho, extensao, caminhos_remover):
    """Pega o caminho e remove de dentro dele, os quais não foram escolhidos"""
    # a ordem importa, portanto, tem que vir primeiro *.* e depois *
    caminho = Path(str(caminho).replace(extensao, ''))
    arquivos = set(map(
        str, caminho.glob(extensao)
    ))
    if len(caminhos_remover) > 0:
        caminhos_remover = list(
            map(lambda x: str(caminho / x), caminhos_remover)
        )
        arquivos -= set(caminhos_remover)
    return list(arquivos)


def passar_regex(expressao, texto):
    """Passa o regex no texto e retorna os resultados."""
    regex = re.compile(expressao)
    tuplas_de_texto = regex.findall(texto)
    texto_recortado = list(filter(
        lambda texto: bool(texto), chain(*tuplas_de_texto)
    ))
    return texto_recortado


def pegar_caminhos():
    """Pega as entradas do usuário, verifica se existem e as retorna."""
    expressao_regular = '[\"\']([^\"\']+)[\"\']|([^\'\"\s-]+)'
    entradas = []
    while True:
        entrada = input('>>> ')
        if not bool(entrada):
            break
        entrada_recortada = passar_regex(expressao_regular, entrada)
        caminho, _ = corrigir_caminho(entrada_recortada[0])
        if not caminho.exists():
            print('Erro: arquivo ou pasta não existe')
        else:
            entradas.append(entrada)
            if caminho.is_dir():
                print('pasta adicionada')
            elif caminho.is_file():
                print('arquivo adicionado')
    return entradas


def fazer_backup(argumentos):
    print('*' * 5 + ' Aviso ' + '*' * 5)
    print('você precisa ter o pendrive montado primeiro.')
    print(
        'pra montar, basta abrir o gerenciador de arquivos'
        ' e clicar no pendrive.'
    )
    print('verifique também se o pendrive tem espaço para as músicas.\n')
    resposta = pegar_entrada('está pronto?', ['sim', 's', 'não', 'nao', 'n'])
    if resposta.lower() in ['nao', 'não', 'n']:
        exit(1)

    try:
        usuario_final = getpwnam(argumentos.usuario)
    except KeyError:
        print('Erro: usuário não existe.')
        exit(1)
    pasta_home = usuario_final.pw_dir

    if argumentos.config_arquivo == 'novo':
        print('digite abaixo as pastas ou arquivos que deseja copiar:')
        print('usagem:', '~/Downloads/*', '~/*.*', '~/Downloads', sep='\n')
        print('~/Downloads - isos "Telegram Desktop" \'teste teste.mp3\'')
        print(
            'o sinal de "menos" acima serve para remover pastas '
            'para não serem copiadas'
        )
        print('"/home/user/teste teste"')
        print('(para terminar, precione enter com o texto vazio)')
        entradas = pegar_caminhos()
        with open('configuracoes.json', 'w') as configfile:
            json.dump(entradas, configfile, indent=4)
    elif argumentos.config_arquivo == 'carregar':
        if Path('configuracoes.json').exists():
            with open('configuracoes.json') as configfile:
                entradas = json.load(configfile)
        else:
            print(
                'Erro: o arquivo de configuração não '
                'existe. execute novamente o programa '
                'e crie uma nova lista de pastas/arquivos '
                'a serem copiadas(os)'
            )
            exit(1)

    destino_pendrive = argumentos.pendrive / Path('backup')
    if destino_pendrive.exists():
        if destino_pendrive.is_file():
            raise Exception(
                'já existe um arquivo com o nome backup '
                'na pasta do pendrive, favor arrumar.'
            )
        elif destino_pendrive.is_dir():
            raise IsADirectoryError(
                'o diretório backup já existe no pendrive, favor arrumar.'
            )
    else:
        destino_pendrive.mkdir()
    expressao_regular = '[\"\']([^\"\']+)[\"\']|([^\'\"\s-]+)'
    arquivos_ou_pastas = []
    for entrada in entradas:
        entrada_recortada = passar_regex(expressao_regular, entrada)
        caminho, *caminhos_remover = entrada_recortada
        caminho, extensao = corrigir_caminho(caminho)
        # por obrigatoriedade, o '*.*' vem primeiro que o '*' se não dá bug
        if extensao == '*.*':
            arquivos_ou_pastas += remover_arquivos(
                caminho, '*.*', caminhos_remover
            )
        elif extensao == '*':
            arquivos_ou_pastas += remover_arquivos(
                caminho, '*', caminhos_remover
            )
        else:
            if caminho.is_dir() and bool(len(caminhos_remover)):
                arquivos_ou_pastas += remover_arquivos(
                    caminho, '*', caminhos_remover
                )
            else:
                arquivos_ou_pastas.append(str(caminho))

    for item in arquivos_ou_pastas:
        local_destino = Path(item).relative_to(pasta_home)
        caminho_final = destino_pendrive / local_destino
        if not caminho_final.parent.exists():
            caminho_final.parent.mkdir(parents=True)
        if Path(item).is_dir():
            copytree(item, caminho_final)
        else:
            copy(item, caminho_final)
    print('arquivos copiados com sucesso.')


def main():
    descricao = (
        'programa que faz o pre install de uma distro derivada de debian'
    )
    usagem = (
        'python3 pre_install.py --usuario <usuário> --pendrive '
        '<local do pendrive> [--config-arquivo <carregar/novo>]'
    )
    parser = ArgumentParser(
        usage = usagem,
        description = descricao
    )
    parser.add_argument(
        '--usuario', type=str, required = True,
        help = 'nome do usuário logado na máquina no momento'
    )
    parser.add_argument(
        '--pendrive', type=str, required = True,
        help = 'pendrive de destino para fazer o backup'
    )
    parser.add_argument(
        '--config-arquivo', type=str, required = False,
        default = 'novo', choices = ['novo', 'carregar'],
        help = 'arquivo de configuração. opções: novo, carregar'
    )
    argumentos = parser.parse_args()
    fazer_backup(argumentos)


if __name__ == '__main__':
    main()