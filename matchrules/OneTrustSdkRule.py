from matchrules import MatchRuleInterface
import scrapy

"""
    a rule which extracts parts of a webpage code based on the id (and forms of) attribute "onetrust-banner-sdk"
"""
class OneTrustSdkRule(MatchRuleInterface.MatchRuleInterface):
    def extract(self, response: scrapy.http.Response):
        res = response.css('[id*="onetrust-banner-sdk"]').get()
        if res is None:
            return ''
        else:
            return res
        
        
    

