# 【Python】Jinja2のテンプレートと Yamlのパラメータを使って、ファイルを生成する
updated at 2024/8/31

## 実行内容
テンプレートファイルとYamlのパラメータファイルからファイルを生成して出力する。

1. テンプレートエンジンとして jinja2を使用。
2. パラメータはYamlファイルから与える。

### 実行方法

```Shell
render_file.py テンプレートファイル名 入力ファイル名 出力ファイル名

> render_file.py  Sample.yml Sample.txt.j2 Output.txt
```

## テンプレートファイルとパラメータファイルの例

**Sample.txt.j2**

```TEXT
# This is a sample text file.
param1 = {{ param1 }};
param2 = {{ param2 }};
param3 = {{ param3 }};
sum = {{ param2 + param3 }};
# end of file
```

**Sample.yml**

```YAML
# Input Yaml
param1: "parameter No.1"
param2: 1
param3: 101
```

## Pythonのコード

```Python
#!/usr/bin/env python3

import sys
import os
import pathlib
import yaml
from jinja2 import Template, Environment, FileSystemLoader

def render_file(fyml, ftpl, fout):
  print(f'Input_Yaml: {fyml} , Input_Template: {ftpl} , Output_File: {fout}')

  # テンプレートファイルの絶対パス,ファイル名取得
  tfilePath = pathlib.Path( ftpl ).resolve()
  tdirPath  = tfilePath.parent
  tfileName = tfilePath.name
  
  # Yamlファイルからパラメータを読み込む
  with open( fyml, 'r') as yml:
    paramDict = yaml.safe_load(yml)

  # テンプレート
  env = Environment(loader=FileSystemLoader(str(tdirPath)))
  template = env.get_template(tfileName)
  
  # レンダリング
  rendered_s = template.render(paramDict)

  # ファイル出力
  with open( fout, 'w')as fw:
    fw.write(rendered_s)

if __name__ == '__main__':
  args = sys.argv
  if 4 <= len(args):
    if os.path.isfile(args[1]):
      if os.path.isfile(args[2]):
        if os.path.isfile(args[3]):
          print(f'Output {args[3]} already Exist!')
        else:
          render_file(args[1], args[2], args[3])
      else:
        print(f'Temlate {args[2]} Not Found!')
    else:
      print(f'File {args[1]} Not Found!')
  else:
    print(f'Usage:')
    print(f'  {pathlib.Path(args[0]).name} parameter_yaml template_file output_file')
```

## References

* [Jinja Documentation](https://jinja.palletsprojects.com/en/3.1.x/)
* [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
