from scrapy import (
    Spider,
    Request,
)
from time import sleep
from utils.selenium_webdriver import (
    Driver,
    EC,
    WebDriverWait,
)
from parse_twitter.items import ParseTwitterItem


class ParserTwitter(Spider):
    name = 'twitter_hashtag'

    def start_requests(self):
        yield Request(
            url='https://twitter.com/hashtag/zelenskywarcriminal?src=hashtag_click&f=live',
            callback=self.parse,
            method="GET",
            encoding="utf-8"
        )

    @staticmethod
    def find_element(driver:object, css_selector:str, time_wait:int=15):
        try:
            return WebDriverWait(driver, time_wait).until(
                EC.presence_of_element_located(
                    (
                        "css selector",
                        css_selector
                    )
                )
            )
        except:
            return None

    def parse(self, response):
        k = 1
        scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        with Driver(url=response.url) as driver:
            sleep(1.5)
            screen_height = driver.execute_script("return window.screen.height;")
            while True:
                
                driver.execute_script("window.scrollTo(0, {screen_height}*{k});".format(screen_height=screen_height, k=k))  
                k += 1
                sleep(scroll_pause_time)
                scroll_height = driver.execute_script("return document.body.scrollHeight;")  
                
                for post in driver.find_elements(
                    "css selector", 
                    'div[data-testid="cellInnerDiv"]'
                ):
                    name = self.find_element(
                        post,
                        'a[role="link"]'
                    )
                    name_text = self.find_element(
                        post,
                        "span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0"
                    )

                    name_text = i.strip() if name_text and (i:=name_text.text) else None
                    name_link = name.get_attribute("href") if name else None 

                    post_params = self.find_element(
                        post,
                        "a.css-4rbku5.css-18t94o4.css-901oao.r-14j79pv.r-1loqt21.r-xoduu5.r-1q142lx."
                        "r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0"
                    )

                    post_link = post_params.get_attribute("href") if post_params else None
                    post_date = i.get_attribute("datetime") if (i:=self.find_element(post_params, "time")) else None
                    post_stats = self.find_element(
                        post, 
                        "div.css-1dbjc4n.r-1ta3fxp.r-18u37iz.r-1wtj0ep.r-1s2bzr4.r-1mdbhws"
                    )
                    post_stats = i.strip() if post_stats and (i:=post_stats.get_attribute("aria-label")) else None
                    yield ParseTwitterItem(
                        name_twitter=name_text,
                        name_link=name_link,
                        post_link=post_link,
                        post_date=post_date,
                        post_stats=post_stats
                    )
                if (screen_height) * k > scroll_height:
                    break
                