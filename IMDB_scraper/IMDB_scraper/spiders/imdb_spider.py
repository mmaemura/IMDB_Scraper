#to run
#conda activate PIC16B
#scrapy crawl imdb_spider -o results.csv

#response.css("div.filmo-row").css("a::text")[0].get()   #to get 'data'
#response.css("div.filmo-row").css("::attr(id)").getall() #gives id to acting roles

import scrapy

class ImdbSpider(scrapy.Spider):
    """
    class to house our scraper. Will start on the IMDB page for 'Cars', then
    will crawl to the actors' page for the movie. Then will crawl to each of
    the actors and gather data on the movies they have all acted in. Yields
    a csv for all the actors and their movies.
    """
    
    name = 'imdb_spider' #will use this name when calling the spider

    start_urls = ['https://www.imdb.com/title/tt0317219/'] #the 'Cars' IMDB page

    def parse(self, response):
        """
        Assumes we're on the start url, i.e the main page for Cars on IMDB.
        Then takes traverses to the 'Cast & crew' page for Cars. 
        """

        cast_page_link = response.css("li.ipc-inline-list__item a")[2].attrib['href']
        #after testing, we need the second item from
        #response.css(li.ipc-inline-list__item a)

        if cast_page_link:
            cast_page_link = response.urljoin(cast_page_link) #creates the full url for the 'Cast & crew' page
            yield scrapy.Request(cast_page_link, callback = self.parse_full_credits) #attempts to crawl to the 'Cast & crew' page
            
    
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
                media_name = filmo.css("a::text")[0].get()
                media_name = media_name.replace(",", "")
                movie_or_TV_name.append(media_name)

        yield {
            "actor": actor_name,
            "movie_or_TV_name": movie_or_TV_name
        }



