# fortunetelling-laowang
老夫精通阴阳五行， 能够算命、紫微斗数、姓名测算、占卜凶吉、看命运八字等。命里有时终须有，命里无时莫强求。



# 环境准备
1. 安装python3.11
2. 安装virtualenvwrapper
```markdown
virtualenvwrapper 是一个用于管理多个虚拟环境的工具，它在 virtualenv 的基础上提供了一些便捷的功能。以下是在 macOS 上安装和配置 virtualenvwrapper 的详细步骤：

步骤 1：安装 virtualenv 和 virtualenvwrapper
首先，你需要确保已经安装了 pip 和 virtualenv。

安装 pip

如果还没有安装 pip，可以使用以下命令安装：

sh
复制代码
sudo easy_install pip
安装 virtualenv 和 virtualenvwrapper

使用 pip 来安装 virtualenv 和 virtualenvwrapper：

sh
复制代码
pip install virtualenv
pip install virtualenvwrapper
步骤 2：配置 virtualenvwrapper
配置 Shell 环境

打开或创建你的 shell 配置文件（例如 ~/.bashrc、~/.bash_profile、~/.zshrc 等，具体取决于你使用的 shell）。在文件末尾添加以下行：

sh
复制代码
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=$(which python3)
source $(which virtualenvwrapper.sh)
这里 WORKON_HOME 是你希望存储虚拟环境的目录，默认是 ~/.virtualenvs。你可以根据需要更改。

重新加载 Shell 配置

保存文件后，重新加载你的 shell 配置文件：

sh
复制代码
source ~/.bashrc
或者

sh
复制代码
source ~/.bash_profile
或者

sh
复制代码
source ~/.zshrc
具体取决于你使用的 shell。

步骤 3：使用 virtualenvwrapper
创建虚拟环境

使用 mkvirtualenv 命令创建一个新的虚拟环境：

sh
复制代码
mkvirtualenv myenv
这里的 myenv 是虚拟环境的名称，你可以根据需要更改。

激活虚拟环境

使用 workon 命令激活虚拟环境：

sh
复制代码
workon myenv
停用虚拟环境

完成工作后，你可以通过以下命令停用虚拟环境：

sh
复制代码
deactivate
列出所有虚拟环境

使用 lsvirtualenv 命令列出所有虚拟环境：

sh
复制代码
lsvirtualenv
删除虚拟环境

使用 rmvirtualenv 命令删除一个虚拟环境：

sh
复制代码
rmvirtualenv myenv
总结
通过以上步骤，你可以在 macOS 上安装和配置 virtualenvwrapper，并使用它来方便地管理多个虚拟环境。virtualenvwrapper 提供了一些便捷的命令，使得创建、激活、停用和删除虚拟环境变得更加容易。
```
4. 创建虚拟环境
```shell
mkvirtualenv fortunetelling-laowang
```

5. 安装依赖
```shell
pip install -r requirements.txt
```

6. 配置pycharm
    - 打开setting->Python Interpreter
    - 新建一个虚拟环境，选择刚刚创建的虚拟环境
7. 环境变量配置 OPENAI_API_KEY
```shell
export OPENAI_API_KEY=your_openai_api_key 
```


# 启动
```shell
python main.py
```