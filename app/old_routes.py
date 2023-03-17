"""
このプログラムに変更を加えて
DBに保存する処理をコメントアウトして、upload()関数に変更を加えて、画像解析結果を表示するようにしました。
確認が終わったら、このプログラムに戻ってくるか、参考にするかするかもしれない
"""
import os
from app import app, db
from app.database import get_match_info_from_db, save_match_info
from flask import flash, render_template, request, redirect, url_for, g
from werkzeug.utils import secure_filename
from utils.image_processing import preprocess_image
from utils.data_extraction import extract_stats

UPLOAD_FOLDER = 'app/static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        image_filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, image_filename)
        file.save(file_path)

        # 画像の前処理
        preprocessed_image = preprocess_image(file_path)

        # 戦績情報の抽出
        match_info = extract_stats(preprocessed_image)

        # 抽出した戦績情報をデータベースに保存
        save_match_info(match_info)

        return redirect(url_for('preview', image_filename=image_filename))

    return redirect(url_for('index'))


@app.route('/preview/<image_filename>')
def preview(image_filename):
    # file_path = os.path.join(UPLOAD_FOLDER, image_filename)
    return render_template('preview.html', image_filename=image_filename)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        preprocessed_image = preprocess_image(file_path)
        stats = extract_stats(preprocessed_image)
        
        return render_template('stats.html', stats=stats)
    else:
        flash('Allowed file types are png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/stats/<int:match_id>')
def stats(match_id):
    match_info = get_match_info_from_db(match_id)
    return render_template('stats.html', match_info=match_info)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()