from unittest import TestCase, skip
from unittest.mock import patch, Mock, call
from src.post_install import post_install


@patch('src.post_install.restaurar_backup')
@patch('src.post_install.print')
@patch('src.post_install.sy')
class TestPostInstallComandosAvulsos(TestCase):
	def setUp(self):
		self.argumentos = Mock()
		self.argumentos.sistema = 'debian'
		self.argumentos.interface = 'i3'
		self.argumentos.usuario = 'none'
		self.comando_git = 'git --git-dir=/home/none/.cfg/ --work-tree=/home/none '

	def test_sy_sendo_chamado_com_comando_snap_install(self, sy, *_):
		post_install(self.argumentos)
		argumento = sy.call_args_list[2].args[0]
		self.assertTrue(argumento.startswith('snap install '))

	def test_sy_sendo_chamado_com_comando_pip_install(self, sy, *_):
		post_install(self.argumentos)
		argumento = sy.call_args_list[3].args[0]
		self.assertTrue(argumento.startswith('pip install '))

	def test_sy_sendo_chamado_com_comando_que_instala_oh_my_zsh(self, sy, *_):
		post_install(self.argumentos)
		sy.assert_has_calls(
			[
				call(
						'sh -c "$(curl -fsSL https://raw.githu'
        				'busercontent.com/robbyrussell'
        				'/oh-my-zsh/master/tools/install.sh)"'
    			),
    			call('chsh -s $(which zsh)'),
    			call(
    					'git clone https://github.com/zsh-users/'
        				'zsh-syntax-highlighting.git'
    			)
			]
		)

	@skip(
		'pulado por enquanto até eu criar um repositório separado para '
		'os meus dotfiles'
	)
	def test_sy_sendo_chamado_com_comando_para_instalar_os_dots_do_repositorio(self, sy, *_):
		post_install(self.argumentos)
		sy.assert_has_calls(
			[
				call('rm .bashrc .zshrc'),
				call(
						'git clone --bare https://github.com/'
						'b166erbot/dotfiles /home/none/.cfg'
				),
				call(self.comando_git + 'checkout'),
				call(self.comando_git + 'config --local status.showUntrackedFiles no')
			]
		)

	def test_sy_sendo_chamado_com_comando_para_instalar_meus_scripts(self, sy, *_):
		post_install(self.argumentos)
		sy.assert_has_calls(
			[
				call('python3 ~/python\ scripts/scripts/setup.py install')
			]
		)


@patch('src.post_install.restaurar_backup')
@patch('src.post_install.print')
@patch('src.post_install.sy')
class TestPostInstallDebian(TestCase):
	def setUp(self):
		self.argumentos = Mock()
		self.argumentos.sistema = 'debian'
		self.argumentos.interface = 'i3'
		self.argumentos.usuario = 'none'
		self.programas_auxiliares = [
			'rofi', 'nitrogen', 'picom', 'lxappearance', 'polybar'
		]

	def test_sy_sendo_chamada_com_comando_atualizar(self, sy, *_):
		post_install(self.argumentos)
		sy.assert_has_calls([call('apt update')])

	def test_sy_sendo_chamado_com_comando_instalar_programas(self, sy, *_):
		post_install(self.argumentos)
		argumento = sy.call_args_list[1].args[0]
		self.assertTrue(argumento.startswith('apt install -y '))

	def test_sy_sendo_chamado_com_comando_para_linkar_coisas(self, sy, *_):
		post_install(self.argumentos)
		sy.assert_has_calls(
			[
				call(
						"ln -s /usr/bin/bpython3 /usr/bin/bpython"
				)
			]
		)

	def test_sy_sendo_chamada_com_comando_para_remover_programas(self, sy, *_):
		post_install(self.argumentos)
		argumento = sy.call_args_list[8].args[0]
		self.assertTrue(argumento.startswith('apt autoremove -y '))

	def test_sy_sendo_chamado_com_comando_autoremove(self, sy, *_):
		post_install(self.argumentos)
		sy.assert_has_calls([call('apt autoremove -y')])

	def test_sy_sendo_chamado_com_comando_para_instalar_interface_i3(self, sy, *_):
		post_install(self.argumentos)
		self.programas_auxiliares.append('i3')
		sy.assert_has_calls(
			[
				call(
						'apt install -y ' + ' '.join(self.programas_auxiliares)
				)
			]
		)

	def test_sy_sendo_chamado_com_comando_para_instalar_interface_bspwm(self, sy, *_):
		self.argumentos.interface = 'bspwm'
		post_install(self.argumentos)
		self.programas_auxiliares.append('bspwm')
		sy.assert_has_calls(
			[
				call(
						'apt install -y ' + ' '.join(self.programas_auxiliares)
				)
			]
		)

	def test_sy_sendo_chamada_com_comando_para_instalar_interface_xfce4(self, sy, *_):
		self.argumentos.interface = 'xfce4'
		post_install(self.argumentos)
		self.programas_auxiliares = ['xfce4', 'xfce4-goodies']
		sy.assert_has_calls(
			[
				call(
						'apt install -y ' + ' '.join(self.programas_auxiliares)
				)
			]
		)


@patch('src.post_install.restaurar_backup')
@patch('src.post_install.print')
@patch('src.post_install.sy')
class TestPostInstallArchLinux(TestCase):
	def setUp(self):
		self.argumentos = Mock()
		self.argumentos.sistema = 'arch-linux'
		self.argumentos.interface = 'i3'
		self.argumentos.usuario = 'none'
		self.programas_auxiliares = [
			'rofi', 'nitrogen', 'picom', 'lxappearance', 'polybar'
		]
	
	def test_sy_sendo_chamada_com_comando_atualizar(self, sy, *_):
		post_install(self.argumentos)
		sy.assert_has_calls([call('pacman -Syy')])

	def test_sy_sendo_chamado_com_comando_instalar_programas(self, sy, *_):
		post_install(self.argumentos)
		argumento = sy.call_args_list[1].args[0]
		self.assertTrue(argumento.startswith('pacman -S '))

	def test_sy_sendo_chamado_com_comando_para_linkar_coisas(self, sy, *_):
		post_install(self.argumentos)
		sy.assert_has_calls(
			[
				call(
						"ln -s /bin/bpython3 /bin/bpython"
				)
			]
		)

	def test_sy_sendo_chamado_com_comando_autoremove(self, sy, *_):
		post_install(self.argumentos)
		sy.assert_has_calls([call('pacman -Qtqd | sudo pacman -Rnsc -')])

	def test_sy_sendo_chamado_com_comando_para_instalar_interface_i3(self, sy, *_):
		post_install(self.argumentos)
		self.programas_auxiliares.append('i3')
		sy.assert_has_calls(
			[
				call(
						'pacman -S ' + ' '.join(self.programas_auxiliares)
				)
			]
		)

	def test_sy_sendo_chamado_com_comando_para_instalar_interface_bspwm(self, sy, *_):
		self.argumentos.interface = 'bspwm'
		post_install(self.argumentos)
		self.programas_auxiliares.append('bspwm')
		sy.assert_has_calls(
			[
				call(
						'pacman -S ' + ' '.join(self.programas_auxiliares)
				)
			]
		)

	def test_sy_sendo_chamada_com_comando_para_instalar_interface_xfce4(self, sy, *_):
		self.argumentos.interface = 'xfce4'
		post_install(self.argumentos)
		self.programas_auxiliares = ['xfce4', 'xfce4-goodies']
		sy.assert_has_calls(
			[
				call(
						'pacman -S ' + ' '.join(self.programas_auxiliares)
				)
			]
		)