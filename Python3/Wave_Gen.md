# 【Python】Sin波を生成してSVファイルに出力する
updated at 2022/9/23

## 実行内容
Sin波の時刻と振幅を記載したCSVファイルを出力する。

1. 複数の波形の重ね合わせができるようにする。
2. 画面上にもグラフを出力する。
3. 波形のパラメータを実行時に指定する。
4. ⊿Σ変調の結果も出力も出力する（未実装）。

## Pythonのコード

```Python
#!/usr/bin/env python3
import sys
import os
import yaml
import numpy as np
import pandas as pd

def gen_wave(fyml):
  print(f'Input_Yaml: {fyml}')
  # Yamlファイルからパラメータを読み込む
  with open( fyml, 'r') as yml:
    config = yaml.safe_load(yml)

　# パラメータの取り出し
  clk_freq = float(config['clock']['frequency'])
  sample_num = int(config['clock']['samples'])
  start_time = float(config['clock'].get('start',0.0))
  csv_file = config['output'].get('wavefile',"output_tmp.csv")
  dsm_file = config['output'].get('dsmfile')
  plot_out = config['output'].get('plot', False)
  dt = 1/clk_freq
  stop_time= start_time+ (sample_num - 1) * dt
  stop_arange = start_time+ (sample_num - 0.5) * dt

  print(f'Output_Wave: {csv_file}')
  if dsm_file is None:
    print(f'Output_DSM: None')
  else:
    print(f'Output_DSM: {dsm_file}')

  print(f'Sample Freq.: {clk_freq} , Delta_time: {dt} , Range: {start_time} , {stop_time} , Count: {sample_num}') 
  
　# 波形生成用パラメータの取り出し
  wave_func= []
  wave_amp= []
  wave_offset= []
  wave_freq= []

  for i,j in enumerate(config['waves']) :
    wave_func.append(j['function'])
    wave_offset.append(float(j['offset']))
    wave_amp.append(float(j['amplitude']))
    wave_freq.append(float(j['frequency']))
    print(f'wave {i} : {wave_func[i]} , freq.: {wave_freq[i]} , offset: {wave_offset[i]} , amplitude: {wave_amp[i]}')
  
　# 波形の生成（Numpy使用）
  x = np.arange(start_time, stop_arange, dt)
  w = np.zeros_like(x)
  for i,j in enumerate(wave_func):
    if j == 'sin':
      y = wave_amp[i] * np.sin(2*np.pi*x*wave_freq[i]) + wave_offset[i]
    elif j == 'cos':
      y = wave_amp[i] * np.cos(2*np.pi*x*wave_freq[i]) + wave_offset[i]
    else:
      y = np.zeros_like(x)
    w = w + y

  wave_max = np.max(w)
  wave_min = np.min(w)
  print(f'Wave_max: {wave_max} , min: {wave_min}') 
  
　# 波形のCSV出力（Pandas使用）
  df = pd.DataFrame(np.stack([x,w],1), columns=['Time', 'Wave'])
  df.to_csv(csv_file, header=True, index=False)

　# 波形の画面出力
  if plot_out:
    import matplotlib.pyplot as plt
    df.plot(x='Time', y='Wave')
    plt.show()

if __name__ == '__main__':
  args = sys.argv
  if 2 <= len(args):
    if os.path.isfile(args[1]):
      gen_wave(args[1])
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {args[0]} input_yaml')
```

### Yamlファイル

```Yaml
# Parameter Yaml
clock:
  frequency: 1E+6
  samples: 3334
  start: 0.0
waves:
  - function: "sin"
    offset: 0.4
    amplitude: 0.4
    frequency: 300
  - function: "sin"
    offset: 0.133333
    amplitude: 0.133333
    frequency: 900
  - function: "sin"
    offset: 0.08
    amplitude: 0.08
    frequency: 1500
  - function: "sin"
    offset: 0.057142857
    amplitude: 0.057142857
    frequency: 2100
  - function: "sin"
    offset: 0.0444444
    amplitude: 0.0444444
    frequency: 2700
output:
  plot: True
  wavefile: "wave_square.csv"
```
