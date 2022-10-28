import os
import re
import time
import datetime
import logging
import requests
import zipfile
import pandas as pd
import app.main.util.proxy as proxy
from bs4 import BeautifulSoup
from datetime import datetime
from ..service.constant_service import ConstantService
from ..database.connection import insert_update_scraping_detail, insert_update_linkedin_scrapped_data


def crawl_by_file(url_list, file_path):
    start_time = time.time()
    data_list = []
    counter = 1
    for url in url_list:
        print(str(counter) + " - Url... " + str(url))
        data_list.append(crawl_by_url(url))
        counter += 1
    return data_list


def data_to_file(df, output_file_name, out_path):
    file_path = out_path + '/'
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    df.to_csv(file_path + output_file_name + '.csv')


def zipdir(src, dst):
    dir_path_list = src.split("/")
    dir_name = dir_path_list[len(dir_path_list) - 1]
    zip_file_path = dst + '/' + dir_name + '_linkedin_Data'
    zf = zipfile.ZipFile("%s.zip" % (zip_file_path), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print('Zipping %s' % (os.path.join(dirname, filename)))
            zf.write(absname, arcname)
    zf.close()
    return dir_name + '_linkedin_Data.zip'


def get_url_to_scrap(file_path):
    url_list = []
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        return url_list

    print("Processing File... " + str(file_path))

    # Check file type
    name, file_type = os.path.splitext(file_path)
    file_type = file_type.lower()

    # Read file on the basis of type
    if file_type in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    elif file_type == '.csv':
        df = pd.read_csv(file_path)
    else:
        print("Unsupported file extension " + file_type + "! We are supporting only (csv, xls, xlsx).")
        return url_list

    for i, j in df.iterrows():
        url = ''
        if 'Url' in j:
            url = str(j['Url'])
        elif 'url' in j:
            url = str(j['url'])
        elif 'linkedinurl' in j:
            url = str(j['linkedinurl'])
        elif 'LinkedinUrl' in j:
            url = str(j['LinkedinUrl'])

        url = str(url).replace(" ", "")
        if url == 'nan' or url == '-' or url == '':
            continue

        url_list.append(prepare_http_url(url))

    return url_list


def crawl_by_url(linkedin_url):
    try:
        if not linkedin_url:
            return {"Linkedin_url not Matched"}
        retry = ConstantService.get_max_retry()
        result = None
        linkedin_data = {}
        logging.info("Started linkedin urls scraping for " + linkedin_url)
        while retry > 0 and (result is None or result.status_code != 200):
            url = prepare_linkedin_url(linkedin_url, 'GUEST')
            result = http_get_request(url)
            if result is None or result.status_code != 200:
                url = prepare_linkedin_url(linkedin_url, 'SHOWCASE')
                result = http_get_request(url)
                if result is None or result.status_code != 200:
                    url = prepare_linkedin_url(linkedin_url, '')
                    result = http_get_request(url)
            retry -= 1
        if result and result.status_code == 200:
            linkedin_data = process_response(result, url)

    except Exception as e:
        return {"error": str(e)}
    else:
        logging.info("Completed linkedin urls scraping for " + linkedin_url)
        return linkedin_data


def http_get_request(url):
    headers = {
        'User-Agent': proxy.ua.random,
        'Referer': 'https://www.linkedin.com',
        'Accept-Language': '*'
    }
    http_result = None
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        try:
            response = requests.get(url, headers=headers, proxies=proxy.get_proxy(), timeout=5)
        except Exception as e:
            # logging.error('+++++ LinkedIn: Fetch linkedin data +++++')
            logging.error(str(e))
        else:
            http_result = response
    else:
        http_result = response

    return http_result


def process_response(response, url):
    linkedin_data = {}
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        if not isinstance(soup, type(None)):
            linkedin_data = extract_linkedin_public_page(soup, url)
            if len(linkedin_data):
                linkedin_data.update({"source_url": url})
                linkedin_data.update({"source": 'linkedin'})

    return linkedin_data


def extract_linkedin_public_page(soup, url):
    # Initialize the data dict
    data_dict = {
        'Company_Name': '',
        'Website': '',
        'Industries': '',
        'Headquarters': '',
        'Employee_Count': '',
        'Type': '',
        'Founded': '',
        'Specialties': '',
        'About_Us': '',
        'Address': '',
        'Funding_Rounds': '',
        'Last_Funding_On': '',
        'Last_Funding_Value': '',
        'Investors': '',
        'Permalink': '',
        'Company Size': '',
        'Source_Url': '',
    }
    org_data = {
        "company_name": '',
        "website": '',
        "source": '',
        "source_url": '',
        "start_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_dt": '',
    }
    linkedin_data_dict = {
        'Company_Name': '',
        'Website': '',
        'Industries': '',
        'Headquarters': '',
        'Employee_Count': '',
        'Specialties': '',
        'About_Us': '',
        'Address': '',
        'CompanyType': '',
        'FundingRounds': '',
        'LastFundingOn': '',
        'LastFundingValue': '',
        'Investors': '',
        'Permalink': '',
        'CompanySize': '',
        "start_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_dt": '',
    }
    try:
        top_card_section = soup.find("section", {"class": "top-card-layout"})
        if not isinstance(top_card_section, type(None)):
            top_card_layout = top_card_section.find("div", {"class": "top-card-layout__entity-info-container"})
            if not isinstance(top_card_layout, type(None)):
                top_card_layout_entity = top_card_layout.find("div", {"class": "top-card-layout__entity-info"})
                if not isinstance(top_card_layout_entity, type(None)):
                    company_name_obj = top_card_layout_entity.find("h1", {"class": "top-card-layout__title"})
                    if not isinstance(company_name_obj, type(None)):
                        data_dict['Company_Name'] = data_clean(company_name_obj.get_text())

                top_card_layout_entity_right = top_card_layout.find("div", {
                    "class": "top-card-layout__entity-info--right-column"})
                if not isinstance(top_card_layout_entity_right, type(None)):
                    linked_emp_obj = top_card_layout_entity_right.find("a", {
                        "data-tracking-control-name": "org-employees_cta_face-pile-cta"})
                    if linked_emp_obj is None:
                        linked_emp_obj = top_card_layout_entity_right.find("a", {
                            "data-tracking-control-name": "org-employees_cta"})
                    if not isinstance(linked_emp_obj, type(None)):
                        emp_linkedin = data_clean(linked_emp_obj.get_text())
                        emp_linkedin = emp_linkedin.replace(',', '')
                        res = [int(i) for i in emp_linkedin.split() if i.isdigit()]
                        if len(res):
                            data_dict['Employee_Count'] = res[0]
        about_section = soup.find("section", {"class": ["artdeco-card p5 mb4", "about-us", "core-section-container"]})
        if not isinstance(about_section, type(None)):
            about_us_obj = about_section.find("p",
                                              {"class": ["break-words whitespace-pre-wrap", "about-us__description"],
                                               "data-test-id": "about-us__description"})
            if not isinstance(about_us_obj, type(None)):
                data_dict['About_Us'] = about_us_obj.get_text()

            # Comment Out Because of data not inserting to the mysql
            basic_info = about_section.find("dl", {"class": ["mt-6", "about-us__basic-info-list"]})
            if not isinstance(basic_info, type(None)):
                basic_info_list = basic_info.findAll("div")
                for div_data in basic_info_list:
                    basic_info_dt = div_data.find("dt")
                    basic_info_dd = div_data.find("dd")
                    if not isinstance(basic_info_dt, type(None)) and not isinstance(basic_info_dd, type(None)):
                        key = data_clean(basic_info_dt.get_text())
                        value = data_clean(basic_info_dd.get_text())
                        data_dict[key.title()] = value
                        # print('sbsudgsld')
                    # data_dict['Industries'] = data_dict[key.title()]
        Columns_section1 = about_section.find("dd", {
            "class": ["font-sans text-md text-color-text break-words overflow-hidden"]})
        if not isinstance(Columns_section1, type(None)):
            data_dict['Website'] = data_clean(Columns_section1.get_text())

        location_section = soup.find("section", {"class": [
            "core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 locations",
            "locations"]})
        if not isinstance(location_section, type(None)):
            location_obj = location_section.find("li", {
                "class": ["mb-3 papabear:w-50% papabear:odd:mr-2 papabear:odd:w-[calc(50%-16px)]",
                          "locations__location"]})
            if not isinstance(location_obj, type(None)):
                addresses = ''
                for address in location_obj.findAll("p"):
                    if not isinstance(address, type(None)):
                        addresses += address.get_text().strip() + ", "
                data_dict['Address'] = data_clean(addresses.rstrip(', '))

        right_rail = soup.find("section", {"class": "right-rail"})
        if not isinstance(right_rail, type(None)):
            funding_section = right_rail.find("section", {"data-test-id": "funding"})
            if not isinstance(funding_section, type(None)):
                basic_info = funding_section.find(True, {
                    "class": ["aside-section-container__content break-words", "funding__basic-info"]})
                if not isinstance(basic_info, type(None)):
                    funding_basic_info = basic_info.find(True,
                                                         {"class": ["before:middot", "funding__basic-info-rounds"]})
                    if not isinstance(funding_basic_info, type(None)):
                        funding_basic_info_data = data_clean(funding_basic_info.get_text())
                        data_dict['Funding_Rounds'] = int(''.join(filter(str.isdigit, funding_basic_info_data)))
                last_funding_section = funding_section.find(True, {
                    "class": ["my-2", "funding__last-round funding__info-container"]})
                if not isinstance(last_funding_section, type(None)):
                    last_funding_date_section = last_funding_section.find(True, {
                        "class": ["link-styled text-sm mb-1 inline-block !text-color-text-secondary",
                                  "funding__last-round-link funding__external-link"]})
                    if not isinstance(last_funding_date_section, type(None)):
                        last_funding_date = last_funding_date_section.find(True, {
                            "class": ["before:middot", "funding__last-round-date"]})
                        if not isinstance(last_funding_date, type(None)):
                            data_dict['Last_Funding_On'] = data_clean(last_funding_date.get_text())
                    last_funding_raised = last_funding_section.find(True, {
                        "class": ["text-display-lg", "funding__last-round-money-raised"]})
                    if not isinstance(last_funding_raised, type(None)):
                        data_dict['Last_Funding_Value'] = data_clean(last_funding_raised.get_text())
                funding_investors_section = funding_section.find(True, {
                    "class": ["mb-2", "funding__investors funding__info-container"]})
                if not isinstance(funding_investors_section, type(None)):
                    funding_investors = funding_investors_section.find_all("a", {"class": [
                        "flex text-sm items-center mb-1 link-styled text-sm mb-1 inline-block "
                        "!text-color-text-secondary",
                        "funding__investors-link funding__external-link"]})
                    investors = ""
                    for funding_investor in funding_investors:
                        if not isinstance(funding_investor, type(None)):
                            investors += data_clean(funding_investor.get_text()) + ", "
                    data_dict['Investors'] = investors.strip(", ")
                crunchbase_section = funding_section.find("a", {"class": ["btn-md btn-secondary inline-block mb-0.5",
                                                                          "funding__crunchbase-link funding__external-link"]})
                crunchbase_uri = re.findall('[^/]+(?=/$|$)', crunchbase_section.get('href'))
                crunchbase_uri_list = crunchbase_uri[0].split("?")
                if len(crunchbase_uri_list):
                    data_dict['Permalink'] = data_clean(crunchbase_uri_list[0])

        # If website not present on linkedin page, check soe site
        if data_dict['Website'] == '' and 'Site' in data_dict:
            data_dict['Website'] = data_dict['Site']
        # print(data_dict)
        org_data.update({
            "company_name": data_dict['Company_Name'],
            "website": data_dict['Website'],
            "source": 'linkedin',
            "source_url": url,
            "end_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        linkedin_data_dict.update({
            'Company_Name': data_dict['Company_Name'],
            'Website': data_dict['Website'],
            'Industries': data_dict['Industries'],
            'Headquarters': data_dict['Headquarters'],
            'Employee_Count': data_dict['Employee_Count'],
            'Specialties': data_dict['Specialties'],
            'About_Us': data_dict['About_Us'],
            'Address': data_dict['Address'],
            'CompanyType': data_dict['Type'],
            'FundingRounds': data_dict['Funding_Rounds'],
            'LastFundingOn': data_dict['Last_Funding_On'],
            'LastFundingValue': data_dict['Last_Funding_On'],
            'Investors': data_dict['Investors'],
            'Permalink': data_dict['Permalink'],
            'CompanySize': data_dict['Company Size'],
            'end_dt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Source_Url': url,
        })
        insert_update_scraping_detail(org_data)
        insert_update_linkedin_scrapped_data(linkedin_data_dict)
    except Exception as e:
        print(str(e))
        # log_error(str(e))
    return data_dict


def prepare_linkedin_url(url, url_type):
    if url_type == 'GUEST':
        if 'organization-guest' not in url:
            url = url.replace('http://', 'https://')
            url = url.replace('/company/', '/organization-guest/company/')

    elif url_type == 'SHOWCASE':
        if 'organization-guest' in url:
            url = url.replace('/organization-guest/company/', '/showcase/')
        else:
            url = url.replace('/company/', '/showcase/')
    else:
        url = clean_url(url)
        url = url.replace('http://', 'https://')
        url = url.replace('company-beta', 'company')
        url = url.replace('/cws/', '/organization-guest/company/')
    return url


def data_clean(y):
    if type(y) == str:
        y = " ".join(re.findall("[a-zA-Z0-9._^%₹$#!~@,-:;&*()='}{|\/]+", y))
    elif type(y) == bytes:
        y = y.strip()
        y = y.replace(b'\xa0', b'')

    return y


def clean_url(url):
    url = url.rstrip('/')
    url = url.rstrip('#')
    url = url.rstrip('/')
    url = url.strip()
    url = url.lower()
    return url


def prepare_http_url(url):
    url = url.replace('http://', '')
    url = url.replace('https://', '')
    url = url.replace('www.', '')
    url = url.strip()
    url = url.strip('/')
    return 'http://www.' + url


def illegal_char_remover(data):
    # ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\uffff]')
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    """Remove ILLEGAL CHARACTER."""
    if isinstance(data, str):
        return ILLEGAL_CHARACTERS_RE.sub("", data)
    else:
        return data



