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
  
  # テーブル作成
  exec_str = "SELECT * FROM sqlite_master where type='table'"
  cur.execute( exec_str )
  for row in cur.fetchall():
    print(row)

  cur.close()
  conn.close()
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
    print(f'  {args[0]} input_db [table_name1 ...]')
```

## Reference

* [PRAGMA Statements (www.sqlite.org)](https://www.sqlite.org/pragma.html)
