from BlockChainAPI import BlockChainAPI
from argparse import ArgumentParser

if __name__=="__main__":
    from argparse import ArgumentParser

    parser=ArgumentParser()
    parser.add_argument('-p', '--port', default=6000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    blockchain_api=BlockChainAPI()
    blockchain_api.run()
