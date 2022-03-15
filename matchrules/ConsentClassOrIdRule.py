from matchrules import MatchRuleInterface
import scrapy

"""
    a rule which extracts parts of a webpage code based on the id or class (and forms of) attribute "consent"
"""
class ConsentClassOrIdRule(MatchRuleInterface.MatchRuleInterface):
    def extract(self, response: scrapy.http.Response):
        items = []
        
        items.append(response.css('[class*="consent"], [id*=consent]').get())
        
        res = ''
        
        for item in items:
            if self.validateConent(item):
                res = self.mergeItems(res, item)
        
        return res
        
    

