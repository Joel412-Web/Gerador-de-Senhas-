from cx_Freeze import setup, Executable

# Inclua arquivos adicionais, se necessário
files = []

# Parâmetros de configuração do executável
options = {
    'build_exe': {
        'packages': ['tkinter', 'customtkinter', 'string', 'random'],
        'include_files': files,
    },
}

# Definição do executável
executables = [
    Executable(
        script='Gerador.py',  # Substitua 'seu_script.py' pelo nome do seu arquivo Python
        base='Win32GUI',  # Use 'Win32GUI' para suprimir a janela do console em aplicativos com GUI
        target_name='gerador_de_senhas.exe'  # Nome do executável gerado
    )
]

setup(
    name='Gerador de Senhas',
    version='1.0',
    description='Aplicação para geração de senhas',
    options=options,
    executables=executables
)
