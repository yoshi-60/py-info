# WindowsでPythonを使う
updated at 2022/8/17

## Windows環境でのPythonの使用

### 公式ページからインストーラをダウンロード

* [Python Releases for Windows](https://www.python.org/downloads/windows/) からインストールしたいバージョンの Windows Installer をダウンロードする。  
現時点での最新版(3.10.6)を 64bit版 Windowsにインストールする場合は、  
[Python 3.10.6 - Aug. 2, 2022](https://www.python.org/downloads/release/python-3106/) から
[Windows installer (64-bit)](https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe) をダウンロードする。

### パッケージのインストール

* ダウンロードしたパッケージを実行する。  
（Python 3.10.6 の場合は python-3.10.6-amd64.exe）  
<img width="480" alt="python-3.10.6-amd64" src="https://user-images.githubusercontent.com/49278963/185079105-bfe11488-ac54-4717-a1a5-19e19e45e03f.png">

* Install Nowをクリックすればよい。  
Windowsの場合、Pythonランチャー(py.exe) がインストールされるので  
「Add Python 3.10 to PATH」はチェックしなくてもよい。

コマンドプロンプトからバージョンを確認する

```powershell
C:\Users\username>py -V
Python 3.10.6
```

**.py** ファイルの関連付けを確認しておく
```powershell
C:\Users\username>assic .py
.py=Python.File

C:\Users\username>ftype Python.File
Python.File="C:\WINDOWS\py.exe" "%L" "%*"
```


## References

* [Windows で Python を使う (docs.python.org)](https://docs.python.org/ja/3/using/windows.html)
* [シェバン (shebang, '#!') 行 (docs.python.org)](https://docs.python.org/ja/3/using/windows.html#shebang-lines)
* [Windows の Python ランチャ (docs.python.org)](https://docs.python.org/ja/3/using/windows.html#python-launcher-for-windows)
