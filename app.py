"""
この構成では、appフォルダ内の__init__.pyファイルでFlaskアプリケーションを作成し、設定を適用し、ルートをインポートしています。
"""
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
