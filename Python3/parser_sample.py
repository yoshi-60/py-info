#!/usr/bin/env puthon3
import argparse

def get_args():
  parser = argparse.ArgumentParser(description='Parser Sample')
  parser.add_argument('name1', type=str, help='This is name 1.')
  parser.add_argument('name2', type=str, help='This is name 2.')
  parser.add_argument('-n', '--number', default=64, type=int, help='This is Integer.')
  parser.add_argument('-s', '--sex', default='male', type=str, choices=['male', 'female'], help='This is sex')
  parser.add_argument('-a', '--address', type=float, default=[0.1, 0.2], nargs=2, help='This is x,y values.')
  parser.add_argument('-l', '--list', type=str, nargs='+', help='This is name list.')
  parser.add_argument('-f', '--flag', action='store_true', help='This is flag.')

  return parser.parse_args()

if __name__ == '__main__':
  args = get_args()
  print(args)
  print(f'name 1: {args.name1}')
  print(f'name 2: {args.name2}')
  print(f'number: {args.number}')
  print(f'sex : {args.sex}')
  print(f'address: {args.address}')
  print(f'list: {args.list}')
  print(f'flag: {args.flag}')
