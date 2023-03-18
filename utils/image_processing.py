"""
このファイルでは、画像処理関連の関数を定義します。
preprocess_image(image): 画像を受け取り、OCRに適した形式に前処理する関数。
segment_image(image): 画像を受け取り、戦績データのセグメントに分割する関数。
"""
import cv2
import os
from utils.ocr import ocr_segment

def enhance_image(segment):
    # BGR形式からHSV形式に変換
    hsv = cv2.cvtColor(segment, cv2.COLOR_BGR2HSV)

    # HSV空間での閾値設定
    lower_bound = (0, 0, 0)
    upper_bound = (180, 255, 100)

    # 閾値に基づいて画像をマスク
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # 元の画像にマスクを適用してコントラストを強調
    enhanced_segment = cv2.bitwise_and(segment, segment, mask=mask)

    return enhanced_segment

def preprocess_image(image_path):
    # 画像を読み込む
    image = cv2.imread(image_path)

    # グレースケールに変換(経験的にもっとも精度が高い)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二値化 (適応的閾値処理を使用)
    # binary_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    return gray_image

def segment_image(image, horizontal_padding=50, vertical_padding=50):
    # # 輪郭を検出
    # とりあえず領域はハードコーディング for 'iPhone 12 mini' at 2023/03/18
    # contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # segments = []
    # for contour in contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     # 各輪郭の周囲にパディングを追加
    #     x1 = max(0, x - horizontal_padding)
    #     y1 = max(0, y - vertical_padding)
    #     x2 = min(image.shape[1], x + w + horizontal_padding)
    #     y2 = min(image.shape[0], y + h + vertical_padding)
    #     segment = image[y1:y2, x1:x2]
    #     segments.append(segment)

    result_image = segment_result(image)
    left_team_image, right_team_image = split_teams(image)
    left_team_players_images= split_players(left_team_image)
    right_team_players_images = split_players(right_team_image)

    segmented_images = {
        "result": result_image,
        "left_team_players": left_team_players_images,
        "right_team_players": right_team_players_images
    }

    return segmented_images

def segment_result(image):
    """
    勝敗のテキスト（VICTORY, LOSE）の画像領域を抽出する。
    """
    # 画像の上部中央部分を切り抜く
    height, width = image.shape[:2]
    result_image = image[0:int(height * 0.2), int(width * 0.4):int(width * 0.6)]

    return result_image

def split_teams(image):
    """
    画像を2つの部分に分割する（左側: 味方チーム、右側: 敵チーム）。
    """
    height, width = image.shape[:2]
    left_team_image = image[:, :int(width * 0.5)]
    right_team_image = image[:, int(width * 0.5):]
    return left_team_image, right_team_image

def split_players(team_image):
    """
    各チーム内で、5つのプレイヤー情報ブロックに分割する。
    """
    height, width = team_image.shape[:2]
    header = team_image[0:199, :]
    body = team_image[200:height-162-1, :]
    footer = team_image[height-162: height, :]

    body_height, body_width = body.shape[:2]

    player_images = []
    for i in range(5):
        player_image = body[int(body_height * i / 5):int(body_height * (i + 1) / 5), :]
        player_images.append(player_image)
    return player_images



def save_all_segments(segmented_images):
    """
    画像の入った辞書を受け取り、各セグメントをファイルに保存する。
    """
    file_path = os.path.abspath(os.path.join(__file__, '../../app/static/images/segmented/'))
    print(file_path)
    for key, images in segmented_images.items():
        
        if key == 'left_team_players' or key == 'right_team_players':
            for i, image in enumerate(images):
                filename = f"{key}{i}.jpg"
                cv2.imwrite(os.path.join(file_path, filename), image)
        else:
            filename = f"{key}.jpg"
            cv2.imwrite(os.path.join(file_path, filename), images)