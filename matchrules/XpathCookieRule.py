from matchrules import MatchRuleInterface
import scrapy

class XpathCookieRule(MatchRuleInterface.MatchRuleInterface):
    def extract(self, response: scrapy.http.Response):
        key = response.url
        items = []
        if key=="https://www.microsoft.com":
            items.append(response.xpath("//p[contains(.//text(), 'cookie')]").get()[:1300])
        elif key=="https://www.support.google.com":
            items.append(response.xpath("//span[contains(.//text(), 'cookie')]").get()[:1000])
        else:
            items.append(response.xpath("//span[contains(., 'cookie')]/..").get())
            items.append(response.xpath("//p[contains(., 'cookie')]/..").get())
            items.append(response.xpath("//div[contains(., 'cookie')]/..").get())
        
        res = ""
        
        for item in items:
            if self.validateConent(item):
                res = self.mergeItems(res, item)
        
        return res
        
