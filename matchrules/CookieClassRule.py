from matchrules import MatchRuleInterface
import scrapy

"""
    a rule which extracts parts of a webpage code based on the class (and forms of) attribute "cookie"
"""
class CookieClassRule(MatchRuleInterface.MatchRuleInterface):
    def extract(self, response: scrapy.http.Response):
        items = []
        
        items.append(response.css('[class*="cookie"]').get())
        
        res = ''
        
        for item in items:
            if self.validateConent(item):
                res = self.mergeItems(res, item)
        
        return res
        
    

