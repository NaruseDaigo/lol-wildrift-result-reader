"""
このファイルでは、OCR関連の関数を定義します。
process_image(image): 画像を受け取り、OCRを実行し、テキストデータを返す関数。
"""
import pytesseract
import difflib

def ocr_segment(segment):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(segment, lang="eng+jpn+vie", config=custom_config)
    return text.strip()

def ocr_result_segment(segment):
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="VICTORYDEFEAT"'
    distorted_text = pytesseract.image_to_string(segment, lang="eng", config=custom_config)
    text = closest_match(distorted_text.strip())
    return text

def ocr_num_segment(segment):
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="0123456789, "'
    text = pytesseract.image_to_string(segment, lang="eng", config=custom_config)
    text = text.strip()
    return text


def closest_match(text):
    victory_match = difflib.SequenceMatcher(None, text, "VICTORY").ratio()
    defeat_match = difflib.SequenceMatcher(None, text, "DEFEAT").ratio()

    if victory_match > defeat_match:
        return "VICTORY"
    else:
        return "DEFEAT"
