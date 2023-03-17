"""
多分、models.pyはクラスを定義するのが一般的
このファイルでは、データベースのモデル（テーブル）を定義します（データベースを使用する場合）。
class PlayerStats(db.Model): プレイヤーの戦績を格納するテーブルのモデルクラス。
"""

from app import db

class MatchInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(128), nullable=False)
    victory_or_lose = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<MatchInfo id={self.id} victory_or_lose={self.victory_or_lose}>"
