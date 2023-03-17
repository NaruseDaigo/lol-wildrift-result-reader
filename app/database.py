from flask import flash, render_template, request, redirect, url_for, g
import sqlite3
from app.models import MatchInfo

DATABASE = 'my_database.db'  # データベース名に変更してください。

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def save_match_info(match_info):
    db = get_db()
    cursor = db.cursor()

    # match_infoは、戦績情報が含まれる辞書オブジェクトと仮定しています。
    player_name = match_info['player_name']
    match_date = match_info['match_date']
    match_result = match_info['match_result']
    kills = match_info['kills']
    deaths = match_info['deaths']
    assists = match_info['assists']

    # 戦績情報をデータベースに保存するSQL文を作成します。
    query = f"""
    INSERT INTO matches (player_name, match_date, match_result, kills, deaths, assists)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    # SQL文を実行してデータベースに戦績情報を保存します。
    cursor.execute(query, (player_name, match_date, match_result, kills, deaths, assists))
    db.commit()
    cursor.close()

def get_match_info_from_db(match_id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM matches WHERE id=?", (match_id,))
    match_info = cur.fetchone()

    if match_info:
        return {
            "match_id": match_info[0],
            "victory_or_lose": match_info[1],
            "left_team": match_info[2],
            "right_team": match_info[3]
        }
    else:
        return None