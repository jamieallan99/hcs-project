from scrapy.http import Response
from html_parsing import strip_tags

"""
    interface for a specific rule which validates content and merges crawled items
"""
class MatchRuleInterface:
    def extract(self, response: Response):
        pass
    
    """
        function which merge items since a smaller crawled chunk of code can be crawled inside a bigger one
        this is to prevent duplicate crawled text
    """
    def mergeItems(self, item1, item2):
        if len(item1) == 0:
            return item2
        
        if len(item1) > len(item2) and item2 in item1:
            return item2
        
        if len(item2) > len(item1) and item1 in item2:
            return item1
        
        return item1+item2
        
        
    """
        function which validates our cralwed text

        it return False if the crawler returns the whole body of cralwed page
        or if none code was found or is less than 100 characters
    """
    def validateConent(self, html: str):
        if html is None or len(html) < 100:
            return False 
        
        if "<body" in html:
            return False
        
        if len(strip_tags(html)) < 100:
            return False
        
        return True
    
        
    
