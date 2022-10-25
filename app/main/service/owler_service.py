# from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
# from bs4 import BeautifulSoup, Comment
# import logging
# import zipfile
# import time, os, shutil
# import pandas as pd
# import re
# import undetected_chromedriver as uc
# from ..service.constant_service import ConstantService
#
# def zipdir(src, dst):
#     dir_path_list = src.split("/")
#     dir_name = dir_path_list[len(dir_path_list) - 1]
#     zip_file_path = dst + '/' + dir_name + '_owler_Data'
#     zf = zipfile.ZipFile("%s.zip" % (zip_file_path), "w", zipfile.ZIP_DEFLATED)
#     abs_src = os.path.abspath(src)
#     for dirname, subdirs, files in os.walk(src):
#         for filename in files:
#             absname = os.path.abspath(os.path.join(dirname, filename))
#             arcname = absname[len(abs_src) + 1:]
#             print('Zipping %s' % (os.path.join(dirname, filename)))
#             zf.write(absname, arcname)
#     zf.close()
#     return dir_name + '_owler_Data.zip'
#
#
# def crawl_by_file(url_list, file_path):
#     # Start time
#     start_time = time.time()
#
#     data_list = []
#     # url_list = get_url_to_scrap(file_path)
#     counter = 1
#     for url in url_list:
#         print(str(counter) + " - Url... " + str(url))
#         data_list.append(crawl_by_url(url))
#         counter += 1
#
#     # Save result as excel
#     # output_file_name = data_to_file(data_list, 'owler_scrapped_data_out')
#     #
#     # # Move file to processed after completed the process
#     # if not os.path.exists(os.path.dirname(ConstantService.data_processed_path())):
#     #     os.makedirs(os.path.dirname(ConstantService.data_processed_path()))
#     # shutil.move(file_path, os.path.join(ConstantService.data_processed_path(), os.path.basename(file_path)))
#
#     # End Time
#     # end_time = time.time()
#     # print("Processing Time: ", '{:.3f} sec'.format(end_time - start_time))
#
#     return data_list
#
#
# def data_to_file(df, output_file_name, out_path):
#     file_path = out_path + '/'
#     if not os.path.exists(os.path.dirname(file_path)):
#         os.makedirs(os.path.dirname(file_path))
#
#     # writer = pd.ExcelWriter(file_path + output_file_name + '.xlsx')
#     # df = pd.DataFrame.from_dict(data_set)
#     # df = df.applymap(illegal_char_remover)
#     # df.to_excel(writer, sheet_name='owler', index=False)
#     # writer.save
#     df.to_csv(file_path + output_file_name + '.csv')
#
#     # return output_file_name + '.csv'
#
#     # return output_file_name + '.xlsx'
#
#
# def get_url_to_scrap(file_path):
#     url_list = []
#     if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
#         return url_list
#
#     print("Processing File... " + str(file_path))
#     logging.info("Started owler get urls for " + file_path)
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
#         elif 'owleraurl' in j:
#             url = str(j['owlerurl'])
#         elif 'OwlerUrl' in j:
#             url = str(j['OwlerUrl'])
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
#
# def crawl_by_url(org_url):
#     try:
#         if not org_url:
#             return {}
#
#         owler_soup, driver = get_by_selenium(org_url)
#         if not isinstance(owler_soup, type(None)):
#             data_dict = extract_owlerinfo_profile_page(owler_soup, org_url)
#             driver.close()
#             return data_dict
#         else:
#             return {}
#     except Exception as e:
#         print(str(e))
#         # logging.error(str(e))
#         return {"error": str(e)}
#
# def get_by_selenium(org_url, stime=10):
#     try:
#         options = webdriver.ChromeOptions()
#         options.add_argument('--ignore-certificate-errors')
#         options.add_argument('--headless')
#         options.add_argument('--disable-infobars')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--no-sandbox')
#         # options.add_argument('--remote-debugging-port=9222')
#         # options.add_argument('user-agent={0}'.format(ConstantService.get_user_agent()))
#         # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
#         # options.user_data_dir = r"C:\Users\User\AppData\Local\Google\Chrome\User Data\Default"
#         # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
#         driver = uc.Chrome(options=options)
#         # driver = webdriver.Chrome(executable_path=ConstantService.get_chrome_path(), chrome_options=options)
#         driver.get(org_url)
#         time.sleep(stime)
#         content = driver.find_element('xpath', '/html/body')
#     except Exception as e:
#         print(str(e))
#         return None
#     else:
#         return content,driver
#
# def extract_owlerinfo_profile_page(owler_soup, org_url):
#     try:
#         data_dict = {
#             "Name": "",
#             "Website": "",
#             "Headquarter": "",
#             "Country": "",
#             "Revenue": "",
#             "Net profit": "",
#             "Employee Count": "",
#             "Description": "",
#             "Industry": "",
#             "Source url": "",
#         }
#         source_code = owler_soup.get_attribute("outerHTML")
#         soup_obj = BeautifulSoup(source_code, "html.parser")
#         data_dict.update({
#             "Source url": org_url
#         })
#
#         if not isinstance(soup_obj, type(None)):
#             description_div = soup_obj.find('div', {'class': "header-description"})
#             #print(description_div)
#             if not isinstance(description_div, type(None)):
#                 company_name = description_div.find('h1', {'class': "company-name"})
#                 if not isinstance(company_name, type(None)):
#                     data_dict.update({
#                         "Name": company_name.text
#                     })
#                 description_det = description_div.find_all('p', {'class': "description"})
#                 for description_detail in description_det:
#                     if not isinstance(description_detail, type(None)):
#                         data_dict.update({
#                             "Description": description_detail.text
#                         })
#             if not isinstance(soup_obj, type(None)):
#                 website_div = soup_obj.find('div', {'class': "website-info flex center"})
#                 if not isinstance(website_div, type(None)):
#                     website_link = website_div.find('div', {'class': "website"})
#                     if not isinstance(website_link, type(None)):
#                         data_dict.update({
#                             "Website": website_link.text
#                 })
#
#                 address_div = soup_obj.find('div', {'class': "location"})
#                 if not isinstance(address_div, type(None)):
#                     head_quarter= address_div.find('span', {'itemprop': "address"})
#                     if not isinstance(head_quarter, type(None)):
#                         data_dict.update({
#                             "Headquarter": head_quarter.text
#                     })
#
#
#                 category_div = soup_obj.find('div', {'class': "company-info-block-wrapper"})
#                 if not isinstance(category_div, type(None)):
#                     revenue_lis = category_div.find('div', {'class': "company-statistics-v2 REVENUE_EXACT CP"})
#                     if not isinstance(revenue_lis, type(None)):
#                         revenue_total = revenue_lis.find('div', {'class': "count-container REVENUE_EXACT CP botifyrevenuedata"})
#                         if not isinstance(revenue_total, type(None)):
#                             data_dict.update({
#                                 "Revenue": revenue_total.text
#                         })
#                     industries = category_div.find('div', {'class': "sectors"})
#                     if not isinstance(industries, type(None)):
#                         data_dict.update({
#                             "Industry": industries.text
#                         })
#
#
#                 if not isinstance(category_div, type(None)):
#                     employee = category_div.find('div', {'class': "company-statistics-v2 EMPLOYEE_EXACT CP"})
#                     if not isinstance(employee, type(None)):
#                         employee_total = employee.find('div', {'class': "count-container"})
#                         if not isinstance(employee_total, type(None)):
#                             data_dict.update({
#                                             "Employee Count": employee_total.text
#                     })
#
#
#
#     except Exception as e:
#         print(str(e))
#         return None
#     else:
#         return data_dict
#
#
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