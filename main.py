#pip install git+https://github.com/openai/whisper.git 
# Requisito: FFmpeg previamente instalado (configure o path nas variáveis de ambiente)
import os
import whisper
import hashlib
import warnings
from typing import List, Dict, Any

warnings.filterwarnings("ignore")

def transcreve(path_midia: str) -> Dict[str, Any]:
    """
    Transcreve o conteúdo de um arquivo de mídia.

    Args:
        path_midia (str): Caminho para o arquivo de mídia.

    Returns:
        Dict[str, Any]: Resultado da transcrição.
    """
    modelo = whisper.load_model("medium")
    transcricao = modelo.transcribe(path_midia)
    return transcricao

def traduz(path_midia: str) -> Dict[str, Any]:
    """
    Traduz o conteúdo de um arquivo de mídia para o inglês.

    Args:
        path_midia (str): Caminho para o arquivo de mídia.

    Returns:
        Dict[str, Any]: Resultado da tradução.
    """
    modelo = whisper.load_model("medium")
    traducao = modelo.transcribe(path_midia, language="en", task="translate")
    return traducao

def formata_resposta(resultado: Dict[str, Any]) -> str:
    """
    Formata o resultado da transcrição ou tradução para um formato legível.

    Args:
        resultado (Dict[str, Any]): Resultado da transcrição ou tradução.

    Returns:
        str: Resultado formatado.
    """
    resposta_formatada = ''
    for trecho in resultado['segments']:
        start = str(round(trecho['start'], 2))
        end = str(round(trecho['end'], 2))
        text = trecho['text']
        resposta_formatada += f'[{start} - {end}]\t{text}\n'
    return resposta_formatada

def extrai_hash(path_midia: str, BLOCK_SIZE: int = 65536) -> str:
    """
    Calcula o hash SHA-256 de um arquivo.

    Args:
        path_midia (str): Caminho para o arquivo de mídia.
        BLOCK_SIZE (int, optional): Tamanho do bloco de leitura. Defaults to 65536.

    Returns:
        str: Hash SHA-256 do arquivo.
    """
    file_hash = hashlib.sha256()
    with open(path_midia, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()

def lista_arquivos(pasta: str, extensoes: tuple = ('mp4', 'opus')) -> List[str]:
    """
    Lista os arquivos de mídia em uma pasta com as extensões especificadas.

    Args:
        pasta (str): Caminho para a pasta.
        extensoes (tuple, optional): Extensões de arquivos a serem listados. Defaults to ('mp4', 'opus').

    Returns:
        List[str]: Lista de caminhos para os arquivos de mídia.
    """
    path_arquivos = []
    for dirpath, dirname, filename in os.walk(pasta):
        for f in filename:
            if f.endswith(extensoes):
                path_arquivos.append(os.path.join(dirpath, f))
    return path_arquivos

def separa_nome_arquivo(caminho_do_arquivo: str) -> str:
    """
    Extrai o nome do arquivo a partir do caminho completo.

    Args:
        caminho_do_arquivo (str): Caminho completo do arquivo.

    Returns:
        str: Nome do arquivo.
    """
    separador = '\\' # '/' (para MacOS e Linux)
    if separador in caminho_do_arquivo:
        return caminho_do_arquivo.split(separador)[-1]
    else:
        return ''

def main(pasta: str, arquivo_texto: str) -> None:
    """
    Processa os arquivos de mídia em uma pasta e gera um arquivo de saída com as transcrições.

    Args:
        pasta (str): Caminho para a pasta contendo os arquivos de mídia.
        arquivo_texto (str): Caminho para o arquivo de texto contendo as referências aos arquivos de mídia.
    """
    arquivos_de_midia = lista_arquivos(pasta)
    arquivos_e_nomes = [(separa_nome_arquivo(x), x) for x in arquivos_de_midia]
    texto_final = []
    arquivo_de_saida = "output.txt"

    with open(arquivo_texto, 'r') as arquivo:
        linha = arquivo.readline()
        while linha:
            texto_final.append(linha)
            for elemento in arquivos_e_nomes:
                if elemento[0] in linha:
                    texto_final.append(f"Transcrição automática do arquivo {elemento[0]}")
                    print(f"Transcrevendo o arquivo {elemento[0]}. Aguarde...")
                    texto_final.append(f"Hash do arquivo (sha256): {extrai_hash(elemento[1])}")
                    texto_final.append(formata_resposta(transcreve(elemento[1])))
                    #texto_final.append(formata_resposta(traduz(elemento[1])))
            linha = arquivo.readline()

    with open(arquivo_de_saida, 'w') as arquivo:
        for trecho in texto_final:
            arquivo.write(trecho + '\n')

if __name__ == '__main__':
    pasta = r'C:\Users\jepim\Downloads\WhatsApp Chat - +55 19 99803-XXXX'
    arquivo_texto = r'C:\Users\jepim\\Downloads\WhatsApp Chat - +55 19 99803-XXXX\_chat.txt'
    print('Iniciando a leitura dos arquivos.')
    main(pasta, arquivo_texto)