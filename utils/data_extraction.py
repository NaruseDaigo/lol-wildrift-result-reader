"""
このファイルでは、OCRで取得したテキストデータから戦績情報を抽出する関数を定義します。
extract_stats(text): テキストデータを受け取り、戦績情報を抽出し、データ構造（辞書やオブジェクト）に変換する関数。
"""
import re

from utils.image_processing import segment_image, save_all_segments
from utils.ocr import ocr_segment, ocr_num_segment, ocr_result_segment

# ロギング
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s:%(name)s - %(message)s")
file_handler = logging.FileHandler('/Users/daigo/workspace/lol-wildrift-stats/logs/app.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

def extract_match_info(image, return_segmented_images=False):
    logger.debug("extract_match_info()関数が実行されました。")
    # 画像分割
    segmented_images = segment_image(image)
    save_all_segments(segmented_images)
    logger.debug("画像分割が完了しました。")
    # save_all_segments(segmented_images)
    # OCR
    result_info = ocr_result_segment(segmented_images['result'])
    print('-----------------')
    print(result_info)
    print('-----------------')
    logger.debug("勝敗抽出が完了しました。")
    left_team_info = [extract_player_info(player_image, 'left') for player_image in segmented_images["left_team_players"]]
    right_team_info = [extract_player_info(player_image, 'right') for player_image in segmented_images["right_team_players"]]
    logger.debug("全抽出が完了しました。")

    match_info = {
        'result': result_info,
        'left_team': left_team_info,
        'right_team': right_team_info
    }

    if return_segmented_images:
        return match_info, segmented_images
    else:
        return match_info



def extract_player_info(player_image, side):
    """
    各プレイヤー情報ブロックから、プレイヤー名、Kill数、Death数、Assist数、獲得した金額などの情報を抽出する。
    """
    height, width = player_image.shape[:2]

    if side == 'left':
        # プレイヤー名のセグメントを抽出
        player_name_image = player_image[:int(height/2), int(401):int(401+248)]
        # Kill数、Death数、Assist数、獲得した金額のセグメントを抽出
        kda_image = player_image[:int(height/2), int(686):int(686+200)]
        gold_image = player_image[:int(height/2), int(886):int(897+141)]
    elif side == 'right':
        player_name_image = player_image[:int(height/2), int(240):int(240+248)]
        kda_image = player_image[:int(height/2), int(525):int(525+200)]
        gold_image = player_image[:int(height/2), int(725):int(725+141)]

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

    return player_info        

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