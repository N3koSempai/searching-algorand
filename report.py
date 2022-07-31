 
class Report():

    def reporting(self,temp_nf, temp_match, temp_error,temp_critical_error):
        print(""" |/|==================================|\|
 |/|   Final Report For This session: |\|
 |/|                                  |\|
 ==>     not found:  {0}
 ==>     match: {1}
 ==>     errors: {2}
 ==>     Internal_errors: {3}
            """.format( temp_nf, temp_match, temp_error,temp_critical_error))
