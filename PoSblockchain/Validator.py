# 验证者
class Validator:
    def __init__(self,address:str,stake:float) -> None:
        self.address=address
        self.stake=stake

    def __repr__(self) -> str:
        return f'Validator(address:{self.address},stake:{self.stake})'
