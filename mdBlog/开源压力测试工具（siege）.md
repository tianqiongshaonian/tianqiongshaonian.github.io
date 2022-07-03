# 开源压力测试工具（siege）

**当前环境（centos 7+）**

第一步更新：

	sudo yum -y update

第二步安装所需要的依赖：

	sudo yum install -y gcc make openssl-devel

第三步下载软件包：

	wget http://download.joedog.org/siege/siege-latest.tar.gz

第四步解压： 

	tar zxvf ./siege-latest.tar.gz 

第五步删除安装包：

	rm -rf siege-latest.tar.gz

第五步进入目录里面：

	cd siege-4.1.3/

第六步骤编译

	./configure && make

第七步安装：

	sudo make install

第八步把文档拷贝当前根目录下：

	cp cp doc/siegerc ~/.siegerc

第九步骤查看siege安装版本

	siege -V

开始测试：10 个客户端发起 10个请求

	siege -c 10 -r 10 --log=./siege.log https://www.baidu.com