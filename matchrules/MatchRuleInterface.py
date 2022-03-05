from scrapy.http import Response
from html_parsing import strip_tags

class MatchRuleInterface:
    def extract(self, response: Response):
        pass
    
    
    def mergeItems(self, item1, item2):
        if len(item1) == 0:
            return item2
        
        if len(item1) > len(item2) and item2 in item1:
            return item2
        
        if len(item2) > len(item1) and item1 in item2:
            return item1
        
        return item1+item2
        
        
    
    def validateConent(self, html: str):
        if html is None or len(html) < 100:
            return False 
        
        if "<body" in html:
            return False
        
        if len(strip_tags(html)) < 100:
            return False
        
        return True
    
        
    
