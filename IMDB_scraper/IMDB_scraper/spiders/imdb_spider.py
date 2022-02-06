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
        Assumes we're on the 'Crew & cast' page for a movie.
        Will then crawl to the pages of actors listed.
        """
    
        actors_suffixes = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        #the partial urls for each of the actors, stored in a list

        prefix = "https://www.imdb.com/"
        #first portion of the complete url for the actors' page

        actors_urls = [prefix + suffix for suffix in actors_suffixes]
        #concatenates to produce the full url

        for url in actors_urls:
            yield scrapy.Request(url, callback = self.parse_actor_page) #attempt to crawl to each of the actors' pages

    def parse_actor_page(self, response):
        """
        Assumes we're on a actor's page on IMDB.
        Yields a dictionary where the first element is
        their name, and the second is a list of all
        their movies with a credited acting role
        """
        actor_name = response.css("span.itemprop::text")[0].get()
        #after testing, we need the 0th element from
        #response.css('span.itemprop::test')
        #use get() and ::text to extract just the text

        movie_or_TV_name = [] #initiate list for the names for actor's titles

        filmo_listings = response.css("div.filmo-row")
        #list for each item in the filmographing section

        for filmo in filmo_listings: #iterate over each credit
            role = filmo.css("::attr(id)").get()
            #extract the type of work, e.g actor/actress, producer,
            #writer, soundtrack, etc

            if role[0:3] == 'act': #check if 'actor' or 'actress'
                media_name = filmo.css("a::text")[0].get()
                #get the texts of links, after experimenting,
                #we want the 0th element

                media_name = media_name.replace(",", "")
                #remove commas because extracting to csv later on

                movie_or_TV_name.append(media_name)
                #add to the list

        yield { #final output
            "actor": actor_name, #string
            "movie_or_TV_name": movie_or_TV_name #list of strings
        }



