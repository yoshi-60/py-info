# 【Python】Wordのテーブルの内容をCSVファイルに出力する
updated at 2024/2/04

## 実行内容
Word(*.docx)内のテーブルのデータを CSVファイルに出力する。

## Pythonのコード

```Python
# word table to csv
from docx import Document
import csv

# 対象のワードファイルのPATH
word_path = r"C:\Users\Public\Documents\InputFile.docx"
csv_path  = r"C:\Users\Public\Documents\OutputFile.csv"

# ワードファイルの読み込み
doc = Document(word_path)

# テーブルデータを取得
tbl_data = []
for tbl_num,myTbl in enumerate(doc.tables):
  print(f'Table_No{tbl_num+1}')
  tbl_data.append(['Table_No',tbl_num+1])
  for row_cnt, row in enumerate(myTbl.rows):
    row_data = [ row_cnt+1 ]
    for cell in row.cells:
      row_data.append(cell.text)
    print(row_data)
    tbl_data.append(row_data)

# データをcsvファイルに出力
with open(csv_path, 'w') as csvf:
  writer = csv.writer(csvf)
  writer.writerows(tbl_data)
```

## References

* [python-docx](https://python-docx.readthedocs.io/en/latest/#python-docx)
* [csv RFC4180 (IETF Tools)](https://tools.ietf.org/pdf/rfc4180.pdf)
* [csv (docs.python.org)](https://docs.python.org/ja/3/library/csv.html)
