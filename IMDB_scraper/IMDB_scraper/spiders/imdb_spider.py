#to run
#scrapy crawl imdb_spider -o movies.csv

#response.css("div.filmo-row").css("a::text")[0].get()   #to get 'data'
#response.css("div.filmo-row").css("::attr(id)").getall() #gives id to acting roles

import scrapy

class ImdbSpider(scrapy.Spider):
    """

    """
    
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt0317219/']

    def parse(self, response):
        """

        """


        cast_page_link = response.css("li.ipc-inline-list__item a")[2].attrib['href']


        if cast_page_link:
            cast_page_link = response.urljoin(cast_page_link)
            yield scrapy.Request(cast_page_link, callback = self.parse_full_credits)
            
    
    def parse_full_credits(self, response):
        """

        """
        

        actors_suffixes = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        prefix = "https://www.imdb.com/"
        actors_urls = [prefix + suffix for suffix in actors_suffixes]
        for url in actors_urls:
            yield scrapy.Request(url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        """
        
        """
        actor_name = response.css("span.itemprop::text")[0].get()
        movie_or_TV_name = []

        filmo_listings = response.css("div.filmo-row")
        for filmo in filmo_listings:
            role = filmo.css("::attr(id)").get()
            if role[0:3] == 'act':
                movie_or_TV_name.append(filmo.css("a::text")[0].get())

        yield {
            "actor": actor_name,
            "movie_or_TV_name": movie_or_TV_name
        }



