# import os
# import sys
# from flask import request, send_file, abort
# from flask_restplus import Resource
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage
# from ..util.dto import ZoominfoDto
# from ..service.zoominfo_service import crawl_by_url
# from ..service.constant_service import ConstantService
#
# api = ZoominfoDto.api
# upload_parser = api.parser()
# upload_parser.add_argument('file', location='files', type=FileStorage)
#
#
# """"@api.route('/crawlUrl')
# class ZoominfoCrawlUrlController(Resource):
#     @api.doc(params={'url': {'description': 'zoominfo url', 'in': 'query', 'type': 'str'}})
#     def get(self):
#         url = request.args.get('url')
#         if request.args.get('url', None) == None:
#             return {
#                 "status": False,
#                 "message": "Sorry! Invalid Command please enter company zoominfo url."
#             }
#         rl(url)
#         res = rl(url)
#         if res is True:
#             pass
#         else:
#             return {
#                 "status": False,
#                 "message": "Sorry! Invalid Command please enter company zoominfo url.",
#             }
#         zoominfo_data = crawl_by_url(url)
#         return {
#             "status": True,
#             "message": "Congratulations! Your Zoominfo url crawled successfully.",
#             "result": zoominfo_data
#         }
#
#
# @api.route('/crawlUrls')
# class ZoominfoCrawlUrlController(Resource):
#     @api.doc(params={'urls': {'description': 'zoominfo urls', 'in': 'body', 'type': 'json', 'example': {"urls": ["zoominfo_url1", "zoominfo_url1"]}}})
#     def post(self):
#         data = request.get_json()
#         linkedin_data_list = []
#         for url in data['urls']:
#             uls(url)
#             res = uls(url)
#             if res is True:
#                 pass
#             else:
#                 return {
#                     "status": False,
#                     "message": "Sorry! Invalid Command please enter company zoominfo url.",
#                 }
#             linkedin_data_list.append(crawl_by_url(url))
#
#         return {
#             "status": True,
#             "message": "Congratulations! Your list of zoominfo urls crawled successfully.",
#             "result": linkedin_data_list
#         }
# #
# #
# # @api.route('/crawlFile')
# # @api.expect(upload_parser)
# # class ZoominfoCrawlUrlController(Resource):
# #     # @api.doc(params={'file': {'description': 'linkedin urls in file', 'in': 'files', 'type': 'file'}})
# #     def post(self):
# #         if 'file' not in request.files:
# #             return {
# #                 "status": False,
# #                 "message": "Sorry! file not passed.",
# #             }
# #         file = request.files['file']
# #
# #         # If the user does not select a file, the browser submits an
# #         if file.filename == '':
# #             return {
# #                 "status": False,
# #                 "message": "Sorry! file not passed.",
# #             }
# #         file_path = ConstantService.data_in_path() + '/' + file.filename
# #         file.save(file_path)
# #         output_file_name = crawl_by_file(file_path)
# #
# #         return {
# #             "status": True,
# #             "message": "Congratulations! Your list of linkedin urls crawled successfully.",
# #             "download_link": "http://" + ConstantService.server_host() + "/linkedin/download?output_file_name=" + output_file_name
# #         }
# #
#
# #
# # @api.route('/download')
# # class ZoominfoCrawlUrlController(Resource):
# #     @api.doc(params={'output_file_name': {'description': 'linkedin crawled data output file name', 'in': 'query', 'type': 'str'}})
# #     def get(self):
# #         output_file_name = request.args.get('output_file_name')
# #         out_file_path = os.path.join(ConstantService.fetched_scraped_data(), output_file_name)
# #         if os.path.exists(out_file_path):
# #             return send_file(out_file_path, as_attachment=True)
# #
# #         abort(404, description="Crawled data not found")
#
# def rl(url):
#     a = "https://www.zoominfo.com/"
#     if a in url:
#         return True
#     else:
#          return False
#
# def uls(url):
#    a= "https://www.zoominfo.com/"
#    if a in url:
#        return True
#    else:
#        return False"""
#
