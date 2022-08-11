# Python3で使う SQLiteのバージョンを変更する
updated at 2022/8/10

## SQLiteのインストール

現時点（2022年8月10日）での最新版である [SQLite Version 3.39.2](https://www.sqlite.org/releaselog/3_39_2.html) (2022-07-21) をインストールします。  
ルート権限は無いものとします。

```Shell
mkdir -p $HOME/src
cd $HOME/src
wget https://www.sqlite.org/2022/sqlite-autoconf-3390200.tar.gz
tar xvzf sqlite-autoconf-3390200.tar.gz
cd sqlite-autoconf-3390200
./configure --prefix=$HOME/local/sqlite-3.39.02/
make
make install

$HOME/local/sqlite-3.39.02/bin/sqlite3 --version
```

## Python3 で SQLite 3.39.2 を使用

環境変数 LD_LIBRARY_PATH に、lib の絶対パスを指定します。

```Shell
export LD_LIBRARY_PATH=$HOME/local/sqlite-3.39.02/lib:$LD_LIBRARY_PATH

python3

>>> import sqlite3
>>> sqlite3.sqlite_version
'3.39.2'

>>> con = sqlite3.connect(":memory:")
>>> cur = con.cursor()
>>> cur.execute("SELECT sqlite_version()")
>>> cur.fetchone()
('3.39.2',)
```
