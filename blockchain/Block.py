class Block:
    def __init__(self,index,timestamp,transactions,proof,previous_hash) -> None:
        self.index=index
        self.timestamp=timestamp
        self.transactions=transactions
        self.proof=proof
        self.previous_hash=previous_hash

    @property
    def to_dict(self):
        return {
            "index":self.index,
            "timestamp":self.timestamp,
            "transactions":[tx for tx in self.transactions],
            "proof":self.proof,
            "previous_hash":self.previous_hash 
        }