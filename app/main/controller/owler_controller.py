# import os
# import sys
#
# import pandas as pd
#
# from ..util.owler_thread import execute
# from flask_restplus import Resource
# from flask import request, send_file, abort
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage
# from ..util.dto import OwlerDto
# from ..service.owler_service import crawl_by_url,crawl_by_file
# from ..service.constant_service import ConstantService
#
# api = OwlerDto.api
# upload_parser = api.parser()
# upload_parser.add_argument('file', location='files', type=FileStorage)
#
#
# @api.route('/crawlUrl')
# class OwlerCrawlUrlController(Resource):
#     @api.doc(params={'url': {'description': 'owler url', 'in': 'query', 'type': 'str'}})
#     def get(self):
#         url = request.args.get('url')
#         if request.args.get('url', None) == None:
#             return {
#                 "status": False,
#                 "message": "Sorry! Invalid Command please enter company owler url."
#             }
#         rl(url)
#         res = rl(url)
#         if res is True:
#             pass
#         else:
#             return {
#                 "status": False,
#                 "message": "Sorry! Invalid Command please enter company owler url.",
#             }
#         owler_data = crawl_by_url(url)
#         return {
#             "status": True,
#             "message": "Congratulations! Your owler url crawled successfully.",
#             "result": owler_data
#         }
#
#
# @api.route('/crawlUrls')
# class OwlerCrawlUrlsController(Resource):
#     @api.doc(params={'urls': {'description': ' owler urls', 'in': 'body', 'type': 'json', 'example': {"urls": ["owler_url1", "owler_url2"]}}})
#     def post(self):
#         data = request.get_json()
#         owler_data_list = []
#         for url in data['urls']:
#             uls(url)
#             res = uls(url)
#             if res is True:
#                 pass
#             else:
#                 return {
#                     "status": False,
#                     "message": "Sorry! Invalid Command please enter company owler url.",
#                 }
#             owler_data_list.append(crawl_by_url(url))
#
#         return {
#             "status": True,
#             "message": "Congratulations! Your  owler urls crawled on owler successfully.",
#             "result": owler_data_list
#         }
#
#
# @api.route('/crawlFile')
# @api.expect(upload_parser)
# class OwlerCrawlUrlController(Resource):
#     # @api.doc(params={'file': {'description': 'dnd urls in file', 'in': 'files', 'type': 'file'}})
#     def post(self):
#         if 'file' not in request.files:
#             return {
#                 "status": False,
#                 "message": "Sorry! file not passed.",
#             }
#         file = request.files['file']
#
#         # If the user does not select a file, the browser submits an
#         if file.filename == '':
#             return {
#                 "status": False,
#                 "message": "Sorry! file not passed.",
#             }
#         file_path = ConstantService.data_in_path() + '/' + file.filename
#         file.save(file_path)
#         owler_validation(file_path)
#         res = owler_validation(file_path)
#         if res is True:
#             pass
#         else:
#             os.remove(file_path)
#             return {
#                 "status": False,
#                 "message": "Column Name Should be -  Urls, urls anyone at once! file not passed",
#             }
#         out_path = ConstantService.fetched_scraped_data()
#         output_file_name = execute(file_path, out_path)
#         # output_file_name = crawl_by_file(file_path)
#
#         return {
#             "status": True,
#             "message": "Congratulations! Your list of dnd urls crawled successfully owler.",
#             "download_link": "http://" + ConstantService.server_host() + "/owler/download?output_file_name=" + output_file_name
#         }
#
#
# @api.route('/download')
# class OwlerCrawlUrlController(Resource):
#     @api.doc(params={'output_file_name': {'description': 'owler crawled data output file name', 'in': 'query', 'type': 'str'}})
#     def get(self):
#         if request.args.get('output_file_name', None) == None:
#             return {
#                 "status": False,
#                 "message": "Sorry! Please insert owler crawled data output file name."
#             }
#         output_file_name = request.args.get('output_file_name')
#         down(output_file_name)
#         res = down(output_file_name)
#         if res is True:
#             pass
#         else:
#             return {
#                 "status": False,
#                 "message": "Sorry! Please insert owler crawled data output file name.",
#             }
#         out_file_path = os.path.join(ConstantService.data_processed_path(), output_file_name)
#         if os.path.exists(out_file_path):
#             return send_file(out_file_path, as_attachment=True)
#
#         abort(404, description="Crawled data not found")
#
# def owler_validation(file_path):
#     name, file_type = os.path.splitext(file_path)
#     file_type = file_type.lower()
#     if file_type in ['.xls', '.xlsx']:
#         df = pd.read_excel(file_path)
#     elif file_type == '.csv':
#         df = pd.read_csv(file_path)
#     else:
#         print("Unsupported file extension " + file_type + "! We are supporting only (csv, xls, xlsx).")
#         return False
#     url_com = ["Url", "url", "Urls", "urls"]
#     for i in df.columns:
#         if i in url_com:
#             return True
#         else:
#             return False
#
# def rl(url):
#     a = "https://www.owler.com/"
#     if a in url:
#         return True
#     else:
#          return False
#
# def uls(url):
#    a= "https://www.owler.com/"
#    if a in url:
#        return True
#    else:
#        return False
#
# def down(output_file_name):
#    a= "owler_scrapped_data_out.xlsx"
#    if a in output_file_name:
#        return True
#    else:
#        return False