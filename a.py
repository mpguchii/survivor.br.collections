import os
import glob
from urllib.parse import urlparse

from bs4 import BeautifulSoup

html_dir = r'C:\Users\mpguc\Desktop\ids'
files_dir = os.path.join(html_dir, 'files')
output_file = os.path.join(html_dir, 'tabela.html')

players = []
header = []

for file_path in glob.glob(os.path.join(html_dir, '*.html')):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    player_id = os.path.basename(file_path).replace('.html', '')

    name_tag = soup.find('div', class_='col-6 text-right')
    if not name_tag:
        continue
    player_name = name_tag.text.strip()

    items = soup.find_all('div', class_='collection-container collection-player-container position-relative')
    item_data = {}
    total_red_stars = 0
    total_yellow_stars = 0

    total_red_quality_y = 0
    total_yellow_quality_y = 0
    total_event_quality_y = 0
    total_purple_quality_y = 0
    total_blue_quality_y = 0
    total_green_quality_y = 0
    
    total_red_quality_r = 0
    total_yellow_quality_r = 0
    total_event_quality_r = 0
    total_purple_quality_r = 0
    total_blue_quality_r = 0
    total_green_quality_r = 0

    for item in items:
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

        stars_div = item.find('div', class_='star-container-small')
        stars_imgs = stars_div.find_all('img') if stars_div else []

        stars = []
        has_red_star = False
        max_stars = len(stars_imgs)             
        
           
        for star_img in stars_imgs:
            star_src = star_img['src']
            if 'Star_Enhance.png' in star_src:
                has_red_star = True
                break
        
        currentRedStars = 0
        currentYellowStars = 0
        
        if has_red_star and max_stars > 0:
            currentYellowStars += max_stars
            
            for star_img in stars_imgs:
                star_src = star_img['src']
                if 'Star_Enhance.png' in star_src:
                    stars.append('Star_Enhance.png')
                    currentRedStars += 1
                elif 'Star_Enhance_BG.png' in star_src: 
                    stars.append('Star_Enhance_BG.png')
        else:
            for star_img in stars_imgs:
                star_src = star_img['src']
                if 'Star_Enhance.png' in star_src:
                    stars.append('Star_Enhance.png')
                    currentRedStars += 1
                elif 'Star_Normal.png' in star_src: 
                    stars.append('Star_Normal.png')
                    currentYellowStars += 1
                elif 'Star_Enhance_BG.png' in star_src: 
                    stars.append('Star_Enhance_BG.png')

        total_yellow_stars += currentYellowStars 
        total_red_stars += currentRedStars

        if "CollectionQuality_11" in img_quality:
          total_red_quality_r += currentRedStars
          total_red_quality_y += currentYellowStars
        elif "CollectionQuality_7" in img_quality and max_stars > 3: 
          total_yellow_quality_r += currentRedStars
          total_yellow_quality_y += currentYellowStars
        elif "CollectionQuality_7" in img_quality: 
          total_event_quality_r += currentRedStars
          total_event_quality_y += currentYellowStars
        elif "CollectionQuality_4" in img_quality: 
          total_purple_quality_r += currentRedStars
          total_purple_quality_y += currentYellowStars
        elif "CollectionQuality_3" in img_quality: 
          total_blue_quality_r += currentRedStars
          total_blue_quality_y += currentYellowStars
        elif "CollectionQuality_2" in img_quality: 
          total_green_quality_r += currentRedStars
          total_green_quality_y += currentYellowStars

        item_data[item_name] = stars

        existe = any(d.get('img') == item_name for d in header)
        if not existe:
            header.append({'img': item_name, 'rank_img': rank_img})

    players.append({
        'id': player_id, 
        'name': player_name, 
        'items': item_data,
        'red_stars': total_red_stars,
        'yellow_stars': total_yellow_stars,
        'total_red_quality_y' : total_red_quality_y,
        'total_yellow_quality_y' : total_yellow_quality_y,
        'total_event_quality_y'  : total_event_quality_y,
        'total_purple_quality_y' : total_purple_quality_y,
        'total_blue_quality_y' : total_blue_quality_y,
        'total_green_quality_y' : total_green_quality_y, 
        'total_red_quality_r'  : total_red_quality_r,
        'total_yellow_quality_r' : total_yellow_quality_r,
        'total_event_quality_r'  : total_event_quality_r,
        'total_purple_quality_r' : total_purple_quality_r,
        'total_blue_quality_r' : total_blue_quality_r,
        'total_green_quality_r' : total_green_quality_r,
    })

players.sort(key=lambda x: (
    -x['total_red_quality_r'], 
    -x['total_red_quality_y'], 
    -x['total_yellow_quality_r'], 
    -x['total_yellow_quality_y'],
    -x['total_event_quality_r'], 
    -x['total_event_quality_y'],
    -x['total_purple_quality_r'], 
    -x['total_purple_quality_y'],
    -x['total_blue_quality_r'], 
    -x['total_blue_quality_y'],
    -x['total_green_quality_r'], 
    -x['total_green_quality_y'],
    ))

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
                        <th class="red-star">Total Vermelhas</th>
                        <th class="yellow-star">Total Amarelas</th>
                        <th >Vermelhos</th>
                        <th >Amerelos</th>
                        <th >Evento</th>
                        <th >Roxo</th>
                        <th >Azul</th>
                        <th >Verde</th>
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


        # 'total_red_quality_y' : total_red_quality_y,
        # 'total_yellow_quality_y' : total_yellow_quality_y,
        # 'total_event_quality_y'  : total_event_quality_y,
        # 'total_purple_quality_y' : total_purple_quality_y,
        # 'total_blue_quality_y' : total_blue_quality_y,
        # 'total_green_quality_y' : total_green_quality_y, 
        # 'total_red_quality_r'  : total_red_quality_r,
        # 'total_yellow_quality_r' : total_yellow_quality_r,
        # 'total_event_quality_r'  : total_event_quality_r,
        # 'total_purple_quality_r' : total_purple_quality_r,
        # 'total_blue_quality_r' : total_blue_quality_r,
        # 'total_green_quality_r' : total_green_quality_r,

# Corpo da tabela
for player in players:
    html += f'                    <tr>\n'
    html += f'                        <td class="sticky-col">{player["id"]}</td>\n'
    html += f'                        <td class="sticky-name">{player["name"]}</td>\n'
    html += f'                        <td class="red-star">{player["red_stars"]}</td>\n'
    html += f'                        <td class="yellow-star">{player["yellow_stars"]}</td>\n'
    html += f'                        <td ><p class="red-star"> V = {player["total_red_quality_r"]} </p>  <p class="yellow-star"> A = {player["total_red_quality_y"]} </p> </td>\n'
    html += f'                        <td ><p class="red-star"> V = {player["total_yellow_quality_r"]} </p>  <p class="yellow-star"> A = {player["total_yellow_quality_y"]} </p> </td>\n'
    html += f'                        <td ><p class="red-star"> V = {player["total_event_quality_r"]} </p>  <p class="yellow-star"> A = {player["total_event_quality_y"]} </p> </td>\n'
    html += f'                        <td ><p class="red-star"> V = {player["total_purple_quality_r"]} </p>  <p class="yellow-star"> A = {player["total_purple_quality_y"]} </p> </td>\n'
    html += f'                        <td ><p class="red-star"> V = {player["total_blue_quality_r"]} </p>  <p class="yellow-star"> A = {player["total_blue_quality_y"]} </p> </td>\n'
    html += f'                        <td ><p class="red-star"> V = {player["total_green_quality_r"]} </p>  <p class="yellow-star"> A = {player["total_green_quality_y"]} </p> </td>\n'
    
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