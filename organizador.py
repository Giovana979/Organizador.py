import os #fornece funções para navegar em pastas, arquivos...
import shutil #biblioteca de alto nível para operações com arquivos
from datetime import datetime #importa a classe datetime para converter os números em datas
from PIL import Image #biblioteca PILLOW importada o módulo Image para abrir o arquivo da imagem
from PIL.ExifTags import TAGS #dicionário TAGS traduz números EXIF em nomes légiveis

origem = "C:\Users\GIHes\Documents\Saved Pictures"
destino = "D:\Backup Photos"

def get_date_taken(path):
    try: 
        #Criando um objeto imagem, carrega os dados da imagem, para conseguir extrair o EXIF
        image = Image.open(path)
        #É o método que entra no cabeçalho da foto e extrai marca do celular, gps, data...
        exif_date = image._getexif()
        #EXIF tem centenas de informações, fazemos um loop para procurar especificamente 
        #a etiqueta "DateTimeOriginal". Se encontrarmos usamos o strptime 
        #para transformar o texto em um objeto de data real do Python
        if exif_date:
            for tag, value in exif_date.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    #Formato EXIF é 'YYYY:MM:DD HH:MM:SS'
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        pass
    #Se não encontrar EXIF, usa a data do sistema como plano B
    return datetime.fromtimestamp(os.path.getmtime(path))

for arquivo in os.listdir(origem):
    if arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        caminho_src = os.path.join(origem, arquivo)

        data = get_date_taken(caminho_src)
        ano = str(data.year)
        mes = data.strftime('%m - %B')

        diretoria_final = os.path.join(destino, ano, mes)
        os.makedirs(diretoria_final, exist_ok=True)

        shutil.copy2(caminho_src, os.path.join(diretoria_final, arquivo))

print("Backup concluído com sucesso!")