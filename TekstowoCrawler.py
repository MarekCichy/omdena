import scrapy
from scrapy.crawler import CrawlerProcess

class TekstowoSpider(scrapy.Spider):
    name = "tekstowo"
    
    download_delay = 0.25

    def start_requests(self):
        for url in urls_list:
            yield scrapy.Request(url=url,
                                 callback=self.parse_front)

    # First, parse links to talks and add transcript

    def parse_front(self, response):
        song_links = response.xpath("//div[@class='box-przeboje']/a[1]/@href")
        links_to_follow = song_links.extract()
        for url in links_to_follow:
            yield response.follow(url=url,
                                  callback=self.parse_pages)
    # Second parsing method:

    def parse_pages(self, response):
        # Create a SelectorList of the talk
        title = response.xpath('//div[@class="belka short "]/strong').extract()[0]
        title = title.split('Kali - ')[1]
        title = title.split('</strong>')[0]
        song = response.xpath(
            '//div[@class="song-text"]').extract()[0]
        song = song.split('<h2>Tekst piosenki:</h2>')[1]
        song = song.split('<a href="javascript:')[0]
        noise = ['\n','\t', '\r', '<br>', '<strong>', '</strong>','<p>', '</p>', ';']
        for n in noise:
            song = song.replace(n,' ')
        lyrics_dict[title] = song

urls_list = ['https://www.tekstowo.pl/piosenki_artysty,kali.html']
for i in range(2,5):
    urls_list.append('https://www.tekstowo.pl/piosenki_artysty,kali,alfabetycznie,strona,'+str(i)+'.html')
    
# Initialize the dictionary **outside** of the Spider class
lyrics_dict = dict()

# Run the Spider
process = CrawlerProcess()
process.crawl(TekstowoSpider)
process.start()

with open('kali_dict.csv', 'w', encoding='utf-8') as f:
    for key in lyrics_dict.keys():
        f.write("%s;%s\n"%(key,lyrics_dict[key]))