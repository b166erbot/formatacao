from unittest import TestCase
from src.utils import corrigir_caminho
from pathlib import Path


class TestCorrigirCaminho(TestCase):
    def test_expandindo_o_usuario(self):
        texto = '~/Downloads/*.*'
        resultado = corrigir_caminho(texto)
        esperado = (Path('~/Downloads').expanduser(), '*.*')
        self.assertEqual(resultado, esperado)

    def test_separando_a_extensao_do_caminho_asterisco_ponto_asterisco(self):
        texto = '~/Downloads/*.*'
        resultado = corrigir_caminho(texto)
        esperado = ('*.*')
        self.assertEqual(resultado[1], esperado)
    
    def test_separando_a_extensao_do_caminho_asterisco(self):
        texto = '~/Downloads/*'
        resultado = corrigir_caminho(texto)
        esperado = ('*')
        self.assertEqual(resultado[1], esperado)
    
    def test_caminho_sem_extensao_retornando_extensao_vazia(self):
        texto = '~/Downloads'
        resultado = corrigir_caminho(texto)
        esperado = (Path('~/Downloads').expanduser(), '')
        self.assertEqual(resultado, esperado)
    
    def test_caminho_completo_com_extensao_retornando_caminho_e_extensao_asterisco_ponto_asterisco(self):
        texto = '/home/none/*.*'
        resultado = corrigir_caminho(texto)
        esperado = (Path('/home/none'), '*.*')
        self.assertEqual(resultado, esperado)
    
    def test_caminho_explicito_com_extensao_retornando_caminho_e_extensao_asterisco(self):
        texto = '/home/none/*'
        resultado = corrigir_caminho(texto)
        esperado = (Path('/home/none'), '*')
        self.assertEqual(resultado, esperado)
    
    def test_caminho_explicito_sem_extensao_retornando_caminho_e_sem_extensao(self):
        texto = '/home/none'
        resultado = corrigir_caminho(texto)
        esperado = (Path('/home/none'), '')
        self.assertEqual(resultado, esperado)