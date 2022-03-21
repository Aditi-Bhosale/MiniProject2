import scrapy

class InfoSpider(scrapy.Spider):
    name='inf'
    start_urls=[
        #'https://www.tripadvisor.in/Tourism-g297608-Ahmedabad_Ahmedabad_District_Gujarat-Vacations.html'
        #'https://www.tripadvisor.in/Tourism-g304555-Jaipur_Jaipur_District_Rajasthan-Vacations.html'
        #'https://www.tripadvisor.in/Tourism-g297586-Hyderabad_Hyderabad_District_Telangana-Vacations.html'
        'https://www.tripadvisor.in/Tourism-g304551-New_Delhi_National_Capital_Territory_of_Delhi-Vacations.html'
        #'https://www.tripadvisor.in/Tourism-g304554-Mumbai_Maharashtra-Vacations.html'
    ]

    def parse(self,response):
        data=response.css('div.fqCDQ::text').extract_first()
        #data=response.css('div.fqCDQ.cxDRi._J.B-.G-.Wh._S::text').extract_first()

        # with open("F:\Aditi\Semesters\SEM6\MiniProject2\TravelAdvisor\Mumbai.txt", "a") as myfile:
        #     myfile.write("\n"+data)
        with open(r"F:\Aditi\Semesters\SEM6\MiniProject2\TravelAdvisor\NewDelhi.txt", "a") as myfile:
            myfile.write("\n"+data)
        
            
        yield {'text':data}