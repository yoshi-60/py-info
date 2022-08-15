# 【Python】SQLiteの テーブル・カラム情報を取得する。

## 実行内容
SQLiteのデータベースファイルに含まれる、テーブル名、カラム名等の情報を取得する。

※ PRAGMA Statements を使う方法もあるが、バージョンに制限がありそうなので、今回は使っていない。

## Pythonコード

```Python
#!/usr/bin/env python3
import sys
import os
import sqlite3

def print_sql_info(fsql,tlist):
  print(fsql)

  conn = sqlite3.connect(fsql)
  cur = conn.cursor()
  
  # テーブル名取得
  table_names = []
  exec_str = "SELECT * FROM sqlite_master where type='table' ;"
  cur.execute( exec_str )
  for row in cur.fetchall():
    #print(row)
    table_names.append(row[2])

  # レコード数、カラム名、データ型 取得
  table_infos = []
  for table_name in table_names:
    # レコード数取得
    exec_str = "SELECT count(*) FROM " + table_name + " ;"
    cur.execute( exec_str )
    record = cur.fetchall()
    #print(record)
    record_max = record[0][0]
    exec_str = "SELECT * FROM " + table_name + " LIMIT 1;"
    cur.execute( exec_str )
    # データ(1行目)を表示
    for row in cur:
      print(row)
    # カラム名取得
    desc = cur.description
    table_info = [ table_name , record_max ]
    col_names = []
    for col in desc:
      #print(col[0])
      # データ型取得
      exec_str = "SELECT typeof(" + col[0] + ") FROM " + table_name + " LIMIT 1;"
      cur.execute( exec_str )
      type_list = cur.fetchall()
      #print(type_list[0][0])
      col_names.append([col[0],type_list[0][0]])

    table_info.append(col_names)
    table_infos.append(table_info)
 
  cur.close()
  conn.close()
  
  for table_info in table_infos:
    print(f'table_name: {table_info[0]}, Record_num: {table_info[1]}, Column_name: ', table_info[2])
  
  return()

if __name__ == '__main__':
  args = sys.argv
  if 2 <= len(args):
    if os.path.isfile(args[1]):
      tlist = []
      for i in range( 2, len(args) ):
        tlist.append(args[i])
      print_sql_info(args[1], tlist)
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    #print(f'  {args[0]} input_db [table_name1 ...]')
    print(f'  {args[0]} input_db'
```

## Reference

* [The Schema Table (www.sqlite.org)](https://www.sqlite.org/schematab.html#introduction)
* [PRAGMA Statements (www.sqlite.org)](https://www.sqlite.org/pragma.html)
