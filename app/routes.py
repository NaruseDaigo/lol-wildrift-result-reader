"""
このファイルでは、アプリケーションのルーティングとビュー関数を定義します。
index(): トップページを表示する関数。
upload(): 画像をアップロードし、プレビュー画面にリダイレクトする関数。
preview(): アップロードされた画像のプレビュー画面を表示する関数。
stats(): 解析結果を表示する関数。
"""
import os
import cv2
import logging
from app import app, db
from app.database import get_match_info_from_db, save_match_info
from flask import flash, render_template, request, redirect, url_for, g
from werkzeug.utils import secure_filename
from utils.image_processing import preprocess_image
from utils.data_extraction import extract_match_info

# ロギング
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s:%(name)s - %(message)s")
file_handler = logging.FileHandler('/Users/daigo/workspace/lol-wildrift-stats/logs/app.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

UPLOAD_FOLDER = 'app/static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    logger.debug("index() 関数が実行されました。")
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    logger.debug("upload() 関数が実行されました。")
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        image_filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, image_filename)
        file.save(file_path)

        return redirect(url_for('analyze', image_filename=image_filename))

    return redirect(url_for('index'))

@app.route('/analyze/<image_filename>', methods=['GET'])
def analyze(image_filename):
    logger.debug("analyze() 関数が実行されました。")
    file_path = os.path.join(UPLOAD_FOLDER, image_filename)
    preprocessed_image = preprocess_image(file_path)
    logger.debug("preprocess_image() 関数が完了しました。")
    match_info = extract_match_info(preprocessed_image)
    logger.debug("extract_match_info() 関数が完了しました。")

    return render_template('match_result.html', match_info=match_info)


@app.route('/preview/<image_filename>')
def preview(image_filename):
    # file_path = os.path.join(UPLOAD_FOLDER, image_filename)
    return render_template('preview.html', image_filename=image_filename)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()