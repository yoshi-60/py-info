# 【Python】CSVファイルをSQLiteにインポートする

## 実行内容
CSVファイルからSQLite3のデータベースを作成する。
1. CSVファイル名とSQLiteのデータベースファイル名は引数として与える。
2. CSVファイルの1行目はヘッダとして、SQLiteのカラム名に設定する。
3. CSVファイルのヘッダを使用しないオプションも可能とする。
4. SQLiteのインデックスは1カラム目に新規に追加する。

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import csv
import sqlite3

def csv_to_sql(fcsv,fsql,hlist):
  print(fcsv,fsql)
  # csvデータを2次元配列 rowsに読み込む
  rows = []
  rnum = 0
  cnum_max = 0
  with open(fcsv, 'r') as f: 
    read_csv = csv.reader(f)
    row0 = next(read_csv)
    for row in read_csv:
      rows.append(row)
      cnum_max = max(len(row),cnum_max)
      rnum = rnum + 1
  print(f'Recore: {rnum} , Field: {cnum_max}')

  # SQLiteのテーブル作成用テキスト作成
  tname = hlist.pop(0)
  header_txt = "id_sql INTEGER PRIMARY KEY"
  cnum = 0
  if len(hlist) > 0:
    for col in hlist:
      header_txt = header_txt + ", " + col + " TEXT"
      cnum = cnum + 1
    insert_txt = ",".join(hlist)
  else:
    for col in row0:
      header_txt = header_txt + ", " + col + " TEXT"
      cnum = cnum + 1
    insert_txt = ",".join(row0)

  # headerの数が不足していた時の処置
  if cnum < cnum_max:
    for col in range(cnum, cnum_max)
      header_txt = header_txt + ", col_" + str(col+1) + " TEXT"
      insert_txt = insert_txt + ", col_" + str(col+1)

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
  exec_str = "INSER INTO " + tname + " (" + insert_txt + ") VALUES (" + value_txt + ")"
  print(exec_str)
  cur.executemany( exec_str , rows)
  
  conn.commit()
  cur.close()
  conn.close()
  return(rnum,cnum_max)

if __name__ == '__main__':
  args = sys.argv
  if 4 <= len(args):
    if args[1].isfile():
      hlist = []
      for i in range( 3, len(args) ):
        hlist.append(args[i])
      csv_to_sql(args[1], args[2], hlist)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:`)
    print(f'  {args[0]} input_csv output_db table_name [col1 col2 col3]')
```

## Reference
* [sqlite3 (docs.python.org](https://docs.python.org/ja/3/library/sqlite3.html)
* [csv (docs.python.org)](https://docs.python.org/ja/3/library/csv.html)
