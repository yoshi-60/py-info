# 【Python】テンプレートエンジンを使って、ファイル生成をする
updated at 2022/11/13

## 実行内容
テンプレートファイルとパラメータファイルからファイルを生成して出力する。

1. テンプレートエンジンとして jinja2を使用。
2. パラメータはYamlファイルから与える。
3. 生成するファイル数はYamlのリストで設定する。

## テンプレートファイルとパラメータファイルの例

**test1.txt.j2**

```TEXT
# This is the {{param0}} file.
param1 = {{ param1 }};
param2 = {{ param2 }};
param3 = {{ param3 }};
sum = {{ param2 + param3 }};
# end of file
```

**test2.txt.j2**

```TEXT
# This is the 2nd {{param0}} file.
{{ param1 }} is {{ param2 * param3 }};
# end of file2
```

**gen_text.yml**

```YAML
# Input Yaml
files: ['test1.txt', 'test2.txt']
param_keys: ['param0', 'param1', 'param2', 'param3']
param_values:
  - ['set1', 'A', 1, 101]
  - ['set2', 'B', 2, 102]
  - ['set3', 'C', 3, 103]
```

## Pythonのコード

```Python
#!/usr/bin/env python3
#
import sys
import os
import pathlib
import yaml
from jinja2 import Template, Environment, FileSystemLoader

def gen_text(fyml, sdir, ddir):
  print(f'Input_Yaml: {fyml} , Input_Directory: {sdir} , Output_Directory: {ddir}')

  # ディレクトリの絶対パス取得
  ddirpath = pathlib.Path( ddir ).resolve()
  sdirpath = pathlib.Path( sdir ).resolve()
  cdir = os.getcwd()
  
  # Yamlファイルからパラメータを読み込む
  with open( fyml, 'r') as yml:
    config = yaml.safe_load(yml)

  # パラメータの取り出し
  gen_files   = config['files']
  key_list    = config['param_keys']
  value_lists = config['param_values']
  
  # テンプレートファイル名
  tmpl_files  = [x+'.j2' for x in gen_files]
  
  # テンプレート
  env = Environment(loader=FileSystemLoader(str(sdirpath)))
  templates = [ env.get_template( x ) for x in tmpl_files]
  
  # レンダリング
  for value_list in value_lists :
    param_value = dict(zip(key_list,value_list))
    rendered_s = [ x.render(param_value) for x in templates]

    # ファイル出力
    for i,f in enumerate(gen_files) :
      fname = os.path.basename(f)
      fout = os.path.splitext(fname)[0] + '_' + param_value['param0'] + os.path.splitext(fname)[1]
      with open( ddirpath / fout, 'w')as fw:
        fw.write(rendered_s[i])
      print(f'Output_filename: {fout}')

if __name__ == '__main__':
  args = sys.argv
  if 4 <= len(args):
    if os.path.isfile(args[1]):
      if os.path.isdir(args[2]):
        if os.path.isdir(args[3]):
          gen_text(args[1], args[2], args[3])
        else:
          print(f'Directory {args[3]} Not Found!')
      else:
        print(f'Directory {args[2]} Not Found!')
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {args[0]} input_yaml source_dir dest._dir')
```

## References

* [Jinja Documentation](https://jinja.palletsprojects.com/en/3.1.x/)
* [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
