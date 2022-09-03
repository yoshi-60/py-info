# 【Python】CSVファイルをSQLiteにインポートする
updated at 2022/8/15

## 実行内容
CSVファイルからSQLite3のデータベースを作成する。
1. CSVファイル名とSQLiteのデータベースファイル名は引数として与える。
2. CSVファイルの1行目はヘッダとして、SQLiteのカラム名に設定する。
3. CSVファイルのヘッダを使用しないオプションも可能とする。
4. CSVファイルの読み込み開始行を指定できるようにする。（-h オプション）
5. TSVファイルの読み込みにも対応する。（-t オプション）
6. SQLiteのインデックスは1カラム目に新規に追加する。
7. SQLiteのデータタイプを指定できるようにする。（-d オプション）

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import csv
import sqlite3

def csv_to_sql(fcsv,fsql,dval,hval,hlist,tlist):
  print(fcsv,fsql)
  print(sys.getfilesystemencoding())
  # csvデータを2次元配列 rowsに読み込む
  #   hvalで指定された行数をheader行としてそれ以降を読み込む
  #   hval = 0 はcsvデータにheader行が無いもの（すべてデータ行）とする
  #   dval に delimiterを設定する
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

  # SQLiteのテーブル作成用テキスト作成
  if len(tlist) < cnum_max:
    for i in range(cnum_max - len(tlist)):
      tlist.append("TEXT")
  tname = hlist.pop(0)
  header_txt = "id_sql INTEGER PRIMARY KEY"
  cnum = 0
  insert_list = []
  if (hval == 0) or (len(hlist) > 0) :
    for col in hlist:
      dtype = tlist.pop(0)
      header_txt = header_txt + ", " + col + " " + dtype
      cnum = cnum + 1
      insert_list.append(col)
  else:
    for col in row0:
      dtype = tlist.pop(0)
      header_txt = header_txt + ", " + col + " " + dtype
      cnum = cnum + 1
      insert_list.append(col)
  
  # headerの数が不足していた時の処置
  if cnum < cnum_max:
    for col in range(cnum, cnum_max):
      dtype = tlist.pop(0)
      header_txt = header_txt + ", col_" + str(col+1) + " " + dtype
      insert_list.append( "col_" + str(col+1) )

  insert_txt = ",".join(insert_list)
  value_txt = "?"
  for i in range(cnum_max - 1):
    value_txt = value_txt + ",?"

  conn = sqlite3.connect(fsql)
  cur = conn.cursor()

  # テーブル作成
  exec_str = "CREATE TABLE IF NOT EXISTS " + tname + " (" + header_txt + ")"
  print(exec_str)
  cur.execute( exec_str )
  # データ追加
  exec_str = "INSERT INTO " + tname + " (" + insert_txt + ") VALUES (" + value_txt + ")"
  print(exec_str)
  cur.executemany( exec_str , rows)
  
  conn.commit()
  cur.close()
  conn.close()
  return(rnum,cnum_max)

if __name__ == '__main__':
  args = sys.argv
  hkey = '-h'
  dkey = '-t'
  tkey = '-d'
  tlist = []
  hval = 1
  dval = ','
  # -d オプションは引数の最後に配置する(引数の数が不明なため)
  if tkey in args:
    aidx = args.index(tkey)
    for i in range( aidx+1, len(args) ):
      tlist.append(args[i])
    del args[aidx:len(args)]
  print(tlist)
  arg_num = 4
  arg_num = (arg_num + 2) if hkey in args else arg_num
  arg_num = (arg_num + 1) if dkey in args else arg_num
  if arg_num <= len(args):
    if hkey in args:
      aidx = args.index(hkey)
      hval = int(args[aidx+1])
      del args[aidx:aidx+2]
    if dkey in args:
      aidx = args.index(dkey)
      dval = '\t'
      del args[aidx]
    if os.path.isfile(args[1]):
      hlist = []
      for i in range( 3, len(args) ):
        hlist.append(args[i])
      csv_to_sql(args[1], args[2], dval, hval, hlist, tlist)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {args[0]} [-h line_num] [-t] input_csv output_db table_name [col1 col2 col3] [-d type1 type2 type3]')
```

## References

* [csv RFC4180 (IETF Tools)](https://tools.ietf.org/pdf/rfc4180.pdf)
* [sqlite3 (docs.python.org)](https://docs.python.org/ja/3/library/sqlite3.html)
* [csv (docs.python.org)](https://docs.python.org/ja/3/library/csv.html)
* [Datatypes In SQLite (www.sqlite.org)](https://www.sqlite.org/datatype3.html)

