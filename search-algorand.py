from algosdk import account
import threading
import requests
import json
import re



class Algobot():

    def __init__(self):
        """set the initial variable"""
        self.address = ''
        self.private_key = ''
        self.url = ''

    def generate_algorand_keypair(self):
        """generate a private_key and public adress and set the url with the adress"""
        self.private_key, self.address = account.generate_account()
        self.url = ("https://algoindexer.algoexplorerapi.io/v2/accounts/" + self.address)

    def manager(self, iter):
        """The main method managed the iteration ,call other methods and save the result in the BD calling a Bd module"""
        result = self.check_method_online()
        print(result)
        #print(self.url)


    def check_method_online(self):
        """This method use the api online for make requests and test the diferents results ."""
        self.generate_algorand_keypair()

        #call to api online
        response = requests.get(self.url)
        if response.content != None:
            res = json.loads(response.content)
        else:
            return ('error', 'not content', 'status_code:' + response.status_code)
        
        #manage a not found adress result
        if response.status_code == 404:
            #load the json only if is not empty

            

            try:
                #try to identify the problem for report
                if res['message'] == 'Not Found':
                    return ('error', 'not found_error')

                    #need regex for more acuracy response
                else:
                    return ('error', {'undeterminate for now': res})

            except Exception as err:
                return ('error', err)

        elif response.status_code == 200:
            
            #test if the account have more than 0 algo or assets
            if res['account']['amount'] > 0 or res['account']['total-assets-opted-in'] > 0:
                amount = res['account']['amount']
                assets = res['account']['total-assets-opted-in']
                return ('ok', {'direction': (self.private_key, self.address ), 'amount': amount, 'assets': assets})
            
            return ('ok', (self.private_key, self.address ))
        else:
            return ('error_not_handler', response.status_code)



algo = Algobot()
algo.manager(1)
