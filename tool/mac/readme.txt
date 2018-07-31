mac版本下自带python2.7.6,所以无需再自己安装python

但是u8sdk需要PIL库，还需要安装下PIL库，命令如下：

1、先安装pip
sudo easy_install pip

2、安装完成后，安装pillow
sudo pip install pillow

3、然后就可以运行打包了
cd U8SDKTool-Win-P34
./scripts/pack.py True True 1