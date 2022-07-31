 
from algosdk import account



class Algobot():

    def __init__(self):
        """set the initial variable"""
        self.address = ''
        self.private_key = ''
        self.url = ''

    def generate_algorand_keypair(self):
        """generate a private_key and public adress and set the url with the adress"""
        self.private_key, self.address = account.generate_account()
        try:

            self.url = ("https://algoindexer.algoexplorerapi.io/v2/accounts/" + self.address)
        except Exception as err:
            #change this save the error in the database and show in the screen
            print("erro", err)
            return False
        return (self.private_key, self.address,self.url)

