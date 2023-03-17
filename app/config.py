class Config(object):
    SECRET_KEY = 'your-secret-key'  # 必ず設定が必要です。秘密鍵として任意の文字列を設定してください。
    SQLALCHEMY_DATABASE_URI = 'sqlite:///my_database.db'  # あなたのデータベース名に変更してください。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # 他の設定項目もここに追加できます