# 分类PoWBlockChain实现
本例子按照Python面向对象设计思想，将单一的PoWblockchain.py程序解耦成多个类的方式实现，类别包括 Block（区块类）、Chian（链类）、Transaction（交易记录类）、BlockChainAPI（区块链后端类）和 main函数。单文件代码为PoWblockchain.py。

## 使用方式
分类PowBlockChain和单文件PoWblockchain.py没有任何区别，只要运行main函数即可启动整个程序。  
后端程序默认的端口为6000，如果主机的6000端口已经被占用，则可以直接在BlockChainAPI对象的run方法中修改port参数。