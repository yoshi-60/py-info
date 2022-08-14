# 【Python】SQLiteで別ファイルにテーブルのコピーを作成する

## 実行内容
SQLiteのファイル(データベース)内のテーブルを別ファイル（新規作成）にコピーする。

## Pythonコード

```Python
#!/usr/bin/env python3
import sys
import os
import sqlite3

def sql_tbl_cp(fsqli, fsqlo, tname):
  print(fsqli, fsqlo, tname)

  # 出力用データベース作成
  conn = sqlite3.connect(fsqlo)
  cur = conn.cursor()
  # 入力側データベースに接続
  exec_str = "ATTACH DATABASE '" + fsqli + "' as data1 ;"
  print(exec_str)
  cur.execute( exec_str )
  # テーブルのコピー作成
  exec_str = "CREATE TABLE " + tname + " AS SELECT * FROM data1." + tname + " ;"
  print(exec_str)
  cur.execute( exec_str )

  conn.commit()
  cur.close()
  conn.close()
  return()

if __name__ == '__main__':
  args = sys.argv
  if 4 <= len(args):
    if os.path.isfile(args[1]):
      sql_tbl_cp(args[1], args[2], args[3])
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {args[0]} input_db output_db table_name')
```
