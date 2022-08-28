# 【Python】CSVファイルをExcelにインポートする
updated at 2022/8/28

## 実行内容
CSVファイルを Excel(xlsx)のシートに読み込む。

1. CSVファイル名とExcel(xlsx)のファイル名は引数として与える。
2. CSVファイルの1行目はヘッダとして、Excelの先頭行に設定する。
3. CSVファイルのヘッダを使用しないオプションも可能とする。
4. CSVファイルの読み込み開始行を指定できるようにする。（-h オプション）
5. CSVファイルのデータの行番号Excelデータに追加できるようにする（-n オプション）。
6. CSVファイルのデータを可能ならば数値に変換できるようにする。（-v オプション）。
7. Excelファイルおよびシートが存在しない場合は新規作成、存在する場合は追記する。
8. Excelファイルのシート名はCSVファイルのファイル名(拡張子を除く)とする。
9. Excelファイルのシート名を指定できるようにする。（-s オプション）
10. Excelのシートへの開始セル位置を指定できるようにする（-c オプション）
11. Excelのシートへの挿入部分に罫線を付加できるようにする。（-b オプション）
11. Excelのシートへの挿入部分のセルの列幅を自動設定できるようにする。（-w オプション）
12. TSVファイルの読み込みにも対応する。（-t オプション）

### 実行例

```Shell
# オプション無し
python3 input.csv output.xlsx

# オプション設定有り
python3 input.csv -n -v -b -w output_xlsx -s sheet_name -c B2 
```

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import pathlib
import csv
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill, Border, Side

# 引数不足時に使用方法を表示
def print_usage(arg0):
  print(f'Usage:')
  print(f'  {arg0} [-h line_num] [-t] [-n] [-v] [-b] [-w] input_csv output_xlsx [-s sheet_name] [-c cell_address] [col1 col2 col3]')
  return()

def str_to_num(vstr):
  try:
    ival = int(vstr, 10)
  except ValueError:
    try:
      fval = float(vstr)
    except ValueError:
      return vstr
    else:
      return fval
  else:
    return ival

def csv_to_xlsx(fcsv,fxlsx,shname,cadr,dval,nval,vval,bval,wval,hval,hlist):
  print(fcsv,fxlsx,shname)
  print(sys.getfilesystemencoding())
  # csvデータを2次元配列 rowsに読み込む
  #   vval = 1 でcsvデータを数値に変換（可能な場合のみ）
  #   nval = 1 でcsvデータに行番号を追加
  #   hvalで指定された行数をheader行としてそれ以降を読み込む
  #   hval = 0 はcsvデータにheader行が無いもの（すべてデータ行）とする
  #   dval に delimiterを設定する
  #   shname シート名を設定する
  #   cadr 書き込み位置を指定する（A1形式）
  #   bval = 1 で罫線設定
  #   wval = 1 でセル幅自動設定
  column_str_max = 64
  rows = []
  rnum = 0
  cnum_max = 0
  clen_max = []
  # 日本語の処理が不要ならば open(fcsv, 'r') でよい
  with open(fcsv, 'r', encoding='utf-8') as f: 
    read_csv = csv.reader(f, delimiter=dval)
    for row in range(hval):
      row0 = next(read_csv)
    # CSVデータ読込み（行番号付加,最大文字数取得）
    for row in read_csv:
      col_len = [len(vstr) for vstr in row]
      if vval == 0:
        row_num = row
      else:
        row_num = [str_to_num(vstr) for vstr in row]
      if nval == 0:
        row_i = []
        col_length = []
      else:
        row_i = [rnum + 1]
        col_length = [len(str(rnum+1))]
      row_i.extend(row_num)
      rows.append(row_i)
      col_length.extend(col_len)
      for col_i in range(0,len(col_length)):
        if col_i < len(clen_max):
          clen_max[col_i] = max(clen_max[col_i],col_length[col_i])
        else:
          clen_max.append(col_length[col_i])
      cnum_max = max(len(row_i),cnum_max)
      rnum = rnum + 1
  print(f'Recore: {rnum} , Field: {cnum_max}')

  # ヘッダ作成
  if nval == 0:
    cnum_add = 0
    header_list = []
  else:
    cnum_add = 1
    header_list = ["No."]
  cnum = 0 + cnum_add
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
      header_list.append( "col_" + str(col+1-cnum_add) )

  print(f'Header: {header_list}')
  print(f'Column width: {clen_max}')

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
  
  # Excelのフォーマット等の設定
  # Fone(name='Calibri', size=11, bold=False, italic=False, underline='none', strike=False,
  #      vertAlign=None, color='FF000000')
  header_f = Font(name='BIZ UDPGothic', size=10, bold=True,  color='ff000000')
  val_f    = Font(name='BIZ UDGothic', size=10, bold=False, color='ff000000')
  header_p = PatternFill(patternType='solid', fgColor='88ccff')
  val_p    = PatternFill(patternType='solid', fgColor='ffffff')
  side_1   = Side(border_style='thin', color='000000')
  side_2   = Side(border_style='double', color='000000')
  if bval == 1:
    header_b = Border(left=side_1, right=side_1, top=side_1, bottom=side_2)
    val_b    = Border(left=side_1, right=side_1, bottom=side_1)
  else:
    header_b = Border(left=None, right=None, top=None, bottom=None)
    val_b    = Border(left=None, right=None, top=None, bottom=None)
  # 書き込み
  irow = ws[cadr].row
  icol = ws[cadr].column
  r = irow
  c = icol
  for val in header_list:
    ws.cell(row=r,column=c).value=val
    ws.cell(row=r,column=c).font=header_f
    ws.cell(row=r,column=c).fill=header_p
    ws.cell(row=r,column=c).border=header_b
    c = c + 1
  for row in rows:
    r = r + 1
    c = icol
    for val in row:
      ws.cell(row=r,column=c).value=val
      ws.cell(row=r,column=c).font=val_f
      #ws.cell(row=r,column=c).fill=val_p
      ws.cell(row=r,column=c).border=val_b
      c = c + 1
  irow_max = r
  icol_max = icol + cnum_max - 1
  #print(f'Row: {irow} , {irow_max} Col: {icol} , {icol_max}')
   
  # セル幅設定
  if wval == 1:
    for c in range(icol,icol_max + 1):
      col_str = ws.cell(row=irow,column=c).column_letter
      clen_val = 1.2 * min(column_str_max,max(4,clen_max[(c - icol)]))
      ws.column_dimensions[col_str].width = clen_val
      #print(c,clen_val)
  # フィルタ設定
  col_max_letter = get_column_letter(icol_max)
  range_str = cadr + ":" + col_max_letter + str(irow_max)
  ws.auto_filter.ref = range_str
  print(f'Sheet: {shname} , Range: {range_str}')
  
  wb.save(filename=fxlsx)
  wb.close()
  
  return(rnum,cnum_max)

if __name__ == '__main__':
  args = sys.argv
  hkey = '-h'
  dkey = '-t'
  skey = '-s'
  ckey = '-c'
  nkey = '-n'
  vkey = '-v'
  bkey = '-b'
  wkey = '-w'
  hval = 1
  dval = ','
  shname = 'Sheet1'
  cval = 'A1'
  nval = 0
  vval = 0
  bval = 0
  wval = 0
  
  arg_num = 3
  arg_num = (arg_num + 2) if hkey in args else arg_num
  arg_num = (arg_num + 1) if dkey in args else arg_num
  arg_num = (arg_num + 2) if skey in args else arg_num
  arg_num = (arg_num + 2) if ckey in args else arg_num
  arg_num = (arg_num + 1) if nkey in args else arg_num
  arg_num = (arg_num + 1) if vkey in args else arg_num
  arg_num = (arg_num + 1) if bkey in args else arg_num
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
    if nkey in args:
      aidx = args.index(nkey)
      nval = 1
      del args[aidx]
    if vkey in args:
      aidx = args.index(vkey)
      vval = 1
      del args[aidx]
    if bkey in args:
      aidx = args.index(bkey)
      bval = 1
      del args[aidx]
    if wkey in args:
      aidx = args.index(wkey)
      wval = 1
      del args[aidx]
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
      csv_to_xlsx(args[1], args[2], shname, cval, dval, nval, vval, bval, wval, hval, hlist)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print_usage( args[0] )
```

## References

* [csv (docs.python.org)](https://docs.python.org/ja/3/library/csv.html)
* [pathlib (docs.python.org)](https://docs.python.org/ja/3/library/pathlib.html))
* [openpyxl Workbook (https://openpyxl.readthedocs.io)](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.workbook.workbook.html#module-openpyxl.workbook.workbook)
* [openpyxl load_workbook (https://openpyxl.readthedocs.io)](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.reader.excel.html#openpyxl.reader.excel.load_workbook)
