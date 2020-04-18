import scrapy
import csv


class IndiaBixSpider(scrapy.Spider):
    name = 'indiabix-spider'
    start_urls = ['https://www.indiabix.com/puzzles/playing-cards-puzzles/',
                          'https://www.indiabix.com/puzzles/clock-puzzles/']

    quiz = [['question_image', 'correct_answer', 'explanation']]

    def parse(self, response):
        for puzzles in response.css('.div-puzzles-container'):  #for 1st set
        #for puzzles in response.css('.bix-div-container'):     #for 2nd set
            # for the following URL's: 
            # start_urls = ['https://www.indiabix.com/puzzles/logical-puzzles/',
            #              'https://www.indiabix.com/puzzles/number-puzzles/',
            #              'https://www.indiabix.com/puzzles/missing-letters-puzzles/',
            #              'https://www.indiabix.com/puzzles/playing-cards-puzzles/',
            #              'https://www.indiabix.com/puzzles/clock-puzzles/'] 
            IndiaBixSpider.quiz.append(['https://www.indiabix.com/'+(puzzles.css('img ::attr(src)')[0].extract())[1:],
                                        puzzles.css('table>tr>td>span ::text')[2].get(),
                                        puzzles.css('table>tr>td ::text')[5].get()])

            # for the following URL:
            # start_urls = ['https://www.indiabix.com/verbal-reasoning/character-puzzles/']
            """IndiaBixSpider.quiz.append(['https://www.indiabix.com/' + str(puzzles.css('img ::attr(src)').extract()[0]),
                                        puzzles.css('span ::text').extract()[1],
                                        puzzles.css('.bix-ans-description>p').get()])"""

        for next_page in response.css('p.mx-pager>a'):
            yield response.follow(next_page, self.parse)

        with open('quiz4.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(IndiaBixSpider.quiz)
            csvFile.close()
