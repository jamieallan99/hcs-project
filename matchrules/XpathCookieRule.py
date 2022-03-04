from matchrules import MatchRuleInterface
import scrapy

class XpathCookieRule(MatchRuleInterface.MatchRuleInterface):
    def extract(self, response: scrapy.http.Response):
        key = response.url
        items = []
        
        if key=="https://www.microsoft.com":
            items.append(response.xpath("//p[contains(.//text(), 'cookie')]").get()[:1350])
        elif key=="https://www.support.google.com":
            items.append(response.xpath("//span[contains(.//text(), 'cookie')]").get()[:1000])
        else:
            items.append(response.xpath("//span[contains(., 'cookie')]/..").get())
            items.append(response.xpath("//p[contains(., 'cookie')]/..").get())
            items.append(response.xpath("//div[contains(., 'cookie')]/..").get())
        pass
        
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
