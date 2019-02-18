import scrapy
import requests
from bs4 import BeautifulSoup

class JobSpider(scrapy.Spider):
    name = 'datasciencespider'

    start_urls = [
        'https://www.seek.com.au/data-scientist-jobs/in-All-Australia?salaryrange=0-70000&salarytype=annual'
        , 'https://www.seek.com.au/data-analyst-jobs/in-All-Australia?salaryrange=0-70000&salarytype=annual'
        , 'https://www.seek.com.au/data-engineer-jobs/in-All-Australia?salaryrange=0-70000&salarytype=annual'
        , 'https://www.seek.com.au/research-scientist-jobs/in-All-Australia?salaryrange=0-70000&salarytype=annual'
        , 'https://www.seek.com.au/business-intelligence-jobs/in-All-Australia?salaryrange=0-70000&salarytype=annual'
        , 'https://www.seek.com.au/data-scientist-jobs/in-All-Australia?salaryrange=70001-120000&salarytype=annual'
        , 'https://www.seek.com.au/data-analyst-jobs/in-All-Australia?salaryrange=70001-120000&salarytype=annual'
        , 'https://www.seek.com.au/data-engineer-jobs/in-All-Australia?salaryrange=70001-120000&salarytype=annual'
        , 'https://www.seek.com.au/research-scientist-jobs/in-All-Australia?salaryrange=70001-120000&salarytype=annual'
        , 'https://www.seek.com.au/business-intelligence-jobs/in-All-Australia?salaryrange=70001-120000&salarytype=annual'
        , 'https://www.seek.com.au/data-scientist-jobs/in-All-Australia?salaryrange=120001-999999&salarytype=annual'
        , 'https://www.seek.com.au/data-analyst-jobs/in-All-Australia?salaryrange=120001-999999&salarytype=annual'
        , 'https://www.seek.com.au/data-engineer-jobs/in-All-Australia?salaryrange=120001-999999&salarytype=annual'
        , 'https://www.seek.com.au/research-scientist-jobs/in-All-Australia?salaryrange=120001-999999&salarytype=annual'
        , 'https://www.seek.com.au/business-intelligence-jobs/in-All-Australia?salaryrange=120001-999999&salarytype=annual'
    ]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('a._2iNL7wI::attr(href)'):
            yield response.follow(href, self.parse_job)

        # bHpQ-bp
        # follow pagination links
        for href in response.css('a.bHpQ-bp::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_job(self, response):

        def extract_job_title(query):

            resultStr = ""

            try:
                # response = requests.get(query)
                soup = BeautifulSoup(response.body, 'lxml')
                element = soup.findAll("span", {"data-automation": "job-detail-title"})
                resultStr = element[0].text
            except:
                resultStr = ""

            return resultStr

        def extract_job_info(tagName, attrName, attrValue):

            resultStr = ""

            try:
                # response = requests.get(query)
                soup = BeautifulSoup(response.body, 'lxml')
                element = soup.findAll(tagName, {attrName: attrValue})
                resultStr = element[0].text
            except:
                resultStr = ""

            return resultStr

        def get_job_info(spanName, attrName, attrValue):
            '''
            Check tag name and return value where attrname and attvalue matches with attribute name and attribute value

            Example:
            <span data-automation="job-detail-title" class="_3FrNV7v _12_uzrS E6m4BZb"><span class=""><h1>Data Scientist</h1></span></span>

            If user sends span, data-automation, job-detail-title, it'll return Data Scientist
            '''

            job_soup = BeautifulSoup(response.body, 'lxml')

            element = job_soup.findAll(spanName, {attrName: attrValue})

            elementText = 'N/A'

            if len(element) > 0:
                elementText = element[0].text

            return elementText

        def get_job_information(whattofind):
            '''
            This method is specifcally for location and salary. For salary info there are no tags.
            It'll search every tag and if found sends location and salary back to user.a_tag
            '''

            job_soup = BeautifulSoup(response.body, 'lxml')

            thisdict = {
              "Job Listing Date": "N/A",
              "Location": "N/A",
              "Work Type": "N/A",
              "Salary": "N/A",
              "Classification": "N/A"
            }

            seekingJobListingDate = False
            seekingLocation = False
            seekingWorkType = False

            element = job_soup.find("section", {'aria-labelledby': 'jobInfoHeader'})

            for i in element:
                i_all = i.findAll('div')
                for j in i:
                    if 'Salary' in j.text:
                        thisdict["Salary"] = j.text.replace('Salary', '')
                    elif 'Classification' in j.text:
                        thisdict["Classification"] = j.text.replace('Classification', '')
                    else:
                        if j.text not in ['Job Information']:
                            if j.text == 'Job Listing Date':
                                seekingJobListingDate = True
                            elif j.text == 'Location':
                                seekingLocation = True
                            elif j.text == 'Work Type':
                                seekingWorkType = True
                            elif seekingJobListingDate == True:
                                seekingJobListingDate = False
                                seekingLocation = False
                                seekingWorkType = False
                                thisdict["Job Listing Date"] = j.text
                            elif seekingLocation == True:
                                seekingJobListingDate = False
                                seekingLocation = False
                                seekingWorkType = False
                                thisdict["Location"] = j.text
                            elif seekingWorkType == True:
                                seekingJobListingDate = False
                                seekingLocation = False
                                seekingWorkType = False
                                thisdict["Work Type"] = j.text

            return thisdict[whattofind]

        yield {
            'job_url': response.url
            , 'job_title': get_job_info('span', 'data-automation', 'job-detail-title')
            , 'job_desc': get_job_info('div', 'data-automation', 'mobileTemplate')
            , 'job_company': get_job_info('span', 'data-automation', 'advertiser-name')
            , 'job_detail_date': get_job_info('dd', 'data-automation', 'job-detail-date')
            , 'job_detail_work_type': get_job_info('dd', 'data-automation', 'job-detail-work-type')
            , 'job_right_to_work': get_job_info('span', 'data-automation', 'rightToWorkRequired')
            , 'job_salary': get_job_information('Salary')
            , 'job_classification': get_job_information('Classification')
            , 'job_location': get_job_information('Location')
        }
