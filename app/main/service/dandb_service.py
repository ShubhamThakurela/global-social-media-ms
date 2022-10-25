# import re
# import time
# import os, shutil
# import pandas as pd
# import logging
# from selenium import webdriver
# import zipfile
# from bs4 import BeautifulSoup, Comment
# import undetected_chromedriver as uc
# from ..database.connection import insert_update_scraping_detail
# from datetime import datetime
#
# def zipdir(src, dst):
#     dir_path_list = src.split("/")
#     dir_name = dir_path_list[len(dir_path_list) - 1]
#     zip_file_path = dst + '/' + dir_name + '_dnb_Data'
#     zf = zipfile.ZipFile("%s.zip" % zip_file_path, "w", zipfile.ZIP_DEFLATED)
#     abs_src = os.path.abspath(src)
#     for dirname, subdirs, files in os.walk(src):
#         for filename in files:
#             absname = os.path.abspath(os.path.join(dirname, filename))
#             arcname = absname[len(abs_src) + 1:]
#             print('Zipping %s' % (os.path.join(dirname, filename)))
#             zf.write(absname, arcname)
#     zf.close()
#     return dir_name + '_dnb_Data.zip'
#
#
# def crawl_by_file(url_list, file_path):
#     # Start time
#     start_time = time.time()
#     data_list = []
#     # url_list = get_url_to_scrap(file_path)
#     counter = 1
#     for url in url_list:
#         print(str(counter) + " - Url... " + str(url))
#         data_list.append(crawl_by_url(url))
#         counter += 1
#     return data_list
#
#
# def data_to_file(df, output_file_name, out_path):
#     file_path = out_path + '/'
#     if not os.path.exists(os.path.dirname(file_path)):
#         os.makedirs(os.path.dirname(file_path))
#
#     df.to_csv(file_path + output_file_name + '.csv')
#     return output_file_name + '.csv'
#
#
# def get_url_to_scrap(file_path):
#     url_list = []
#     if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
#         return url_list
#
#     print("Processing File... " + str(file_path))
#     logging.info("Started dnb get urls for " + file_path)
#
#     # Check file type
#     name, file_type = os.path.splitext(file_path)
#     file_type = file_type.lower()
#
#     # Read file on the basis of type
#     if file_type in ['.xls', '.xlsx']:
#         df = pd.read_excel(file_path)
#     elif file_type == '.csv':
#         df = pd.read_csv(file_path)
#     else:
#         print("Unsupported file extension " + file_type + "! We are supporting only (csv, xls, xlsx).")
#         return url_list
#
#     for i, j in df.iterrows():
#         url = ''
#         if 'Url' in j:
#             url = str(j['Url'])
#         elif 'url' in j:
#             url = str(j['url'])
#         elif 'dnburl' in j:
#             url = str(j['dnburl'])
#         elif 'DnBurl' in j:
#             url = str(j['DnBUrl'])
#         elif 'Website' in j:
#             url = str(j['Website'])
#         elif 'website' in j:
#             url = str(j['website'])
#
#         url = str(url).replace(" ", "")
#         if url == 'nan' or url == '-' or url == '':
#             continue
#
#         url_list.append(prepare_http_url(url))
#
#     return url_list
#
#
# def prepare_http_url(url):
#     url = url.replace('http://', '')
#     url = url.replace('https://', '')
#     url = url.replace('www.', '')
#     url = url.strip()
#     url = url.strip('/')
#     return 'http://www.' + url
#
#
# def crawl_by_url(org_url):
#     try:
#         data_dict = {}
#         if not org_url:
#             return {}
#         zoom_soup,driver = get_by_selenium(org_url)
#         if not isinstance(zoom_soup, type(None)):
#             data_dict = extract_dandb_profile_page(zoom_soup,org_url)
#             data_dict['Source_url'] = org_url
#             driver.close()
#             return data_dict
#         return data_dict
#     except Exception as e:
#         return {"error": str(e)}
#
#
# def get_by_selenium(org_url, stime=10):
#     try:
#         options = webdriver.ChromeOptions()
#         options.add_argument('--ignore-certificate-errors')
#         options.add_argument('--headless')
#         options.add_argument('--disable-infobars')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--remote-debugging-port=9222')
#         driver = uc.Chrome(options=options)
#         driver.get(org_url)
#         driver.refresh()
#         time.sleep(stime)
#         content = driver.find_element('xpath', '/html/body')
#     except Exception as e:
#         print(str(e))
#         return None
#     else:
#         return content, driver
#
#
# def extract_dandb_profile_page(dandb_soup, org_url):
#     data_dict1 = {
#         "Name": "",
#         "Description": "",
#         "Website": "",
#         "Headquarters": "",
#         "Country": "",
#         "Revenue": "",
#         "Net_Profit": "",
#         "Employee_Count": "",
#         "Industry": "",
#         "Source_url": ""
#     }
#     data_dict = {
#         "company_name": '',
#         "website": '',
#         "source": '',
#         "source_url": '',
#         "start_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "end_dt": '',
#     }
#     try:
#         source_code = dandb_soup.get_attribute("outerHTML")
#         soup = BeautifulSoup(source_code, "html.parser")
#         if not isinstance(soup, type(None)):
#             name = soup.find(class_="company-profile-header-title")
#             if not isinstance(name, type(None)):
#                 data_dict1['Name'] = name.text
#
#             industry_links = soup.find("span", {"name": "industry_links"})
#             if not isinstance(industry_links, type(None)):
#                 industry_links_spam = industry_links.find_all("span")
#                 if not isinstance(industry_links_spam, type(None)):
#                     text1 = industry_links_spam[0].text.strip()
#                     data_dict1['Industry'] = data_clean(text1)
#
#             company_website = soup.find("span", {"name": "company_website"})
#             if not isinstance(company_website, type(None)):
#                 company_website = company_website.find("span")
#                 if not isinstance(company_website, type(None)):
#                     for a in company_website.find_all('a', href=True):
#                         link = a['href']
#                     data_dict1['Website'] = link
#
#             address_section2 = soup.find("span", {"name": "company_address"})
#             if not isinstance(address_section2, type(None)):
#                 address_section2 = address_section2.find_all("span")
#                 if not isinstance(address_section2, type(None)):
#                     address = address_section2[0].text.strip()
#                     if not isinstance(address, type(None)):
#                          data_dict1['Headquarters'] = address.split('\n')[0]
#
#             revenue_in_us_dollar = soup.find("span", {"name": "revenue_in_us_dollar"})
#             if not isinstance(revenue_in_us_dollar, type(None)):
#                 revenue_in_us_dollar = revenue_in_us_dollar.find_all("span")
#                 if not isinstance(revenue_in_us_dollar, type(None)):
#                     data_dict1['Revenue'] = revenue_in_us_dollar[0].text
#         data_dict.update({
#             "company_name": data_dict1['Name'],
#             "website": data_dict1['Website'],
#             "source": 'd&b',
#             "source_url": org_url,
#             "end_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         })
#         insert_update_scraping_detail(data_dict)
#         return data_dict1
#
#     except Exception as e:
#         logging.error(str(e))
#         return None
#
# def data_clean(y):
#     if type(y) == str:
#         y = " ".join(re.findall("[a-zA-Z0-9._^%₹$#!~@,-:;&*()='}{|\/]+", y))
#     elif type(y) == bytes:
#         y = y.strip()
#         y = y.replace(b'\xa0', b'')
#
#     return y
#
#
# def illegal_char_remover(data):
#     # ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\uffff]')
#     ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
#     """Remove ILLEGAL CHARACTER."""
#     if isinstance(data, str):
#         return ILLEGAL_CHARACTERS_RE.sub("", data)
#     else:
#         return data