"""
このファイルでは、OCR関連の関数を定義します。
process_image(image): 画像を受け取り、OCRを実行し、テキストデータを返す関数。
"""
import pytesseract

def ocr_segment(segment):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(segment, lang="eng+jpn+vie", config=custom_config)
    return text.strip()

def ocr_num_segment(segment):
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="0123456789-, "'
    text = pytesseract.image_to_string(segment, lang="eng", config=custom_config)
    return text.strip()