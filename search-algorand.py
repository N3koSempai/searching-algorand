from algosdk import account
import threading
import requests
import json
import re
import conn


class Algobot():

    def __init__(self):
        """set the initial variable"""
        self.address = ''
        self.private_key = ''
        self.url = ''
        #initialize the database
        self.db = conn.DB()
        self.db.start()


    def generate_algorand_keypair(self):
        """generate a private_key and public adress and set the url with the adress"""
        self.private_key, self.address = account.generate_account()
        try:

            self.url = ("https://algoindexer.algoexplorerapi.io/v2/accounts/" + self.address)
        except Exception as err:
            #change this save the error in the database and show in the screen
            pass

    def manager(self, iter, method):
        """The main method managed the iteration ,call other methods and save the result in the BD calling a Bd module"""
        result = self.check_method_online()
        
        # vaiable for statistics
        temp_match = 0
        temp_nf = 0
        temp_error = 0
        temp_critical_error = 0
        #how much iterations 
        if method == 'online':
            for i in range(0,iter):
                
                #make call to the api online
                result = self.check_method_online()
                
                
                # the answer is ok
                if result[0] == 'ok':

                    #the answer have amount or assets > 0
                    print(result[1]['acuracy'])
                    if result[1]['acuracy'] == 'good':
                        self.db.added_match(200, result[1]['acuracy'], result[1]['direction'][0],result[1]['direction'][1],result[1]['amount'],result[1]['assets'])

                    elif result[1]['acuracy'] == 'bad':
                        self.db.added_match(200, result[1]['acuracy'], result[1]['direction'][0],result[1]['direction'][1])
                    temp_match = temp_match + 1
                elif result[0] == 'error_not_handler':
                    try:
                        self.db.added_error(result[1], result[2])
                    except Exception as err:
                        self.db.added_error('999', 'internal error when try to save error not handler: {miss}'.format(miss = err) )
                    temp_error = temp_error + 1
                elif result[0] == 'error':
                    if result[1] == 'not_content':
                        print('Critical error, not content found in the response of the api online \n Are you connected to internet?')
                        print('\n status code: ', result[2])
                        temp_critical_error = temp_critical_error + 1
                        #remove this
                        self.db.added_error(900, result[2])
                        
                    elif result[1] == 'Not Found':
                        #normal error when the account is new
                        #100 is for new address
                        # not make nothing for now
                        temp_nf = temp_nf + 1
                        # 
                        self.db.added_error(900, result[2])
                    
                    elif result[1] == 'undeterminate for now':
                        #900 for unidentified error

                        # !!Atention!! . THIS CONDITIONAL WORK WITH ERROR. MAKE THE SAME OF 'NOT FOUND' COINDITIONAL
                        

                        # disable for make less petition to the database. now dont save the not found results, only stdistics save
                        #print(self.db.added_error(900, result[2]['message']))
                        
                        temp_nf = temp_nf + 1
            #send stadistics to the database when the loop is finished for better performance
            print(self.db.added_std(temp_match,temp_nf,temp_error,temp_critical_error))
            self.report(temp_nf,temp_match,temp_error,temp_critical_error)
            
    def check_method_online(self):
        """This method use the api online for make requests and test the diferents results ."""
        self.generate_algorand_keypair()

        #call to api online
        response = requests.get(self.url)
        if response.content != None:
            res = json.loads(response.content)
        else:
            return ('error', 'not content', response.status_code)
        
        #manage a not found adress result
        if response.status_code == 404:
            #load the json only if is not empty

            

            try:
                #try to identify the problem for report
                if res['message'] == 'Not Found':
                    return ('error', 'not found_error')

                    #need regex for more acuracy response
                else:
                    return ('error', 'undeterminate for now', res)

            except Exception as err:
                return ('error', err)

        elif response.status_code == 200:
            
            #test if the account have more than 0 algo or assets
            if res['account']['amount'] > 0 or res['account']['total-assets-opted-in'] > 0:
                amount = res['account']['amount']
                assets = res['account']['total-assets-opted-in']
                #acuracy is used for show the level of verification (if amount and assets is > 0)
                return ('ok', {'acuracy':'good','direction': (self.private_key, self.address ), 'amount': amount, 'assets': assets})
            
            return ('ok', {'acuracy':'bad','direction': (self.private_key, self.address )})
        else:
            
            return ('error_not_handler', response.status_code, res)

    def report(self,temp_nf, temp_match, temp_error,temp_critical_error):
        print(""" Final Report For This session
                    {0} , {1} , {2}, {3}
            """.format( temp_nf, temp_match, temp_error,temp_critical_error))

algo = Algobot()
algo.manager(10, 'online')
