import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd


def find_jobs_from(website, job_title, location, filename="results.xls"):
    if website == 'Indeed':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_information_indeed(job_soup)
    save_jobs_to_excel(jobs_list, filename)

    print('{} new job postings retrieved from {}. Stored in {}.'.format(num_listings,
                                                                        website, filename))


def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)


def load_indeed_jobs_div(job_title, location):
    getVars = {'q': job_title, 'l': location, 'fromage': 'last', 'sort': 'date'}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup


def extract_job_information_indeed(job_soup):
    job_elems = job_soup.select('div.slider_container.css-11g4k3a.eu4oa1w0')

    cols = []
    extracted_info = []

    titles = []
    cols.append('titles')
    for job_elem in job_elems:
        titles.append(extract_job_title_indeed(job_elem))
    extracted_info.append(titles)

    companies = []
    cols.append('companies')
    for job_elem in job_elems:
        companies.append(extract_company_indeed(job_elem))
    extracted_info.append(companies)

    blurbs = []
    cols.append('blurbs')
    for job_elem in job_elems:
        blurbs.append(extract_blurb_indeed(job_elem))
    extracted_info.append(blurbs)

    links = []
    cols.append('links')
    for job_elem in job_elems:
        links.append(extract_link_indeed(job_elem))
    extracted_info.append(links)

    dates = []
    cols.append('date_listed')
    for job_elem in job_elems:
        dates.append(extract_date_indeed(job_elem))
    extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])

    return jobs_list, num_listings


def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', class_='jobTitle')
    title = title_elem.text.strip()
    return title[3:]


def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='companyName')
    company = company_elem.text.strip()
    return company


def extract_blurb_indeed(job_elem):
    blurb_elem = job_elem.find('li')
    blurb = blurb_elem.text.strip()
    return blurb


def extract_link_indeed(job_elem):
    link = job_elem.find('a')['href']
    link = 'https://www.indeed.com' + link
    return link


def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date[6:]
