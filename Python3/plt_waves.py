#!/usr/bin/env python3
# 複数のCSVファイルを重ねたグラフを出力
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plt_waves(flist):
  f_name = []
  df= []
  sample_num= []
  col_names= []
  dt = []
  clk_freq= []
  start_time = []
  stop_time  = []
  wave_max   = []
  wave_min   = []

  plt.figure(figsize=(10, 4))
  for i,fcsv in enumerate(flist):
    print(f'Input_csv: {fcsv}')

    f_name.append(os.path.basename(fcsv))
    df.append(pd.read_csv(fcsv,header=0))
    sample_num.append(len(df[i]))
    col_names.append(df[i].columns.values)
    col_max = df[i].max(axis=0).values.tolist()
    col_min = df[i].min(axis=0).values.tolist()
    dt.append(df[i].iat[1,0] - df[i].iat[0,0])
    clk_freq.append(1/dt[i])
    start_time.append(col_min[0])
    stop_time.append(col_max[0])
    wave_max.append(col_max[1])
    wave_min.append(col_min[1])

    print(f'Columns: {col_names[i][0]} , {col_names[i][1]}') 
    print(f'Sample Freq.: {clk_freq[i]} , Delta_time: {dt[i]} , Range: {start_time[i]} , {stop_time[i]} , Count: {sample_num[i]}') 
    print(f'Wave_max: {wave_max[i]} , min: {wave_min[i]}') 

    plt.plot(df[i][df[i].columns[0]], df[i][df[i].columns[1]], linestyle='solid', label=f_name[i])

  plt.title('csv_waves')
  plt.legend(bbox_to_anchor=(1.02,1), loc='upper left', borderaxespad=0)
  plt.xlabel(col_names[0][0])
  plt.ylabel(col_names[0][1])
  plt.grid(axis='both')
  plt.tight_layout()
  plt.show()

  freq = []
  Amp = []
  plt.figure(figsize=(10, 4))
  for i,fn in enumerate(f_name):
    x = df[i].iloc[:,1].to_numpy()
    F = np.fft.fft(x)
    F = F / (sample_num[i] / 2)
    Amp.append(np.abs(F))
    #Pow = Amp**2
    freq.append(np.fft.fftfreq(sample_num[i], d=dt[i]))
    plt.plot(freq[i][:sample_num[i]//2],Amp[i][:sample_num[i]//2], linestyle='solid', label=fn)

  plt.title('csv_frequency')
  plt.legend(bbox_to_anchor=(1.02,1), loc='upper left', borderaxespad=0)
  plt.xlabel('Frequency')
  plt.ylabel('Amplitude')
  plt.grid(axis='both')
  plt.tight_layout()
  plt.show()

if __name__ == '__main__':
  args = sys.argv
  nf = 0
  if 2 <= len(args):
    for fn in args[1:] :
      if not os.path.isfile(fn):
        print(f'File {fn} Not Found!')
        nf = nf + 1
    if nf == 0:
      plt_waves(args[1:])
  else:
    print(f'Usage:')
    print(f'  {args[0]} input_csv1 input_csv2 . . .')
 
