# Flaskで遊ぼう

## 1. pip、Flaskインストール

    $ sudo apt-get install python-pip
    $ sudo pip install Flask


## 2. サンプル作成

    $ mkdir flask && cd flask
    $ vi index.py
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        
        from flask import Flask
        app = Flask(__name__)
        
        @app.route("/")
        def hello():
            return "Hello World!"
        
        if __name__ == "__main__":
            app.run('0.0.0.0', debug=True)
            
     $ python index.py

WEBサーバが起動したので、```http://<IPアドレス>:5000/```にアクセス。```Hello World```と画面に表示されます。

## 3. SSLに対応
### 3.1 オレオレ証明書の作成

    $ openssl genrsa 2048 > server.key
    $ openssl req -new -key server.key > server.csr
    $ openssl x509 -days 3650 -req -signkey server.key < server.csr > server.crt
    $ rm -f server.csr

作成した鍵たちは任意のところに保存しておいてください。

### 3.2 FlaskでSSLを
起動時の設定に証明書を設定
    
    app.run('0.0.0.0', debug=True, ssl_context=(
      '<server.keyのディレクトリ>/server.crt',
      '<server.keyのディレクトリ>/server.key'
    ))    

```server.crt``` と ```server.key``` は先ほど保存したパスを指定して下さい。

これで **```https://<IPアドレス>:5000/```** にアクセスすると無事にsslでの通信が完了です。

## 4. Basic認証をかける
この[サイト](http://d.hatena.ne.jp/tell-k/20111005/1317781147)を参考にやってみました。

このサイトに説明になってしまうので、簡単に説明します。

- decorator.pyの作成
    - ここでID/PASSのチェックを行います
- FlaskにもFilterのような物が存在しているために、その部分で認証を行う
