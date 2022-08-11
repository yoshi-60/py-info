# ローカルに Python をインストールする
updated at 2022/8/10

# Python のインストール
Python 3.9 の最新版である [3.9.13](https://www.python.org/downloads/release/python-3913/) (2022/5/17) をインストールします。  
ルート権限は無いものとします。

```Shell
mkdir -p $HOME/src
cd $HOME/src

wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tar.xz
tar Jxvf Python-3.9.13.tar.xz

cd Python-3.9.13
./configure --prefix=$HOME/local/python-3.9.13/
make
make install

export PATH=$PATH:$HOME/local/python-3.9.13/bin
```
