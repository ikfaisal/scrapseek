# scrapseek
In this application, I have scrapped www.seek.com.au.

To do that I have used scrapy and beutiful soup.

'''
  scrapy startproject scrapjobs
'''

This command will scaffold the structure for scrapy.

I need to write a spider to get it going.

There are two css selectors. One is browing each job advretised in seek and opening corresponding job. Other one is searching for next button. And follow that link.

When I have opened one particular job I wanted to fetch

- Job Title
- Job Description
- Job Posting Date
- Job Location
- Job Salary
- Job Category

I have used beutiful soup to do that.

After writing the whole spider. We need to execute following command.

'''
  scrapy crawl datasciencespider -o datasciencejobs.json
'''
