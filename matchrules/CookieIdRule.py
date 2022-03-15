from matchrules import MatchRuleInterface
import scrapy

"""
    a rule which extracts parts of a webpage code based on the id (and forms of) attribute "cookie"
"""
class CookieIdRule(MatchRuleInterface.MatchRuleInterface):
    def extract(self, response: scrapy.http.Response):
        items = []
        
        items.append(response.css('[id*="cookie"]').get())
        
        res = ''
        
        for item in items:
            if self.validateConent(item):
                res = self.mergeItems(res, item)
        
        return res
        
    

