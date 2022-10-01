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

def csv_to_np(fcsv, skiprow, tscale):
  print(f'Input_csv: {fcsv}')
  if tscale:
    pscale = ''
  else:
    pscale = ' , No X-axis'
  if skiprow == 0:
    print(f'  No Header{pscale}')
  else :
    print(f'  Header skip: {skiprow}{pscale}')

  ndin = np.loadtxt(fcsv, delimiter=',', skiprows=skiprow)
  dat_size = ndin.shape[0]
  print(f'Data size: {dat_size}')
  if tscale:
    ndat = ndin[:,1:]
    ntim = ndin[:,0]
  else:
    ndat = ndin
    ntim = np.arange(0,dat_size)

  print(type(ndin))
  print(ndin.shape, ndin.dtype)
  print(type(ndat),type(ntim))
  print(ndat.shape, ndat.dtype)
  print(ntim.shape, ntim.dtype)

if __name__ == '__main__':
  args = sys.argv
  arg_num = 2
  optlist = {'-r': 2, '-x': 1}     # オプションと必要な引数の数（オプション自身も含む）
  optval  = { 'r': 1,  'x': True}  # デフォルト値
  optflag = { 'x': False}          # フラグオプションの設定値
  
  for opkey in optlist.keys():
    if opkey in args:
      arg_num = (arg_num + optlist[opkey])

  if arg_num <= len(args):
    for opkey in optlist.keys():
      if opkey in args:
        aidx = args.index(opkey)
        if optlist[opkey] == 1:
          optval[opkey[1:]] = optflag[opkey[1:]]
          del args[aidx]
        elif optlist[opkey] == 2:
          optval[opkey[1:]] = args[aidx+1]
          del args[aidx:aidx+2]
        else:
          optval[opkey[1:]] = args[aidx+1:aidx+optlist[opkey]]
          del args[aidx:aidx+optlist[opkey]]
    if os.path.isfile(args[1]):
      csv_to_np(args[1], int(optval['r']), optval['x'])
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {args[0]} input_csv [-r 0] [-x]')
    print(f'             -r skiprow : 0 = No header , 1 = Header skip, -x : No X-axis data')
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
