from algosdk import account
import threading
import requests
import json
import re



class Algobot():

    def __init__(self):
        self.address = ''
        self.private_key = ''
        self.url_explorer = 'https://algoindexer.algoexplorerapi.io/v2/accounts/'

    def generate_algorand_keypair(self):
        self.private_key, self.address = account.generate_account()

    def check(self, iter):
        #request info from the api
        response = (requests.get(self.url_explorer + self.address))
        # take only the atribut amount
        if response.status_code != 404 and response.content != None:
            try:
                rs = json.loads(response.content)
                amount = rs['account']['amount']
                #check if the address have money and save in a file called match.txt
                file = open('match.txt', 'a')
                if amount > 0:
                    file.write('address:' + self.address + ' private_key ' + self.private_key)
                    return 1
            except:
                print(rs)
                return 'error'


        else:
            print('nothing in the ', iter, ' iteration')
            return 0

algo = Algobot()
try:
    Max = int(input("write the maximun iteration(10 by default): ") or '10')
except:
    print('you have an eror, only write digits')
match = 0
error = 0
for i in range(0, Max):
    algo.generate_algorand_keypair()
    result = algo.check(i)
    if result == 'error':
        error = error + 1
        continue
    match = match + result
print("\n ITERATION FINISH: \n MATCH: ", match, '\n ERROR: ', error)




