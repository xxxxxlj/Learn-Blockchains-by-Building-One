# 结点类
from urllib.parse import urlparse
class Node:
    def __init__(self,address,stake:int=0) -> None:
        ''''
            初始化节点类,包括节点和节点初始权益值
            address <any> 节点地址
            stake <int> 权益证明值，默认为0
        '''
        self.stake=stake
        # 解析url，改成可以用的那种
        parsed_url=urlparse(address)
        if parsed_url.netloc:
            self.netloc = parsed_url.netloc
        elif parsed_url.path:
            self.netloc = parsed_url.path       
        else:
            raise ValueError('Invalid URL')
        
    def register(self,nodes:list):
        '''
            注册结点
            node_set <set> 结点类
        '''
        nodes.append(self)

    @property
    def to_dict(self):
        return {
            "address":self.netloc,
            "stake":self.stake
        }
