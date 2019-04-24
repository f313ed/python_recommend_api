#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
■ 使い方
アプリケーションサーバを立ち上げ
$ python3 app.py

Webサーバを立ち上げ
$ python3 -m http.server 8080

http://localhost:8080/
にアクセスするとコンソールにレコメンド指数が表示されます

■ 参考
https://cloudpack.media/44251


"""







from wsgiref.simple_server import make_server
from package.score import Score


import json

def app(environ, start_response):
    status = '200 OK'
    headers = [
        ('Content-type', 'application/json; charset=utf-8'),
        ('Access-Control-Allow-Origin', '*'),
    ]
    start_response(status, headers)

    # 顧客(id:100) に対するキャストごとのレコメンド指数を取得
    score = Score(100)
    scores = score.get_scores()

    return [json.dumps(scores).encode("utf-8")]
    # return [json.dumps({'message':'hoge'}).encode("utf-8")]   #sample ok


with make_server('', 3000, app) as httpd:
    print("Serving on port 3000...")
    httpd.serve_forever()




"""
# from package.score import Score
# # 顧客(id:100) に対するキャストごとのレコメンド指数を取得　
# score = Score(100)
# scores = score.get_scores()
# print(scores)
"""

