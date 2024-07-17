# Learn-Blockchains-by-Building-One
本仓库使用Python学习搭建一个简单的区块链  
本项目参考了开源项目 https://github.com/dvf/blockchain  
具体学习内容可参考博客 https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

This repo is to lean Blockchain by building a simple one  
This repo consult the open source project https://github.com/dvf/blockchain  
If you want to learn more detail about the project,you can get more info from this blog https://hackernoon.com/learn-blockchains-by-building-one-117428612f46  

使用方法
* 打开两个终端，分别运行blockchain.py程序，一个端口设置为6000，另一个设置为6001。（这里直接使用vscode 终端）
<img src='/img/start-service.png'>
* 使用vscode插件postcode进行接口测试，这里测试了/mine,/chain,/nodes/register,/nodes/resolve,/transactions/new等接口，接口信息见图
<img src='/img/postcode.png'>
1.挖矿
<img src='/img/mine.png'>
2.展示区块链内容
<img src='/img/chain.png'>
3.注册结点
<img src='/img/nodeRegister.png'>
4.共识解决冲突,结点2（端口6001）的链长度为3，而结点1（6000）的链长度为1，解决冲突后，结点1上的区块链会被修改，并变成三个节点
<img src='/img/resolve.png'>