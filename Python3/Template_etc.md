# テンプレートエンジン

## envsubst

### tenplate

```Text
// envsubst template
  value1 = ${param_A}
  value2 = ${param_B}
// if statement not available
```

### ユーザーインストール

#### コンパイルする場合

```Shell
wget https://ftp.gnu.org/gnu/gettext/gettext-0.20.2.tar.gz
tar xvfz gettext-0.20.2.tar.gz
cd gettext-0.20.2
./configure --prefix=$HOME/local/gettext/0_20_2
make
make install

ln -s $HOME/local/gettext/0_20_2/bin/envsubst $HOME/local/bin/
```

#### rpmから抽出する場合

```Shell
wget http://mirror.centos.org/centos/7/os/x86_64/Packages/gettext-0.19.8.1-3.el7.x86_64.rpm
rpm2cpio gettext-0.19.8.1-3.el7.x86_64.rpm | cpio --list
mkdir work
cd work
rpm2cpio ../gettext-0.19.8.1-3.el7.x86_64.rpm | cpio -ivd
tree
```

## jinja2

### tenplate

```Text
// Jinja2 template
  value1 = {{ param_A }}
  value2 = {{ param_B }}
{% if param_C == 0 %}
  print("value3 is Zero.")
{% else %}
  print("value3 is Not Zero.")
{% endif %}
```
## Template toolkit

### tenplate

```Text
// Template toolkit template
  value1 = [% param_A %]
  value2 = [% param_B %]
[% IF param_C == 0 %]
  print("value3 is Zero.")
[% ELSE %]
  print("value3 is Not Zero.")
[% END %]
```

## gcc

### tenplate

```Text
// envsubst template
  value1 = param_A
  value2 = param_B
#if param_C == 0
  print("value3 is Zero.")
#else
  print("value3 is Not Zero.")
#endif
```

### 実行

```Shell
cat text_template.tmpl | gcc -E -C -P -include parameter.h - | cat --squeeze-blank > text_generated.txt
```
