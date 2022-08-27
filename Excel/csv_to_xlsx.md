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
from openpyxl import load_workbook
from openpyxl import Workbook

# 引数不足時に使用方法を表示
def print_usage(arg0):
  print(f'Usage:')
  print(f'  {arg0} [-h line_num] [-t] input_csv output_xlsx [-s sheet_name] [-c cell_address] [col1 col2 col3]')
  return()

def csv_to_xlsx(fcsv,fxlsx,shname,cadr,dval,hval,hlist):
  print(fcsv,fxlsx,shname)
  print(sys.getfilesystemencoding())
  # csvデータを2次元配列 rowsに読み込む
  #   hvalで指定された行数をheader行としてそれ以降を読み込む
  #   hval = 0 はcsvデータにheader行が無いもの（すべてデータ行）とする
  #   dval に delimiterを設定する
  #   shname シート名を設定する
  #   cadr 書き込み位置を指定する（A1形式）
  
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

  # ヘッダ作成
  cnum = 0
  header_list = []
  if (hval == 0) or (len(hlist) > 0) :
    for col in hlist:
      cnum = cnum + 1
      header_list.append(col)
  else:
    for col in row0:
      cnum = cnum + 1
      header_list.append(col)
  # headerの数が不足していた時の処置
  if cnum < cnum_max:
    for col in range(cnum, cnum_max):
      header_list.append( "col_" + str(col+1) )

  # Excelのブックを開く
  if os.path.isfile(fxlsx):
    wb = load_workbook(filename=fxlsx, read_only=False)
  else:
    wb = Workbook()
    ws = wb.worksheets[0]
    ws.title = shname
  # シートの存在確認と作成
  if shname in wb.sheetnames:
    ws = wb[shname]
  else:
    ws = wb.create_sheet(shname)
  
  # 書き込み
  irow = ws[cadr].row
  icol = ws[cadr].column
  r = irow
  c = icol
  for val in header_list:
    ws.cell(row=r,column=c).value=val
    c = c + 1
  for row in rows:
    r = r + 1
    c = icol
    for val in row:
      ws.cell(row=r,column=c).value=val
      c = c + 1
  irow_max = r - 1
  icol_max = icol + cnum_max - 1
  
  wb.save(filename=fxlsx)
  wb.close()
  
  return(rnum,cnum_max)

if __name__ == '__main__':
  args = sys.argv
  hkey = '-h'
  dkey = '-t'
  skey = '-s'
  ckey = '-c'
  hval = 1
  dval = ','
  shname = 'Sheet1'
  cval = 'A1'
  
  arg_num = 3
  arg_num = (arg_num + 2) if hkey in args else arg_num
  arg_num = (arg_num + 1) if dkey in args else arg_num
  arg_num = (arg_num + 2) if skey in args else arg_num
  arg_num = (arg_num + 2) if ckey in args else arg_num
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
      aidx = args.index(skey)
      shname = args[aidx+1]
      del args[aidx:aidx+2]
    if ckey in args:
      aidx = args.index(ckey)
      cval = args[aidx+1]
      del args[aidx:aidx+2]
    if os.path.isfile(args[1]):
      #シート名をCSVファイル名から取得(-s 指定が無かった時)
      if shname == 'Sheet1' :
        csv_file = pathlib.Path(args[1])
        shname = csv_file.stem
      #カラムヘッダを取得（指定されていた場合のみ）
      hlist = []
      if 4 <= len(args):
        for i in range( 3, len(args) ):
          hlist.append(args[i])
      csv_to_xlsx(args[1], args[2], shname, cval, dval, hval, hlist)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print_usage( args[0] )
```

## References

* [csv (docs.python.org)](https://docs.python.org/ja/3/library/csv.html)
* [openpyxl Docs (https://openpyxl.readthedocs.io/)](https://openpyxl.readthedocs.io/en/stable/#introduction)
* [pathlib (docs.python.org)](https://docs.python.org/ja/3/library/pathlib.html))
