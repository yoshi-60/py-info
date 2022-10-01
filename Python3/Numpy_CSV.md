# 【Python】CSVファイルのデータをNumpyのndarrayに読み込む
updated at 2022/10/01

## 実行内容
CSVファイルのデータをNumpyの**ndarray**に読み込みグラフ出力する。

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
    print(f'No Header{pscale}')
  else :
    print(f'Header skip: {skiprow}{pscale}')

  ndin = np.loadtxt(fcsv, delimiter=',', skiprows=skiprow)
  dat_size = ndin.shape[0]
  print(f'Data size: {dat_size}')
  if tscale:
    ndat = ndin[:,1:]
    ntim = ndin[:,0]
    print(f'Time_min: {ntim.min(axis=0)} , Time_max: {ntim.max(axis=0)}')
  else:
    ndat = ndin
    ntim = np.arange(0,dat_size)
  print(f'Value_min: {ndat.min(axis=0)} , Value_max: {ndat.max(axis=0)}')
  
  fname = os.path.basename(fcsv)
  plt.plot(ntim,ndat)
  plt.title(fname)
  plt.grid(axis='both')
  plt.ylabel('Data_Value')
  if tscale:
    plt.xlabel('Time')
  else:
    plt.xlabel('Sample')
  plt.show()
  
if __name__ == '__main__':
  args = sys.argv
  arg_num = 2
  optlist = {'-r': 2, '-x': 1}     # オプションと必要な引数の数（オプション自身も含む）
  optval  = { 'r': 1,  'x': True}  # デフォルト値
  optflag = { 'x': False}          # フラグオプションの設定値
  # 必要な引数の数を計算
  for opkey in optlist.keys():
    if opkey in args:
      arg_num = (arg_num + optlist[opkey])
  # 引数の取り出しと実行
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
$ csv_to_numpy.py wave_square.csv
Input_csv: wave_square.csv
Header skip: 1
Data size: 3334
Time_min: 0.0 , Time_max: 0.003333
Value_min: [0.34348246] , Value_max: [1.08635933]
```

<img width="480" alt="square_wave" src="https://user-images.githubusercontent.com/49278963/193401163-6466eea7-da7f-4fe2-9e4b-2e07491185a7.png">

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

## References

* [Numpy Reference (nympy.org)](https://numpy.org/doc/stable/reference/index.html#reference)
