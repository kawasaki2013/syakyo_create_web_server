# syakyo_create_web_server

書籍「[Webサーバを作りながら学ぶ　基礎からのWebアプリケーション開発入門](http://gihyo.jp/book/2016/978-4-7741-8188-2)」(前橋和弥　著)をPythonで書いてみたときのリポジトリです。

現在のところ、第1,2章のみの実装となっています。

　  
## 開発環境

- Windows10 x64
- Python 3.5.2 32bit

　  
それぞれ、

```
path\to\syakyo_create_web_server\src>python modoki02_main_2_6.py
```

のように実行します。

　  
## 書籍の項目と関係するファイル
### 1.3.2 TCPサーバ/クライアントのプログラム

- tcp_server_1_3_2.py
- tcp_client_1_3_2.py

また、送受信で使うファイルは、`file`ディレクトリの中にあります。

　  
### 1.5.3 1つのHTMLファイルを返す

- modoki01_1_5_3.py

　  
### 1.5.4 普通にWebページを表示できるようにする

- modoki01_1_5_4.py

　  
### 2.6 Modoki/0.2のソースコード

- modoki02_main_2_6.py
- modoki02_response_2_6.py
- modoki02_util_2_6.py

他に使用するhtmlやcssは`static`ディレクトリの中にもあります。

　  
## 関係するBlog

- [「Webサーバを作りながら学ぶ 基礎からのWebアプリケーション開発入門」が良かったのでPythonで書いてみた - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2016/07/04/064006)