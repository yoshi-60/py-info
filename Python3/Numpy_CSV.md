# 【Python】CSVファイルのデータをNumpyに読み込む
updated at 2022/10/01

## 実行内容
CSVファイルのデータをNumpyの ndarrayに読み込みグラフ出力する。

1. ヘッダの有無, X軸データの有無を指定できるようにする。

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def csv_to_np(fcsv):
  print(f'Input_csv: {fcsv}')

```

### 画面出力

```Shell
$ plot_wave.py wave_square.csv
Input_csv: wave_square.csv
Columns: Time , Wave
Sample Freq.: 1000000.0 , Delta_time: 1e-06 , Range: 0.0 , 0.003333 , Count: 3334
Wave_max: 1.0863593349859093 , min: 0.3434824580771949
```

<img width="480" alt="square_wave" src="https://user-images.githubusercontent.com/49278963/191883247-0f4b4d37-481c-4295-b51b-966113837b66.png">

```Shell
$ head wave_square.csv
Time,Wave
0.0,0.7149202570000001
1e-06,0.7186900918733848
2e-06,0.7224594847445748
3e-06,0.726227993703401
4e-06,0.7299951770237249
4.9999999999999996e-06,0.7337605932553961
6e-06,0.7375238013161444
7e-06,0.74128436058338
8e-06,0.7450418309858837
```
