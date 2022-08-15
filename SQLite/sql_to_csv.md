# 【Python】SQLiteからCSVファイルに出力する
updated at 2022/8/15

## 実行内容
SQLiteのファイル（データベース）のテーブルを CSVファイルに出力する。

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import csv
import sqlite3

def sql_to_csv(fsql,fcsv,tlist):
  print(fsql,fcsv,tlist)
  
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
  with open(fcsv, 'w', newline='', encoding='utf-8') as f: 
    write_csv = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    # headerの書き込み
    row0 = [row[0] for row in cur.description]
    write_csv.writerow(row0)
    # データの書き込み
    rows = cur.fetchall()
    write_csv.writerows(rows)

  row1 = rows[0]
  print(f'Table: {tname}, Record: {record}')
  print(row0)
  print(row1)
    
  return(record)

if __name__ == '__main__':
  args = sys.argv
  if 3 <= len(args):
    if os.path.isfile(args[1]):
      tlist = []
      for i in range( 3, len(args) ):
        tlist.append(args[i])
      sql_to_csv(args[1], args[2], tlist)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {args[0]} input_db [table_name]')
```

## References

* [CSV File Reading and Writing (docs.python.org)](https://docs.python.org/ja/3/library/csv.html)
