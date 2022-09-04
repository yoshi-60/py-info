# 【Python】Excelの書式を設定する
updated at 2022/9/04

## 実行内容
Excelファイルのセルの書式(フォント、フィル、枠線等)を設定する。

## Pythonのコード

### フォント設定

```Python
from openpyxl import load_workbook
from openpyxl.styles.fonts import Font

wb_name = '/home/username/sample.xlsx'
ws_name = 'Sheet1'
cell_range = 'B2:E4'

# ブックを開く
wb = load_workbook('/home/username/sample.xlsx')

# シートを取得
ws = wb[ws_name]

# フォントを設定
font = Font(name='BIZ UDPGothic', size=10, color='ff0000ff', 
           strike=False, bold=True, italic=False, underline='single')

# セルに設定
for row in ws[cell_range]:
  for cell in row:
    cell.font = font

# 保存する
wb.save(wb_name)
```

### セル幅とセル高を設定する

```Python
from openpyxl import load_workbook
from openpyxl.utils.cell import range_boundaries, get_column_letter

wb_name = '/home/username/sample.xlsx'
ws_name = 'Sheet1'
cell_range = 'B2:E4'

# ブックを開く
wb = load_workbook('/home/username/sample.xlsx')

# シートを取得
ws = wb[ws_name]

# セル幅設定
cell_boudary = range_boundaries(cell_range)
for c in range(cell_boudary[1],cell_boudary[3]+1)
  ws.column_dimensions[get_col_letter(c)].width = 12

# セル高設定
for r in range(cell_boudary[0],cell_boudary[2]+1)
  ws.row_dimensions[r].height = 28

# 保存する
wb.save(wb_name)
```

### フィル設定

```Python
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

wb_name = '/home/username/sample.xlsx'
ws_name = 'Sheet1'
cell_range = 'B2:E4'

# ブックを開く
wb = load_workbook('/home/username/sample.xlsx')

# シートを取得
ws = wb[ws_name]

# 背景色を変更
fill = PatternFill(patternType='solid', fgColor='ffff0000', bgColor='ffff0000')

# セルに設定
for row in ws[cell_range]:
  for cell in row:
    cell.fill = fill

# 保存する
wb.save(wb_name)
```

### 罫線設定

```Python
from openpyxl import load_workbook
from openpyxl.styles import Border, Side

wb_name = '/home/username/sample.xlsx'
ws_name = 'Sheet1'
cell_range = 'B2:E4'

# ブックを開く
wb = load_workbook('/home/username/sample.xlsx')

# シートを取得
ws = wb[ws_name]

# 罫線を設定
side_l = Side(style = 'thick', color='000000')
side_r = Side(style = 'thick', color='000000')
side_t = Side(style = 'thick', color='000000')
side_b = Side(style = 'thick', color='000000')

# セルに設定
for row in ws[cell_range]:
  for cell in row:
    cell.border = Border(left = side_l, right = side_r, top = side_t, bottom = side_b)

# 保存する
wb.save(wb_name)
```
 
## References

* [utils.cell (openpyxl.readthedocs.io)](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.utils.cell.html)
* [Font (openpyxl.readthedocs.io)](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.fonts.html#openpyxl.styles.fonts.Font)
* [PatternFill (openpyxl.readthedocs.io)](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.fills.html#openpyxl.styles.fills.PatternFill)
* [Side (openpyxl.readthedocs.io)](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.borders.html#openpyxl.styles.borders.Side)
* [Border (openpyxl.readthedocs.io)](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.borders.html#openpyxl.styles.borders.Border)
* 
