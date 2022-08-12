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
  return()

if __name__ == '__main__':
  args = sys.argv
  if 4 <= len(args):
    if args[1].isfile():
      hlist = []
      for i in range( 3, len(args)-1 ):
        hlist.append(args[i])
      csv_to_sql(args[1], args[2], hlist)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:`)
    print(f'  {args[0]} input_csv output_db table_name [col1 col2 col3]')
```

## Referebce
