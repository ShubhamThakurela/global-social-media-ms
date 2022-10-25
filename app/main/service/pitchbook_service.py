import shutil
from datetime import datetime
import os
import re
import time
import logging
import requests
import zipfile
import pandas as pd
from bs4 import BeautifulSoup
import app.main.util.proxy as proxy
from ..database.connection import insert_update_scraping_detail, insert_update_pitchbook_scrapped_data


def zipdir(src, dst):
    dir_path_list = src.split("/")
    dir_name = dir_path_list[len(dir_path_list) - 1]
    zip_file_path = dst + '/' + dir_name + '_pitchbook_Data'
    zf = zipfile.ZipFile("%s.zip" % (zip_file_path), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print('Zipping %s' % (os.path.join(dirname, filename)))
            zf.write(absname, arcname)
    zf.close()
    return dir_name + '_pitchbook_Data.zip'


def crawl_by_file(url_list, file_path):
    # Start time
    start_time = time.time()

    data_list = []
    # url_list = get_url_to_scrap(file_path)
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

    # return output_file_name + '.csv'


def get_url_to_scrap(file_path):
    url_list = []
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        return url_list

    print("Processing File... " + str(file_path))
    logging.info("Started pitchbook get urls for " + file_path)

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
        elif 'pitchbookurl' in j:
            url = str(j['pitchbookurl'])
        elif 'PitchbookUrl' in j:
            url = str(j['PitchbookUrl'])
        elif 'Website' in j:
            url = str(j['Website'])
        elif 'website' in j:
            url = str(j['website'])

        url = str(url).replace(" ", "")
        if url == 'nan' or url == '-' or url == '':
            continue

        url_list.append(prepare_http_url(url))

    return url_list


def crawl_by_url(pitch_url):
    try:
        referer_url = "https://www.google.com"
        data_dict = {}
        logging.info("Started scraping for " + pitch_url)

        if pitch_url != "":
            pitch_response = requests.get(pitch_url, headers={'User-Agent': proxy.ua.random, 'Referer': referer_url},
                                          timeout=5)
            if pitch_response.status_code == 200:
                pitch_soup = BeautifulSoup(pitch_response.content, "html.parser")
                if not isinstance(pitch_soup, type(None)):
                    data_dict = extract_pitchbook_profile_page(pitch_soup, pitch_url, )
                    data_dict['source_url'] = pitch_url
        return data_dict

    except Exception as e:
        print(str(e))
        # log_error('+++++ Pitchbook: fetch data +++++')
        logging.error(str(e))
        return {}
    else:
        return org_data


def extract_pitchbook_url(soup):
    pitchbook_url = ""
    try:
        links_section = soup.find("div", {"id": "links"})
        if not isinstance(links_section, type(None)):
            results_section = links_section.find_all("div",
                                                     {"class": "result results_links results_links_deep web-result"})
            if not isinstance(results_section, type(None)):
                for result_section in results_section:
                    result_title = result_section.find("h2", {"class": "result__title"})
                    if not isinstance(result_title, type(None)):
                        result_a_section = result_title.find("a", {"class": "result__a"})
                        if not isinstance(result_a_section, type(None)):
                            result_href = result_a_section.get("href")
                            if "pitchbook.com/profiles/company" in result_href:
                                pitchbook_url = data_clean(result_href)
                                break
    except Exception as e:
        print(str(e))
        logging.error(str(e))

    return pitchbook_url


def extract_pitchbook_profile_page(soup, pitch_url):
    pitch_dict = {}
    pitchbook_dict = {
        "company_name": '',
        "Website": '',
        "Founded": '',
        "Status": '',
        "Employees": '',
        "Revenue": '',
        "Net_Income": '',
        "About_Us": '',
        "Ownership_Status": '',
        "Financing_Status": '',
        "Primary_Industry": '',
        "Primary_Office": '',
        "Address": '',
        "Source_Url": '',
        "start_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_dt": '',
    }
    org_data = {
        "company_name": '',
        "website": '',
        "source": '',
        "source_url": '',
        "start_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_dt": '',
    }
    try:

        main_section = soup.find("div", {"role": "main"})
        if not isinstance(main_section, type(None)):
            overview_section = main_section.find("div", {"id": "overview"})
            if not isinstance(overview_section, type(None)):
                quick_facts_section = overview_section.find("div", {"role": "list"})
                if not isinstance(quick_facts_section, type(None)):
                    list_items = quick_facts_section.find_all("div", {"role": "listitem"})
                    if not isinstance(list_items, type(None)):
                        for item in list_items:
                            item_ul = item.find("ul")
                            if not isinstance(item_ul, type(None)):
                                item_li = item_ul.find_all("li")
                                key = data_clean(item_li[0].get_text())
                                value = data_clean(item_li[1].get_text())
                                pitch_dict[key] = value

            table_data = main_section.find("div", {"id": "financials"})
            if not isinstance(table_data, type(None)):
                trdata = table_data.tbody.find_all('tr')
                if not isinstance(trdata, type(None)):
                    list_item = []
                    for row in trdata:
                        list_item.append(row.find_all('td')[2].string)
                    pitch_dict["Revenue"] = list_item[1]
                    pitch_dict["Net_Income"] = list_item[3]

            general_information_section = main_section.find("div", {"aria-label": "Company General information"})
            if not isinstance(general_information_section, type(None)):
                definition_section = general_information_section.find("div", {"role": "definition"})
                if not isinstance(definition_section, type(None)):
                    definition_p = definition_section.find_all("p")
                    if len(definition_p) > 0:
                        about_us = [data_clean(x.get_text()) for x in definition_p if
                                    x.get_text().strip() != 'Description']
                        pitch_dict['About Us'] = ' '.join(about_us)

                contact_section = general_information_section.find("div", {"class": "pp-contact-info"})
                if not isinstance(contact_section, type(None)):
                    contact_info_sections = general_information_section.find_all("div",
                                                                                 {"class": "pp-contact-info_item"})
                    if not isinstance(contact_info_sections, type(None)):
                        for contact_info in contact_info_sections:
                            # contact_info_divs = contact_info.find_all("div")
                            contact_info_divs = contact_info.find_all()
                            if len(contact_info_divs) > 1:
                                key = data_clean(contact_info_divs[0].get_text())
                                pitch_dict[key] = data_clean(contact_info_divs[1].get_text())

                    address_ul_section = general_information_section.find("ul", {"class": "list-type-none"})
                    if not isinstance(address_ul_section, type(None)):
                        contact_li_sections = address_ul_section.find_all("li")
                        if not isinstance(contact_li_sections, type(None)):
                            address = ""
                            for contact_li in contact_li_sections:
                                address += data_clean(contact_li.get_text()) + ", "
                            pitch_dict["Address"] = address.strip(", ")

                if 'Website' not in pitch_dict:
                    web_link_section = contact_section.find("a", {"aria-label": "Website link"})
                    if web_link_section:
                        pitch_dict["Website"] = web_link_section.get('href')

                if 'Company_name' not in pitch_dict:
                    class_name = soup.find("div", {"class": "XL-8 M-7 XS-12 flex-container flex-justify-between"})
                    soup_class = class_name.find("h3", {"font-color-white mb-xl-0 offset-right-S-5"})
                    if not isinstance(soup_class, type(None)):
                        pitch_dict['Company Name'] = data_clean(soup_class.get_text())

        if 'Employees' in pitch_dict:
            employees = str(pitch_dict['Employees']).replace(',', '')
            pitch_dict['Employees'] = str(employees).replace(' ', '')

        # if len('Employees') == 0 in pitchbook_dict:
        #     pitchbook_dict['Employees'] = 11

        org_data.update({
            "company_name": pitch_dict['Company Name'],
            "website": pitch_dict["Website"],
            "source": 'Pitchbook',
            "source_url": pitch_url,
            "end_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        pitchbook_dict.update({
            "company_name": pitch_dict['Company Name'],
            "Website": pitch_dict["Website"],
            "Founded": pitch_dict["Founded"],
            "Status": pitch_dict["Status"],
            # "Employees": pitchbook_dict['Employees'],
            # "Revenue": pitch_dict["Revenue"],
            # "Net_Income": pitch_dict["Net_Income"],
            "About_Us": pitch_dict["About Us"],
            "Ownership_Status": pitch_dict["Ownership Status"],
            "Financing_Status": pitch_dict["Financing Status"],
            "Primary_Industry": pitch_dict["Primary Industry"],
            "Primary_Office": pitch_dict["Primary Office"],
            "Address": pitch_dict["Address"],
            "Source_Url": pitch_url,
            "end_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        # print(pitchbook_dict)
        insert_update_scraping_detail(org_data)
        insert_update_pitchbook_scrapped_data(pitchbook_dict)
    except Exception as e:
        print(str(e))
        logging.error(str(e))

    return pitch_dict


def get_domain(url):
    url = url.rstrip('/')
    url = url.rstrip('#')
    url = url.rstrip('/')
    url = url.replace('http://', '')
    url = url.replace('https://', '')
    url = url.replace('www.', '')
    url = url.strip()
    url = url.lower()
    res = url.split('/')
    url = res[0].strip()
    url = url.split(":")[0].strip()
    return url


def prepare_linkedin_url(url):
    url = clean_url(url)
    url = url.replace('http://', 'https://')
    url = url.replace('www.', '')
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
