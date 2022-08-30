# 【Python】テキストファイルをExcelにインポートする
updated at 2022/8/30

## 実行内容
テキストファイルを Excel(xlsx)のシートに読み込む。

1. テキストファイル名とExcel(xlsx)のファイル名は引数として与える。
2. テキストファイル名をExcelの先頭行に設定する。
3. テキストファイル名を入力しないこともできるようにする。（-h オプション）
4. テキストファイル名の入力セルとデータ入力開始位置を変更できるようにする。（-h オプション）
5. テキストファイルの読み込み開始行と終了行を指定できるようにする。（-l オプション）
6. テキストファイルのデータの行番号Excelデータに追加できるようにする（-n オプション）。
7. Excelファイルおよびシートが存在しない場合は新規作成、存在する場合は追記する。
8. Excelファイルのシート名はテキストファイルのファイル名(拡張子を除く)とする。
9. Excelファイルのシート名を指定できるようにする。（-s オプション）
10. Excelのシートへの開始セル位置を指定できるようにする（-c オプション）
11. Excelのシートへの挿入部分に罫線を付加できるようにする。（-b オプション）
12. Excelのシートへの挿入部分のセルの列幅を自動設定できるようにする。（-w オプション）
13. Excelのシートへのテキストデータの挿入行をグループ化し、折りたためるようにする。（-g オプション）

### 実行例

```Shell
# オプション無し
python3 input.txt output.xlsx

# オプション設定有り
python3  input.txt  output_xlsx -h 1 0 -l 10 -20 -n -b -w -g -s sheet_name -c B3
```

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import pathlib
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Border, Side
from openpyxl.worksheet.properties import Outline

# 引数不足時に使用方法を表示
def print_usage(arg0):
  print(f'Usage:')
  print(f'  {arg0}  input_txt  output_xlsx [-l start end] [-n] [-b] [-w] [-g] [-s sheet_name] [-h row col] [-c cell_address]')
  print('       -l j k : Import line number')
  print('       -h n m : header(file name) line offset (default = 1 1, No header = 0 0)')
  print('       -n : add line number')
  print('       -b : add border')
  print('       -w : column width adjust')
  print('       -g : group row')
  print('       -s sheet_name : default = text filename without extention')
  print('       -c cell_addr. : start address , default = A1')
  return()

def line_calc(llist,lnum):
  # Start
  if llist[0] == 0:
    lstart = 1
  elif llist[0] > 0 and llist[0] <= lnum:
    lstart = llist[0]
  elif llist[0] > lnum:
    lstart = 0
  elif llist[0] > (0 - lnum):
    lstart = lnum + llist[0]
  else:
    lstart = 1
  # End
  if llist[1] == 0:
    lend = lnum
  elif llist[1] > 0 and llist[1] <= lnum:
    lend = llist[1]
  elif llist[1] > lnum:
    lend = lnum
  elif llist[1] > (0 - lnum):
    lend = lnum + llist[1]    
  else:
    lend = 0
  if lstart == 0 or lend == 0 or lstart > lend:
    lstart = 0
    lend = 0
  #print(f'Input: {llist[0]} , {llist[1]} , {lnum} , Output; {lstart} , {lend}')
  return lstart,lend

def text_to_xlsx(ftxt,fxlsx,shname,cadr,nval,bval,wval,gval,hlist,llist):
  print(ftxt,fxlsx,shname)
  print(sys.getfilesystemencoding())
  # テキストデータを2次元配列 rowsに読み込む
  #   nval = 1 でテキストデータに行番号を追加
  #   hlistでファイル名とデータの間隔を指定
  #   llistで指定された行番号のみ読み込む
  #   shname シート名を設定する
  #   cadr 書き込み位置を指定する（A1形式）
  #   bval = 1 で罫線設定
  #   wval = 1 でセル幅自動設定
  #   gval = 1 グループ化
  column_str_max = 96
  rows = []
  rnum = 0
  clen_max = [0,0]
  col_max = 0
  # テキストファイル読み込み
  with open(ftxt, 'r', encoding='utf-8') as f: 
    read_txt = f.readlines()
  # テキストデータ取り込み（行番号付加,最大文字数取得）
  lnum = len(read_txt)
  lstart,lend = line_calc(llist,lnum)
  if lstart > 0:
    for ir in range(lstart,lend+1):
      row = read_txt[ir-1].rstrip('\n')
      col_max = max(col_max,len(row))
      if nval == 0:
        row_i = []
      else:
        row_i = [ir]
      row_i.append(row)
      rows.append(row_i)
      rnum = rnum + 1
    clen_max = [len(str(lend)),col_max]
  print(f'Recore: {lnum} , Import: {rnum} , Line: {lstart} - {lend}')
  # ヘッダ作成
  txt_file = pathlib.Path(ftxt)
  file_name = txt_file.name
  print(f'File name: {file_name}')
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
  # Font(name='Yu Gothic', size=11, bold=False, italic=False, underline='none', strike=False,
  #      vertAlign=None, color='FF000000')
  ws.sheet_properties.outlinePr = Outline(applyStyles=None, summaryBelow=False, summaryRight=False, showOutlineSymbols=None)
  header_f = Font(name='BIZ UDPGothic', size=10, bold=True,  color='ff0000ff')
  val_f    = Font(name='BIZ UDGothic', size=10, bold=False, color='ff000000')
  side_1   = Side(border_style='thin', color='000000')
  if bval == 1:
    val_b    = Border(left=side_1, right=side_1, top=side_1, bottom=side_1)
  else:
    val_b    = Border(left=None, right=None, top=None, bottom=None)
  # 書き込み
  irow = ws[cadr].row
  icol = ws[cadr].column
  r = irow
  c = icol
  # ヘッダ(ファイル名)
  if hlist[0] > 0:
    ws.cell(row=r,column=c).value=file_name
    ws.cell(row=r,column=c).font=header_f
    irow_h = irow
    icol_h = icol
  else:
    hlist = [0,0] 
    irow_h = 0
    icol_h = 0
  if hlist[1] < 0:
    hlist[1] = 0
  irow_d = irow + hlist[0]
  icol_d = icol + hlist[1]
  # file line
  r = irow_d
  for row in rows:
    c = icol_d
    for val in row:
      ws.cell(row=r,column=c).value=val
      ws.cell(row=r,column=c).font=val_f
      ws.cell(row=r,column=c).border=val_b
      c = c + 1
    r = r + 1
  irow_max = r - 1
  icol_max = icol_d + nval
  print(f'Header Row: {irow_h} , Col: {icol_h}')
  print(f'Data   Row: {irow_d} , {irow_max} Col: {icol_d} , {icol_max}')
   
  # セル幅設定
  if wval == 1:
    for c in range(icol_d,icol_max + 1):
      col_str = ws.cell(row=irow,column=c).column_letter
      clen_val = 1.1 * min(column_str_max,max(4,clen_max[(c - icol_d)]))
      ws.column_dimensions[col_str].width = clen_val
      #print(c,clen_val)
  # グループ（アウトライン）設定
  row_st  = irow_d
  row_end = irow_max
  if gval == 1:
    ws.row_dimensions.group(row_st, row_end, outline_level=1, hidden=True)

  col_max_letter = get_column_letter(icol_max) 
  range_str = cadr + ":" + col_max_letter + str(irow_max)
  #ws.auto_filter.ref = range_str
  print(f'Sheet: {shname} , Range: {range_str}')
  
  wb.save(filename=fxlsx)
  wb.close()
  
  return(lnum,rnum)

if __name__ == '__main__':
  args = sys.argv
  lkey = '-l'
  hkey = '-h'
  skey = '-s'
  ckey = '-c'
  nkey = '-n'
  bkey = '-b'
  wkey = '-w'
  gkey = '-g'
  hval = [1,1]
  lval = [0,0]
  shname = 'Sheet1'
  cval = 'A1'
  nval = 0
  bval = 0
  wval = 0
  gval = 0
  
  arg_num = 3
  arg_num = (arg_num + 3) if hkey in args else arg_num
  arg_num = (arg_num + 3) if lkey in args else arg_num
  arg_num = (arg_num + 2) if skey in args else arg_num
  arg_num = (arg_num + 2) if ckey in args else arg_num
  arg_num = (arg_num + 1) if nkey in args else arg_num
  arg_num = (arg_num + 1) if bkey in args else arg_num
  arg_num = (arg_num + 1) if wkey in args else arg_num
  arg_num = (arg_num + 1) if gkey in args else arg_num
  if arg_num <= len(args):
    if lkey in args:
      aidx = args.index(lkey)
      lval = [int(args[aidx+1]),int(args[aidx+2])]
      del args[aidx:aidx+3]
    if hkey in args:
      aidx = args.index(hkey)
      hval = [int(args[aidx+1]),int(args[aidx+2])]
      del args[aidx:aidx+3]
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
    if bkey in args:
      aidx = args.index(bkey)
      bval = 1
      del args[aidx]
    if wkey in args:
      aidx = args.index(wkey)
      wval = 1
      del args[aidx]
    if gkey in args:
      aidx = args.index(gkey)
      gval = 1
      del args[aidx]
    if os.path.isfile(args[1]):
      # シート名をテキストファイル名から取得(-s 指定が無かった時)
      if shname == 'Sheet1' :
        txt_file = pathlib.Path(args[1])
        shname = txt_file.stem
      text_to_xlsx(args[1], args[2], shname, cval, nval, bval, wval, gval, hval, lval)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print_usage( args[0] )
```

## References

* [pathlib (docs.python.org)](https://docs.python.org/ja/3/library/pathlib.html))
* [openpyxl Workbook (https://openpyxl.readthedocs.io)](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.workbook.workbook.html#module-openpyxl.workbook.workbook)
* [openpyxl load_workbook (https://openpyxl.readthedocs.io)](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.reader.excel.html#openpyxl.reader.excel.load_workbook)
