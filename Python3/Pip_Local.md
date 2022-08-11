# pip でのインストールをローカルにダウンロードしたファイルで行う
updated at 2022/8/10

## パッケージファイルの取得
Excelファイルの操作に用いられる「openpyxl」を例に説明する。

### pip download で取得
引数にパッケージ名を指定してpip downloadを実行する。  
-dオプションで、ダウンロード先のディレクトリが指定できる（指定がない場合は、カレントディレクトリに保存）。  
依存関係にあるパッケージも保存される。

```Shell
mkdir -p $HOME/packages
pip download -d $HOME/packages openpyxl==3.0.10
```

### 必要なファイルをブラウザからダウンロード
ブラウザからダウンロードする場合は、openpyxlだけでなく、jdcalとet_xmlfileという  
openpyxlが利用しているライブラリも一緒にインストールする。  
そのため、全部で3つのライブラリのファイルをダウンロードする。

* [https://pypi.org/project/openpyxl/#files](https://pypi.org/project/openpyxl/#files)
* [https://pypi.org/project/jdcal/#files](https://pypi.org/project/jdcal/#files)
* [https://pypi.org/project/et_xmlfile/#files](https://pypi.org/project/et_xmlfile/#files)

```Shell
mkdir -p $HOME/packages
cd $HOME/packages
wget https://files.pythonhosted.org/packages/7b/60/9afac4fd6feee0ac09339de4101ee452ea643d26e9ce44c7708a0023f503/openpyxl-3.0.10-py2.py3-none-any.whl
wget https://files.pythonhosted.org/packages/f0/da/572cbc0bc582390480bbd7c4e93d14dc46079778ed915b505dc494b37c57/jdcal-1.4.1-py2.py3-none-any.whl
wget https://files.pythonhosted.org/packages/96/c2/3dd434b0108730014f1b96fd286040dc3bcb70066346f7e01ec2ac95865f/et_xmlfile-1.1.0-py3-none-any.whl
```

## パッケージのインストール
引数にパッケージ名を指定してpip installを実行する。  
--user オプションで管理者権限無しでインストールできる。
--no-index オプションでPyPIへの参照を無効化し、  
--find-links オプションで指定したディレクトリからパッケージを検索する。  
環境変数 **PYTHONUSERBASE** で user install のインストール先を変更できる（デフォルトは `~/.local` ）。

```Shell
mkdir -p $HOME/local/python
export PYTHONUSERBASE=$HOME/local/python
python3 -m site --user-base

pip install --user --no-index --find-links=$HOME/packages openpyxl
```
