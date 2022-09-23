#!/usr/bin/env python3
import numpy as np

def sin_func(x):
  bin_str = "100110"
  vratio  = 0.125
  return sin_bstr(x, bin_str, vratio)

def sin_bstr(x, bin_str, vratio):
  blen = len(bin_str)
  wsel = wave_select(bin_str)
  nx = (x / (blen * np.pi)).astype('int64')
  xr = x - (nx * blen * np.pi)
  nxr = (2 * xr / np.pi).astype('int64')
  nws = np.zeros_like(nxr)
  for iw in range(nws.size):
    nws[iw] = wsel[nxr[iw]]
  wn0 = -1.0 + vratio * (1 + np.cos(2*xr))
  wn1 = np.sin(xr)
  wn2 = -1.0 * np.sin(xr)
  wn3 = 1.0 - vratio * (1 + np.cos(2*xr))
  wn01  = np.where(nws==1, wn1, wn0)
  wn012 = np.where(nws==2, wn2, wn01)
  np_sin_bstr = np.where(nws==3, wn3, wn012)
  return np_sin_bstr

def wave_select(bin_str):
  blen = len(bin_str)
  slen = 2 * blen
  bstr = bin_str[blen-1] + bin_str + bin_str[0]
  slist = [0 for idx in range(slen)]
  idx = 0
  for ib in range(blen):
    b0 = bstr[ib:ib+2]
    b1 = bstr[ib+1:ib+3]
    if b0 == '01' and (ib % 2)== 0 :
      slist[idx] = 1
    elif b0 == '01' :
      slist[idx] = 2
    elif b0 == '10' and (ib % 2)==0 :
      slist[idx] = 2
    elif b0 == '10' :
      slist[idx] = 1
    elif b0 == '11' :
      slist[idx] = 3
    else:
      slist[idx] = 0
    idx = idx + 1
    if b1 == '01' and (ib % 2)== 0 :
      slist[idx] = 2
    elif b1 == '01' :
      slist[idx] = 1
    elif b1 == '10' and (ib % 2)==0 :
      slist[idx] = 1
    elif b1 == '10' :
      slist[idx] = 2
    elif b1 == '11' :
      slist[idx] = 3
    else:
      slist[idx] = 0
    idx = idx + 1
  return slist

if __name__ == '__main__':
  #for i in range(13):
  #  x = 0.5 * i * np.pi
  #  y = sin_func(x)
  #  print(f'x: {x} , sin(x): {np.sin(x)} , sin_func(x) {y}')
