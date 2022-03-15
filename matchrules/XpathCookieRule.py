from matchrules import MatchRuleInterface
import scrapy

"""
    a rule which extracts parts of a webpage code based on the key-word "cookie"
    this key-word is search anywhere in the span/p/div tags of HTML code
"""
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
        
