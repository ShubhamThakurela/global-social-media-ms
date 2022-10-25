# import logging
# import os
# import zipfile
# from bs4 import BeautifulSoup, Comment
# import app.main.util.selenium as selenium
#
#
# def zipdir(src, dst):
#     dir_path_list = src.split("/")
#     dir_name = dir_path_list[len(dir_path_list) - 1]
#     zip_file_path = dst + '/' + dir_name + '_zoominfo_Data'
#     zf = zipfile.ZipFile("%s.zip" % (zip_file_path), "w", zipfile.ZIP_DEFLATED)
#     abs_src = os.path.abspath(src)
#     for dirname, subdirs, files in os.walk(src):
#         for filename in files:
#             absname = os.path.abspath(os.path.join(dirname, filename))
#             arcname = absname[len(abs_src) + 1:]
#             print('Zipping %s' % (os.path.join(dirname, filename)))
#             zf.write(absname, arcname)
#     zf.close()
#     return dir_name + '_zoominfo_Data.zip'
#
#
# def crawl_by_url(org_url):
#     try:
#         if not org_url:
#             return {}
#         zoom_soup,driver = selenium.get_content(org_url)
#         if not isinstance(zoom_soup, type(None)):
#             data_dict = extract_zoominfo_profile_page(zoom_soup)
#             data_dict["Employee_Count"] = ""
#             data_dict['Source_url'] = org_url
#             driver.close()
#             return data_dict
#     except Exception as e:
#         print(str(e))
#         logging.error(str(e))
#         return {"error": str(e)}
#
#
# def extract_zoominfo_profile_page(zoom_soup):
#     data_dict = {
#         "Name": "",
#         "Description": "",
#         "Website": "",
#         "Headquarters": "",
#         "Revenue": "",
#         "Employee_Count": "",
#         "Source_url": ""
#     }
#     try:
#         source_code = zoom_soup.get_attribute("outerHTML")
#         soup_obj = BeautifulSoup(source_code, "html.parser")
#         if not isinstance(soup_obj, type(None)):
#             cam_name = soup_obj.find(class_="company-name")
#             if not isinstance(cam_name, type(None)):
#                 data_dict['Name'] = cam_name.text
#
#             description = soup_obj.find(class_="company-description-text-content")
#             if not isinstance(description, type(None)):
#                  data_dict['Description'] = description.text
#
#             link = soup_obj.find_all(class_="content link")
#             if len(link) > 0:
#                 data_dict['Website'] = link[0].string
#
#             text_content = soup_obj.find_all(class_="icon-text-content content")
#             if len(text_content) > 0:
#                 data_dict['Headquarters'] = text_content[0].string
#             if len(text_content) > 2:
#                 data_dict['Revenue'] = text_content[2].string
#
#     except Exception as e:
#         print(str(e))
#         logging.error(str(e))
#         return None
#     else:
#         return data_dict
