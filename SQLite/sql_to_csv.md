# 【Python】SQLiteからCSVファイルに出力する
updated at 2022/8/16

## 実行内容
SQLiteのファイル（データベース）のテーブルを CSVファイルに出力する。

1. CSVファイル名とSQLiteのデータベースファイル名は引数として与える。
2. テーブル名も引数として与えるが、指定しない場合は最初のテーブルを出力する。
3. CSVファイルにヘッダを出力しないオプションも可能とする。（-h オプション）
4. TSVファイルの出力にも対応する。（-t オプション）
5. CSVファイルのクオート文字（'"'）を変更できるようにする。（-c オプション）
6. CSVファイルのクオート方法を指定できるようにする。（-q オプション）

コマンド入力例

```Shell
# オプション無し
python3 sql_to_csv.py infile.db outfile.csv

# オプション設定
python3 sql_to_csv.py infile.db outfile.tsv -t -h -c "'" -q 1 table_1
```

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import csv
import sqlite3

def sql_to_csv(fsql,fcsv,tlist, dval, hval, cval, qval):
  print(fsql,fcsv,tlist)
  # sqliteデータをcsvに書き込む
  #   tlist[0] テーブル名指定、空の場合は最初のテーブル
  #   dval に delimiterを設定する
  #   hval = 0 の場合header行を出力しない
  #   cval に quotecharを指定する
  #   qval に quoting パラメータを指定する（0/1/2/3）

  conn = sqlite3.connect(fsql)
  cur = conn.cursor()
  
  # テーブル名取得
  table_names = []
  exec_str = "SELECT * FROM sqlite_master where type='table' ;"
  cur.execute( exec_str )
  for row in cur.fetchall():
    table_names.append(row[2])
  if len(table_names) < 1:
    print(f'No table in {fsql} !!')
    return(0)
  elif len(tlist) > 0:
    if tlist[0] in table_names:
      tname = tlist[0]
    else:
      print(f'Table {tlist[0]} Not Found in {fsql} !!')
      return(0)
  else:
    tname = table_names[0]
  
  # レコード数取得
  exec_str = "SELECT count(*) FROM " + tname + " ;"
  cur.execute( exec_str )
  record_list = cur.fetchall()
  record = record_list[0][0]

  # テーブルのデータ取得
  exec_str = "SELECT * FROM " + tname + " ;"
  cur.execute( exec_str )
  
  # CSVファイルへの書き込み
  quote_num, quote_str = csv_quoting(qval)
  with open(fcsv, 'w', newline='', encoding='utf-8') as f: 
    write_csv = csv.writer(f, delimiter=dval, quotechar=cval, quoting=quote_num)
    # headerの書き込み
    row0 = [row[0] for row in cur.description]
    if hval != 0:
      write_csv.writerow(row0)
      header_str = "Output   "
    else:
      header_str = "No_output"
    # データの書き込み
    rows = cur.fetchall()
    write_csv.writerows(rows)

  row1 = rows[0]
  print(f'Table: {tname}, Record: {record}, Header: {header_str}, Quote_character: {cval} , Quoting: {quote_str}')
  print(fsql)
  print(row0)
  print(row1)
  print(fcsv)
  with open(fcsv, mode='r', encoding='utf-8') as f:
    for i in range(hval+1):
      rline = f.readline()
      print(rline.rstrip('\n'))
    
  return(record)

def csv_quoting(qval):
  if qval == 1:
    quote_num = csv.QUOTE_ALL
    quote_str = "QUOTE_ALL"
  elif qval == 2:
    quote_num = csv.QUOTE_NONNUMERIC
    quote_str = "QUOTE_NONNUMERIC"
  elif qval == 3:
    quote_num = csv.QUOTE_NONE
    quote_str = "QUOTE_NONE"
  else:
    quote_num = csv.QUOTE_MINIMAL
    quote_str = "QUOTE_MINIMAL"

  return quote_num ,quote_str

if __name__ == '__main__':
  args = sys.argv
  dkey = '-t'
  dval = ','
  hkey = '-h'
  hval = 1
  ckey = '-c'
  cval = '"'
  qkey = '-q'
  qval = 0
  arg_num = 3
  arg_num = (arg_num + 1) if hkey in args else arg_num
  arg_num = (arg_num + 1) if dkey in args else arg_num
  arg_num = (arg_num + 2) if ckey in args else arg_num
  arg_num = (arg_num + 2) if qkey in args else arg_num
  if arg_num <= len(args):
    if dkey in args:
      aidx = args.index(dkey)
      dval = '\t'
      del args[aidx]
    if hkey in args:
      aidx = args.index(hkey)
      hval = 0
      del args[aidx]
    if ckey in args:
      aidx = args.index(ckey)
      cval = args[aidx+1]
      del args[aidx:aidx+2]
    if qkey in args:
      aidx = args.index(qkey)
      qval = int(args[aidx+1])
      del args[aidx:aidx+2]
    if os.path.isfile(args[1]):
      tlist = []
      for i in range( 3, len(args) ):
        tlist.append(args[i])
      sql_to_csv(args[1], args[2], tlist, dval, hval, cval, qval)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {args[0]} input_db output_csv [-t] [-c quotechar] [-q quoting_num] [table_name]')
```

## References

* [CSV File Reading and Writing (docs.python.org)](https://docs.python.org/ja/3/library/csv.html)
* [Built-in Aggregate Functions (www.sqlite.org)](https://www.sqlite.org/lang_aggfunc.html#descriptions_of_built_in_aggregate_functions)
