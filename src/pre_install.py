from os import getuid
from src.fazer_backup import main


def root() -> bool:
    return getuid() == 0


def pre_install():
    if root():
        print('o pre_install seria melhor executado com o usuário comum')
        exit(1)

    main()
    print('agora, alguns lembretes:')
    print('fazer backup dos arquivos da mãe!')
