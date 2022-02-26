# 1. 搭建环境 (系统环境为Ubuntu18.04下)

```bash
conda create -n R
conda activate R
conda install r-base -y
conda install -c conda-forge r-devtools
```

> 使用vscode的代码提示，可能还需微软的dotnet，请自行安装。

## 1. `libreadline.so.6`和`libncurses.so.5` 报错找不到 (系统库版本对不上)

```bash
# dll的版本因系统会有所区别，自行判断
cd /lib/x86_64-linux-gnu/
sudo ln -s libreadline.so.8.0 libreadline.so.6
sudo ln -s libncurses.so.6 libncurses.so.5
```

# 2. 执行要求：

> 其实主要是路径问题，不同数据集除非特意调文件结构很难保持代码一致性，调起来也不麻烦，就自行处理即可

1. 需要修改代码中：`data_root`, 代码会自动扫描文件。此外还要指定`annotation_path`的标注文件名字
2. 需要修改时间戳间隔, 找到：`kpi_seq <- ts(kpi_value, start=c(2020, 1), frequency = 24 * 60 / 15)`这一行
3. 最终会输出

> `stat.py`是用于统计指标的脚本，可以不用关注。
