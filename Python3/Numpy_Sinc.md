# 【Python】CSVファイルのデータにNumpyでSincフィルタをかける
updated at 2022/10/16

## 実行内容
CSVファイルのデータをNumpyに読み込み、Sincフィルタをかけてグラフ出力する。

1. 入力データは⊿Σ変調のビットストリーム(0/1)を想定。
2. ヘッダの有無, X軸データの有無を指定できるようにする。
3. Sincフィルタの次数を1～4の間で選択できるようにする。

※ 積算時の Numpyのオーバーフローを考慮していないので、パターン長に制限有り

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def sinc_plot(fcsv,deci,istart, sincsel, stepplt, skiprow, tscale):
  print(f'Input_csv: {fcsv}')
  if tscale:
    pscale = ''
  else:
    pscale = ' , No X-axis'
  if skiprow == 0:
    print(f'No Header{pscale}')
  else :
    print(f'Header skip: {skiprow}{pscale}')

  # Sinc Order
  if '1' in sincsel:
    sinc1plt = True
  else:
    sinc1plt = False
  if '2' in sincsel:
    sinc2plt = True
  else:
    sinc2plt = False
  if '3' in sincsel:
    sinc3plt = True
  else:
    sinc3plt = False
  if '4' in sincsel:
    sinc4plt = True
  else:
    sinc4plt = False

  nin = np.loadtxt(fcsv, delimiter=',', skiprows=skiprow)
  nline = nin.shape[0]
  print(f'Lines: {nline}, Decimation: {deci}')

  # Add Initial Zero
  nzero = np.zeros_like(nin[0])
  ninz = np.insert(nin,0,nzero,axis=0)

  # separate ndarray
  if tscale:
    ndim = ninz[:,1:].astype('int64')
    ntim = nin[:,0]
    print(f'Time_min: {nin[:,0].min(axis=0)} , Time_max: {nin[:,0].max(axis=0)}')
  else:
    ndim = ninz.astype('int64')
    ntim = np.arange(0,nline)
    
  # Integration
  ncum1 = np.cumsum(ndim,  axis=0)
  ncum2 = np.cumsum(ncum1, axis=0)
  ncum3 = np.cumsum(ncum2, axis=0)
  ncum4 = np.cumsum(ncum3, axis=0)

  # Decimation
  ndeci1 = ncum1[istart::deci]
  ndeci2 = ncum2[istart::deci]
  ndeci3 = ncum3[istart::deci]
  ndeci4 = ncum4[istart::deci]

  # Differential
  ndiff1 = np.diff(ndeci1, n=1, axis=0)
  ndiff2 = np.diff(ndeci2, n=2, axis=0)
  ndiff3 = np.diff(ndeci3, n=3, axis=0)
  ndiff4 = np.diff(ndeci4, n=4, axis=0)
  print(f'Plot Points sinc1: {ndiff1.shape[0]} , sinc2: {ndiff2.shape[0]} , sinc3: {ndiff3.shape[0]}, sinc4: {ndiff4.shape[0]}')

  # Plot X-axis
  ntimp = np.insert(ntim,0,0)
  nx1 = ntimp[istart+deci*1::deci]
  nx2 = ntimp[istart+deci*2::deci]
  nx3 = ntimp[istart+deci*3::deci]
  nx4 = ntimp[istart+deci*4::deci]

  # Plot
  plt.figure(figsize=(12, 5))
  if stepplt :
    if sinc1plt:
      plt.step(nx1,ndiff1/deci,    where='post',label='sinc1')
    if sinc2plt:
      plt.step(nx2,ndiff2/deci**2, where='post',label='sinc2')
    if sinc3plt:
      plt.step(nx3,ndiff3/deci**3, where='post',label='sinc3')
    if sinc4plt:
      plt.step(nx4,ndiff4/deci**4, where='post',label='sinc4')
  else:
    if sinc1plt:
      plt.plot(nx1,ndiff1/deci,    label='sinc1')
    if sinc2plt:
      plt.plot(nx2,ndiff2/deci**2, label='sinc2')
    if sinc3plt:
      plt.plot(nx3,ndiff3/deci**3, label='sinc3')
    if sinc4plt:
      plt.plot(nx4,ndiff4/deci**4, label='sinc4')

  plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
  if tscale:
    plt.xlabel('Time')
  else:
    plt.xlabel('Sample Count')
  plt.ylabel('Normalized Amplitude')
  plt.grid(axis='both')
  plt.tight_layout()
  plt.show()

if __name__ == '__main__':
  args = sys.argv
  arg_num = 2
  optlist = {'-d': 2, '-r': 2, '-t': 2, '-s': 2,    '-p': 1, '-x': 1}      # option 
  optval  = { 'd': 32, 'r': 1,  't': 0,  's': '1234', 'p': True,'x': True}  # default
  optflag = { 'p': False, 'x': False} # flag settion value
  # arg numbers
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
      sinc_plot(args[1], int(optval['d']), int(optval['t']), optval['s'], optval['p'], int(optval['r']), optval['x'])
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {os.path.basename(args[0])} input_csv [-d integer] [-s 14] [-p] [-r 1] [-x]')
    print(f'        -d integer: decimation number (default 32)')
    print(f'        -p : No step plot')
    print(f'        -s sinc: sinc order')
    print(f'        -r skiprow: 1 = Header skip')
    print(f'        -x : No X-axis data')
```

### 画面出力

```Shell
$ sinc_plot.py bs_square.csv -d 16 -s 14
Input_csv: bs_square.csv
Header skip: 1
Lines: 3334, Decimation: 16
Time_min: 0.0 , Time_max: 0.003333
Plot Points sinc1: 208 , sinc2: 207 , sinc3: 206, sinc4: 205
```

<img width="800" alt="square_wave" src="https://user-images.githubusercontent.com/49278963/196025662-482ae47e-cccf-4104-9326-a7931bab9c68.png">

```Shell
$ head bs_square.csv
Time,Bit-stream
0.0,1
1e-06,0
2e-06,0
3e-06,0
4e-06,1
4.9999999999999996e-06,1
6e-06,1
7e-06,0
8e-06,0
```

## References

* [Numpy Reference (numpy.org)](https://numpy.org/doc/stable/reference/index.html#reference)
