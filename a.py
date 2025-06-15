import os
import glob
from urllib.parse import urlparse

from bs4 import BeautifulSoup

html_dir = r'C:\Users\mpguc\Desktop\ids'
files_dir = os.path.join(html_dir, 'files')
output_file = os.path.join(html_dir, 'tabela.html')

players = []
header = []

# Processa todos os arquivos HTML
for file_path in glob.glob(os.path.join(html_dir, '*.html')):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # ID do jogador (vem do nome do arquivo)
    player_id = os.path.basename(file_path).replace('.html', '')

    # Nome do jogador
    name_tag = soup.find('div', class_='col-6 text-right')
    if not name_tag:
        continue
    player_name = name_tag.text.strip()

    # Coleta os itens
    items = soup.find_all('div', class_='collection-container collection-player-container position-relative')
    item_data = {}
    total_red_stars = 0
    total_yellow_stars = 0

    for item in items:
        # Imagem do item
        icon_img = item.find('img', class_='collection-item')
        if not icon_img:
            continue
        icon_src = icon_img['src']
        caminho = urlparse(icon_src).path
        item_name = os.path.basename(caminho)

        img_quality = item.find('img', class_='position-absolute collection-quality-item')
        if img_quality:
            img_quality = img_quality['src']
            rank_q = urlparse(img_quality).path
            rank_img = os.path.basename(rank_q)

        # Contar estrelas
        stars_div = item.find('div', class_='star-container-small')
        stars_imgs = stars_div.find_all('img') if stars_div else []

        stars = []
        has_red_star = False
        max_stars = len(stars_imgs)             
        
        # Primeiro verifica se tem estrelas vermelhas
        for star_img in stars_imgs:
            star_src = star_img['src']
            if 'Star_Enhance.png' in star_src:  # Estrela vermelha
                has_red_star = True
                break
        
        # Se tem estrela vermelha, todas as amarelas estão preenchidas
        if has_red_star and max_stars > 0:
            # Adiciona todas as estrelas amarelas
            #stars.extend(['Star_Normal.png'] * max_stars)
            total_yellow_stars += max_stars
            
            # Adiciona as estrelas vermelhas
            for star_img in stars_imgs:
                star_src = star_img['src']
                if 'Star_Enhance.png' in star_src:
                    stars.append('Star_Enhance.png')
                    total_red_stars += 1
                elif 'Star_Enhance_BG.png' in star_src: 
                    stars.append('Star_Enhance_BG.png')
        else:
            for star_img in stars_imgs:
                star_src = star_img['src']
                if 'Star_Enhance.png' in star_src:  # Estrela vermelha
                    stars.append('Star_Enhance.png')
                    total_red_stars += 1
                elif 'Star_Normal.png' in star_src:  # Estrela amarela
                    stars.append('Star_Normal.png')
                    total_yellow_stars += 1
                elif 'Star_Enhance_BG.png' in star_src:  # Estrela amarela
                    stars.append('Star_Enhance_BG.png')

        item_data[item_name] = stars

        existe = any(d.get('img') == item_name for d in header)
        if not existe:
            header.append({'img': item_name, 'rank_img': rank_img})

    players.append({
        'id': player_id, 
        'name': player_name, 
        'items': item_data,
        'red_stars': total_red_stars,
        'yellow_stars': total_yellow_stars
    })

# Ordenar jogadores por estrelas vermelhas (decrescente) e depois amarelas (decrescente)
players.sort(key=lambda x: (-x['red_stars'], -x['yellow_stars']))

# Criar HTML
html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabela de Jogadores</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }
        
        .table-wrapper {
            width: 100%;
            overflow: hidden;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            background: white;
        }
        
        .table-container {
            overflow-x: auto;
            width: 100%;
            max-height: 99vh;
            position: relative;
        }
        
        table {
            border-collapse: collapse;
            width: max-content;
            min-width: 100%;
            font-size: 14px;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: center;
            vertical-align: middle;
            white-space: nowrap;
        }
        
        thead th {
            background-color: #4a6fa5;
            color: white;
            position: sticky;
            top: 0;
            z-index: 10;
            font-weight: bold;
        }
        
        th.sticky-col, td.sticky-col {
            position: sticky;
            left: 0;
            z-index: 5;
            background-color: #4a6fa5;
            color: white;
        }
        
        th.sticky-name, td.sticky-name {
            position: sticky;
            left: 80px;
            z-index: 5;
            background-color: white;
            color: #333;
        }
        
        th.red-star, td.red-star {
            position: sticky;
            left: 160px;
            z-index: 5;
            background-color: white;
            color: #e63946;
            font-weight: bold;
        }
        
        th.yellow-star, td.yellow-star {
            position: sticky;
            left: 240px;
            z-index: 5;
            background-color: white;
            color: #ffd166;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        tr:hover {
            background-color: #e6f3ff;
        }
        
        .item-container {
            position: relative;
            width: 48px;
            height: 48px;
            margin: 0 auto;
        }
        
        .item-img {
            position: absolute;
            top: 0;
            left: 0;
            width: 48px;
            height: 48px;
            z-index: 2;
        }
        
        .quality-img {
            position: absolute;
            top: 0;
            left: 0;
            width: 48px;
            height: 48px;
            z-index: 1;
        }
        
        .stars-line {
            display: flex;
            justify-content: center;
            gap: 2px;
            margin-top: 5px;
        }
        
        .star-img {
            width: 16px;
            height: 16px;
        }
    </style>
</head>
<body>
    <div class="table-wrapper">
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th class="sticky-col">ID</th>
                        <th class="sticky-name">Nome</th>
                        <th class="red-star">Vermelhas</th>
                        <th class="yellow-star">Amarelas</th>
"""

# Cabeçalho com imagens de itens
for img in header:
    html += f"""<th>
                    <div class="item-container">
                        <img class="quality-img" src="files/{img['rank_img']}">
                        <img class="item-img" src="files/{img['img']}">
                    </div>
                </th>
"""

html += """
                    </tr>
                </thead>
                <tbody>
"""

# Corpo da tabela
for player in players:
    html += f'                    <tr>\n'
    html += f'                        <td class="sticky-col">{player["id"]}</td>\n'
    html += f'                        <td class="sticky-name">{player["name"]}</td>\n'
    html += f'                        <td class="red-star">{player["red_stars"]}</td>\n'
    html += f'                        <td class="yellow-star">{player["yellow_stars"]}</td>\n'
    
    for icon in header:
        if icon['img'] in player['items']:
            stars = player['items'][icon['img']]
            html += f'<td><div class="stars-line">'            
            for s in stars:
                html += f'<img class="star-img" src="files/{s}" alt="star">'
            html += '</div></td>\n'
        else:
            html += '<td></td>\n'
    html += '                    </tr>\n'

html += """
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Tabela gerada: {output_file}")