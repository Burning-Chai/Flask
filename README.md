# Flaskで遊ぼう

皆さん、こんにちは。KEYチームの矢納です。少し間が空いてしまいました。

今回は[Flask](http://flask.pocoo.org/)を使ってみたので、使い方を紹介しようかなと思います。
Flaskを使ってみたのは自宅にRaspberryPiを用意し、外からアクセスできるようにしたいというのが発端です。RaspberryPi上で動く軽量なWEBサーバは何だろうと調べたら、Flaskがヒットしました。

> Flask（フラスク）は、プログラミング言語Python用の、軽量なウェブアプリケーションフレームワークである

wikipediaにしっかりと書いてありました(^o^)

では、やった事の紹介に入りたいと思います。実際に行った環境はRaspberryPi上です。

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

## 5. serving.pyの修正
この[サイト](http://flask.pocoo.org/snippets/111/)にもあるのですが、少しバグがあるそうです。

修正点としては serving.py の BaseWSGIServer に関数を一つ追加するだけです。

    $ sudo find / -name serving.py
    /usr/local/lib/python2.7/dist-packages/werkzeug/serving.py # RasiberryPiの場合
    $ sudo vi <servingのディレクトリ>/serving.py

serving.py の429行目に BaseWSGIServerクラスがあるので、そのクラスに下記の2行を追加してください。

    def shutdown_request(self,request):
        request.shutdown()

## おわりに

このブログで書いたコードはGitHubにあげてありますので、参考にしてください。
[https://github.com/Burning-Chai/Flask](https://github.com/Burning-Chai/Flask)

Email: yanou at atware.co.jp

