from matchrules import MatchRuleInterface
import scrapy

class OneTrustSdkRule(MatchRuleInterface.MatchRuleInterface):
    def extract(self, response: scrapy.http.Response):
        res = response.css('[id*="onetrust-banner-sdk"]').get()
        if res is None:
            return ''
        else:
            return res
        
        
    

