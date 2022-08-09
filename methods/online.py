import requests
import json


class Online_method():


    def check_method_online(self, keys):
        """This method use the api online for make requests and test the diferents results ."""

        #call to api online
        response = requests.get(keys[2])
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
                return ('ok', {'acuracy':'good','direction': (keys[0], keys[1] ), 'amount': amount, 'assets': assets})

            return ('ok', {'acuracy':'bad','direction': (keys[0], keys[1] )})
        else:

            return ('error_not_handler', response.status_code, res)
