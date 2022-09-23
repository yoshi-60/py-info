# 【Python】CSVファイルの波形をグラフ出力する
updated at 2022/9/23

## 実行内容
CSVファイルをグラフ出力する。

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plt_wave(fcsv):
  print(f'Input_csv: {fcsv}')

  f_name = os.path.basename(fcsv)
  df= pd.read_csv(fcsv,header=0)
  sample_num= len(df)
  col_names= df.columns.values
  col_max= df.max(axis=0).values.tolist()
  col_min= df.min(axis=0).values.tolist()
  dt = df.iat[1,0] - df.iat[0,0]
  clk_freq= 1/dt
  start_time = col_min[0]
  stop_time  = col_max[0]
  wave_max   = col_max[1]
  wave_min   = col_min[1]

  print(f'Columns: {col_names[0]} , {col_names[1]}') 
  print(f'Sample Freq.: {clk_freq} , Delta_time: {dt} , Range: {start_time} , {stop_time} , Count: {sample_num}') 
  print(f'Wave_max: {wave_max} , min: {wave_min}') 

  df.plot(x=col_names[0], y=col_names[1], title=f_name, grid=True, legend=False)
  plt.xlabel(col_names[0])
  plt.ylabel(col_names[1])
  plt.show()

  # Numpy fft
  x = df.iloc[:,1].to_numpy()
  F = np.fft.fft(x)
  freq = np.fft.fftfreq(sample_num, d=dt)
  F = F / (sample_num / 2)
  Amp = np.abs(F)
  plt.plot(freq[:sample_num//2],Amp[:sample_num//2])
  plt.title(f_name)
  plt.xlabel('Frequency')
  plt.ylabel('Amplitude')
  plt.grid(axis='both')
  plt.show()

if __name__ == '__main__':
  args = sys.argv
  if 2 <= len(args):
    if os.path.isfile(args[1]):
      plt_wave(args[1])
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {args[0]} input_csv')
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

