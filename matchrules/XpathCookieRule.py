from matchrules import MatchRuleInterface
import scrapy

class XpathCookieRule(MatchRuleInterface.MatchRuleInterface):
    def extract(self, response: scrapy.http.Response):

        items = []
        items.append(response.xpath("//span[contains(., 'cookie')]/..").get())
        items.append(response.xpath("//p[contains(., 'cookie')]/..").get())
        items.append(response.xpath("//div[contains(., 'cookie')]/..").get())
        
        res = ""
        
        for item in items:
            if self.validateConent(item):
                res = self.mergeItems(res, item)
        
        return res
        
    
    def mergeItems(self, item1, item2):
        if len(item1) == 0:
            return item2
        
        if len(item1) > len(item2) and item2 in item1:
            return item2
        
        if len(item2) > len(item1) and item1 in item2:
            return item1
        
        return item1+item2
        
        
    
    def validateConent(self, html: str):
        if html is None or len(html) < 10:
            return False 
        
        if "<body" in html:
            return False
        
        return True
