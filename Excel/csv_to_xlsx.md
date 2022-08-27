# 【Python】CSVファイルをExcelにインポートする

## 実行内容
CSVファイルを Excel(xlsx)のシートに読み込む。

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import pathlib
import csv
import openpyxl

# 引数不足時に使用方法を表示
def print_usage(arg0):
  print(f'Usage:')
  print(f'  {args[0]} [-h line_num] [-t] input_csv output_xlsx [-s sheet_name] [col1 col2 col3]')
  return()

def csv_to_xlsx(fcsv,fxlsx,shname,dval,hval,hlist):
  print(fcsv,fxlsx,shname)
  print(sys.getfilesystemencoding())
  # csvデータを2次元配列 rowsに読み込む
  #   hvalで指定された行数をheader行としてそれ以降を読み込む
  #   hval = 0 はcsvデータにheader行が無いもの（すべてデータ行）とする
  #   dval に delimiterを設定する
  #   shname シート名を設定する
  
  rows = []
  rnum = 0
  cnum_max = 0
  # 日本語の処理が不要ならば open(fcsv, 'r') でよい
  with open(fcsv, 'r', encoding='utf-8') as f: 
    read_csv = csv.reader(f, delimiter=dval)
    for row in range(hval):
      row0 = next(read_csv)
    for row in read_csv:
      rows.append(row)
      cnum_max = max(len(row),cnum_max)
      rnum = rnum + 1
  print(f'Recore: {rnum} , Field: {cnum_max}')
 
  return(rnum,cnum_max)

if __name__ == '__main__':
  args = sys.argv
  hkey = '-h'
  dkey = '-t'
  skey = '-s'
  hval = 1
  dval = ','
  shname = 'sheet1'

  arg_num = 2
  arg_num = (arg_num + 2) if hkey in args else arg_num
  arg_num = (arg_num + 1) if dkey in args else arg_num
  arg_num = (arg_num + 2) if skey in args else arg_num
  if arg_num <= len(args):
    if hkey in args:
      aidx = args.index(hkey)
      hval = int(args[aidx+1])
      del args[aidx:aidx+2]
    if dkey in args:
      aidx = args.index(dkey)
      dval = '\t'
      del args[aidx]
    if skey in args:
      aidx = args.index(hkey)
      shname = args[aidx+1]
      del args[aidx:aidx+2]
    if os.path.isfile(args[1]):
      #シート名をCSVファイル名から取得(-s 指定が無かった時)
      if shname == 'sheet1' :
        csv_file = pathlib.Path(args[1])
        shname = csv_file.stem
      #カラムヘッダを取得（指定されていた場合のみ）
      hlist = []
      for i in range( 3, len(args) ):
        hlist.append(args[i])
      csv_to_xlsx(args[1], args[2], shname, dval, hval, hlist)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print_usage( arg[0] )
```

## References

* [csv (docs.python.org)](https://docs.python.org/ja/3/library/csv.html)
* [openpyxl Docs (https://openpyxl.readthedocs.io/)](https://openpyxl.readthedocs.io/en/stable/#introduction)
* [pathlib (docs.python.org)](https://docs.python.org/ja/3/library/pathlib.html))
