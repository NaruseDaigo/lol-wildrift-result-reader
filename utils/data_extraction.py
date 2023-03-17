"""
このファイルでは、OCRで取得したテキストデータから戦績情報を抽出する関数を定義します。
extract_stats(text): テキストデータを受け取り、戦績情報を抽出し、データ構造（辞書やオブジェクト）に変換する関数。
"""
import re

from utils.image_processing import extract_victory_or_lose, split_players, split_teams
from utils.ocr import ocr_segment, ocr_num_segment

def parse_kda_txt(kda_text):
    """
    OCRの結果からKill数、Death数、Assist数、獲得した金額を抽出する
    """

    # 正規表現を使用して各数値を検索
    pattern = r'\D*(\d+)\D*(\d+)\D*(\d+)\D*'
    match = re.search(pattern, kda_text)
    if match:
        kills = int(match.group(1))
        deaths = int(match.group(2))
        assists = int(match.group(3))
    else:
        # マッチしなかった場合、デフォルト値を設定
        kills = -1
        deaths = -1
        assists = -1

    return kills, deaths, assists

def extract_match_info(image, return_segmented_image=False):
    victory_or_lose = extract_victory_or_lose(image)
    left_team_image, right_team_image = split_teams(image)
    left_team_player_images = split_players(left_team_image)
    right_team_player_images = split_players(right_team_image)
    left_team_info = [extract_player_info(player_image, 'left') for player_image in left_team_player_images]
    right_team_info = [extract_player_info(player_image, 'right') for player_image in right_team_player_images]

    match_info = {
        'victory_or_lose': victory_or_lose,
        'left_team': left_team_info,
        'right_team': right_team_info
    }

    # セグメントされた画像を適切に設定してください。
    # segmented_images = left_team_player_images
    segmented_images = \
        [extract_player_info(player_image, 'right', return_segmented_image=True)[1] for player_image in right_team_player_images]

    if return_segmented_image:
        return match_info, segmented_images
    else:
        return match_info



def extract_player_info(player_image, side, return_segmented_image=False):
    """
    各プレイヤー情報ブロックから、プレイヤー名、Kill数、Death数、Assist数、獲得した金額などの情報を抽出する。
    """
    height, width = player_image.shape[:2]

    if side == 'left':
        # プレイヤー名のセグメントを抽出
        player_name_image = player_image[:int(height/2), int(275+126):int(275+126+248)]
        # Kill数、Death数、Assist数、獲得した金額のセグメントを抽出
        kda_image = player_image[:int(height/2), int(275+126+248+37):int(275+126+248+37+211)]
        gold_image = player_image[:int(height/2), int(275+126+248+37+211):int(275+126+248+37+341)]
    else: 
        player_name_image = player_image[:int(height/2), int(109+126+5):int(109+126+5+248)]
        kda_image = player_image[:int(height/2), int(109+126+5+248+37):int(109+126+5+248+37+211)]
        gold_image = player_image[:int(height/2), int(109+126+5+248+37+211):int(109+126+5+248+37+341)]

    player_name = ocr_segment(player_name_image)
    kda_txt = ocr_num_segment(kda_image)
    gold_txt = ocr_num_segment(gold_image)

    kills, deaths, assists = parse_kda_txt(kda_txt)
    gold = int(gold_txt.replace(',', ''))

    # 戦績に応じた称号のアイコンはOCRで読み取るのが難しいため、スキップします。

    # スペルのイラストもOCRで読み取るのが難しいため、スキップします。

    # アイテムのイラストもOCRで読み取るのが難しいため、スキップします。

    # 称号を獲得していたらそのイラストが表示されている部分もOCRで読み取るのが難しいため、スキップします。

    player_info = {
        'player_name': player_name,
        'kills': kills,
        'deaths': deaths,
        'assists': assists,
        'gold': gold
    }
    

    if return_segmented_image:
        return player_info, gold_image
    else:
        return player_info