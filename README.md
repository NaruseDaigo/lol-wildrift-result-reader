# LoL Wild Rift Result Reader

LoL Wild Rift Result Readerは、League of Legends: Wild Riftの試合結果スクリーンショットをアップロードし、OCR技術を使用して試合結果を抽出するFlaskのWebアプリケーションです。\
このスマホゲームは公式がAPIを提供していないため、そうしてデータを取得することができません。また個人の戦績も50試合までしか保存されないし、統計情報もごく簡単なものしか提供されません。そこで試合結果のスクリーンショットを読み込み、データを構造化して保存するWeb アプリケーションを作っています。

## スクリーンショット
![index.html](https://user-images.githubusercontent.com/39047898/226121250-b5930458-d087-4bcb-b38a-73ae493a177e.png)
![match_result.html](https://user-images.githubusercontent.com/39047898/226121283-19586c79-7cd0-42c4-8220-1c6139339663.png )

## 主な機能

- スクリーンショットのアップロード
- 試合結果のOCR処理
- 各チームのプレイヤー名、キル数、デス数、アシスト数、ゴールド数の表示

# 追加予定

- イラストから使用キャラクター、購入アイテムも読み取る
- 対戦相手ごとの勝率など、データを分析して提示する

## 使い方

1. リポジトリをクローンまたはダウンロードし、プロジェクトフォルダに移動します。
2. 必要なパッケージをインストールするために、`pip install -r requirements.txt`を実行します。
3. `python set_db.py`を実行します。
3. アプリケーションを起動するために、`python app.py`を実行します。
4. Webブラウザで `http://localhost:5000` にアクセスし、画面の指示に従って画像をアップロードします。
5. アップロードされた画像から抽出された試合結果が表示されます。

## 開発環境

- Python 
- Flask 
- pytesseract 
- OpenCV 



