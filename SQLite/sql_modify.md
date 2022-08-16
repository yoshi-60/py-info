# 【Python】複数のSQLiteファイルの操作結果を別のSQLiteファイルに出力する。

## 実行内容
複数のSQLiteファイルにあるテーブルを参照して操作(抽出、結合等)を行い。  
結果を別のSQLiteファイルに出力する。


## Pythonのコード
操作用テキストファイルの例

```SQL
# Comment
CREATE TABLE new_table (id_sql INTEGER, col_1 TEXT, col_2 TEXT, col_3 TEXT) ;
INSERT INTO new_table (id_sql, col_1, col_2) SELECT id_sql, col_1, col_2 FROM data_1.table2021 ;
INSERT INTO new_table (col_3) SELECT col_2 FROM data_2.table2022 ;
ALTER  TABLE new_table ADD COLUMN add_col TEXT ;
# END
```

Pythonコード

```Python
#!/usr/bin/env python3
import sys
import os
import sqlite3

def print_usage(arg0):
  print(f'Usage:')
  print(f'  {arg0} output_db -f command_file [input_db1 input_db2 ...]')
  return()

def sql_modify(fsqlo, fname, db_list):
  print(fsqlo, fname, db_list)

  # 出力用データベース作成
  conn = sqlite3.connect(fsqlo)
  cur = conn.cursor()

  # 入力側データベースに接続
  db_num = 0
  for dname in db_list:
    db_num = db_num + 1
    db_str = "data_" + str(db_num)
    exec_str = "ATTACH DATABASE '" + dname + "' as " + db_str + " ;"
    print(exec_str)
    cur.execute( exec_str )

  # 操作用文字列取得
  # 先頭文字が "#" の行を除外する
  exec_list = []
  with open(fname, 'r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
      if row.find('#') != 0:
        exec_list.append(row.rstrip('\n'))

  # 操作実行
  exec_num = 0
  for exec_str in exec_list:
    exec_num = exec_num + 1
    print(f'Execute: {exec_num}')
    print(exec_str)
    res = cur.execute( exec_str )
    print(f'Result:  {exec_num}')
    print(res.fetchone())
  
  # データベースクローズ
  conn.commit()
  cur.close()
  conn.close()
  return()

if __name__ == '__main__':
  args = sys.argv
  fkey = '-f'
  db_list = []
  db_nf = 0
  if 4 <= len(args):
    if fkey in args:
      aidx = args.index(fkey)
      fname = args[aidx+1]
      del args[aidx:aidx+2]
      if os.path.isfile(fname):
        for i in range(2, len(args) ):
          if os.path.isfile(args[i]):
            db_list.append(args[i])
          else:
            db_nf = db_nf + 1
            print(f'File {args[i]} Not Found!')
            break
        if db_nf == 0:
          sql_modify(args[1], fname, db_list)
      else:
        print(f'File {fname} Not Found!')
    else:
      print_usage(args[0])
  else:
    print_usage(args[0])
```

## References

* [DB-API 2.0 interface for SQLite databases (docs.python.org)](https://docs.python.org/ja/3/library/sqlite3.html)
