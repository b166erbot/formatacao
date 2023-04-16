from unittest import TestCase
from unittest.mock import patch
from src.fazer_backup import passar_regex, pegar_caminhos


class TestPassarRegex(TestCase):
    expressao = '[\"\']([^\"\']+)[\"\']|([^\'\"\s-]+)'
    
    def test_texto_1(self):
        texto = '~/Downloads/ - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste.py\''
        resultado = passar_regex(self.expressao, texto)
        esperado = [
            '~/Downloads/', 'teste', 'teste.py', 'teste.mp3',
            'teste teste', 'teste teste.mp3', 'teste teste.py'
        ]
        self.assertEqual(resultado, esperado)
    
    def test_texto_2(self):
        texto = '/home/none/Downloads - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\''
        resultado = passar_regex(self.expressao, texto)
        esperado = [
            '/home/none/Downloads', 'teste', 'teste.py',
            'teste.mp3', 'teste teste', 'teste teste.mp3',
            'teste teste'
        ]
        self.assertEqual(resultado, esperado)
    
    def teste_texto_3(self):
        texto = '"/home/none/teste teste" - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\''
        resultado = passar_regex(self.expressao, texto)
        esperado = [
            '/home/none/teste teste', 'teste', 'teste.py',
            'teste.mp3', 'teste teste', 'teste teste.mp3',
            'teste teste'
        ]
        self.assertEqual(resultado, esperado)
    
    def teste_texto_4(self):
        texto = '~/Downloads/* - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\''
        resultado = passar_regex(self.expressao, texto)
        esperado = [
            '~/Downloads/*', 'teste', 'teste.py', 'teste.mp3',
            'teste teste', 'teste teste.mp3', 'teste teste'
        ]
        self.assertEqual(resultado, esperado)
    
    def teste_texto_5(self):
        texto = '~/Downloads/. - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\''
        resultado = passar_regex(self.expressao, texto)
        esperado = [
            '~/Downloads/.', 'teste', 'teste.py', 'teste.mp3',
            'teste teste', 'teste teste.mp3', 'teste teste'
        ]
        self.assertEqual(resultado, esperado)
    
    def teste_texto_6(self):
        texto = '\'/home/none/teste teste\' - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\''
        resultado = passar_regex(self.expressao, texto)
        esperado = [
            '/home/none/teste teste', 'teste', 'teste.py',
            'teste.mp3', 'teste teste', 'teste teste.mp3',
            'teste teste'
        ]
        self.assertEqual(resultado, esperado)
    
    def teste_texto_6(self):
        texto = '"~/Downloads/teste teste/." -teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\''
        resultado = passar_regex(self.expressao, texto)
        esperado = [
            '~/Downloads/teste teste/.', 'teste', 'teste.py',
            'teste.mp3', 'teste teste', 'teste teste.mp3',
            'teste teste'
        ]
        self.assertEqual(resultado, esperado)
    
    def teste_texto_7(self):
        texto = '~/Downloads/*'
        resultado = passar_regex(self.expressao, texto)
        esperado = ['~/Downloads/*']
        self.assertEqual(resultado, esperado)
    
    def teste_texto_8(self):
        texto = '~/Downloads/*.*'
        resultado = passar_regex(self.expressao, texto)
        esperado = ['~/Downloads/*.*']
        self.assertEqual(resultado, esperado)
    
    def teste_texto_9(self):
        texto = '~/Downloads'
        resultado = passar_regex(self.expressao, texto)
        esperado = ['~/Downloads']
        self.assertEqual(resultado, esperado)
    
    def teste_texto_10(self):
        texto = '/home/none/*'
        resultado = passar_regex(self.expressao, texto)
        esperado = ['/home/none/*']
        self.assertEqual(resultado, esperado)
    
    def teste_texto_11(self):
        texto = '/home/none/*.*'
        resultado = passar_regex(self.expressao, texto)
        esperado = ['/home/none/*.*']
        self.assertEqual(resultado, esperado)

    def teste_texto_12(self):
        texto = '/home/none'
        resultado = passar_regex(self.expressao, texto)
        esperado = ['/home/none']
        self.assertEqual(resultado, esperado)


@patch('src.fazer_backup.print')
class TestPegarCaminhos(TestCase):
    @patch('src.fazer_backup.input')
    @patch('src.fazer_backup.Path.exists', return_value = True)
    def test_retornando_as_exatas_pastas_caso_elas_existam(self, print, input, exists):
        side_eff = [
            '~/Downloads/ - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste.py\'',
            '/home/none/Downloads - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '"/home/none/python scripts" - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '~/Downloads/* - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '~/Downloads/. - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '\'/home/none/python scripts\' - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '"~/python scripts/." - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '~/Downloads/*',
            '~/Downloads/*.*',
            '~/Downloads',
            '/home/none/*',
            '/home/none/*.*',
            '/home/none',
            ''
        ]
        input.side_effect = side_eff
        esperado = [
            '~/Downloads/ - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste.py\'',
            '/home/none/Downloads - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '"/home/none/python scripts" - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '~/Downloads/* - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '~/Downloads/. - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '\'/home/none/python scripts\' - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '"~/python scripts/." - teste teste.py teste.mp3 "teste teste" "teste teste.mp3" \'teste teste\'',
            '~/Downloads/*',
            '~/Downloads/*.*',
            '~/Downloads',
            '/home/none/*',
            '/home/none/*.*',
            '/home/none'
        ]
        resultado = pegar_caminhos()
        self.assertEqual(resultado, esperado)

    @patch('src.fazer_backup.input')
    @patch('src.fazer_backup.Path.exists', return_value = False)
    def test_nao_retornando_as_pastas_caso_elas_nao_existam(self, print, input, exists):
        side_eff = [
            'esta pasta não existe',
            'nem esta',
            '/home/none/não existe',
            ''
        ]
        input.side_effect = side_eff
        esperado = []
        resultado = pegar_caminhos()
        self.assertEqual(resultado, esperado)
