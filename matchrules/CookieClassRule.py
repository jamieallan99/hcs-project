from matchrules import MatchRuleInterface
import scrapy

class CookieClassRule(MatchRuleInterface.MatchRuleInterface):
    def extract(self, response: scrapy.http.Response):
        items = []
        
        items.append(response.css('[class*="cookie"]').get())
        
        res = ''
        
        for item in items:
            if self.validateConent(item):
                res = self.mergeItems(res, item)
        
        return res
        
    

