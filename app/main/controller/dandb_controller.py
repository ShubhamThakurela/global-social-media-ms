import pandas as pd
from flask import request, send_file, abort
from flask_restplus import Resource
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from ..service.constant_service import ConstantService
from ..util.dto import DandBDto
from ..util.dnb_thread import execute
import os
from ..service.dandb_service import crawl_by_url, crawl_by_file

api = DandBDto.api

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/crawlUrl')
class dandbCrawlUrlController(Resource):
    @api.doc(params={'url': {'description': 'DnB url', 'in': 'query', 'type': 'str'}})
    def get(self):
        url = request.args.get('url')
        if request.args.get('url', None) == None:
            return {
                "status": False,
                "message": "Sorry! Invalid Command please enter company dnb url."
            }
        rl(url)
        res = rl(url)
        if res is True:
            pass
        else:
            return {
                "status": False,
                "message": "Sorry! Invalid Command please enter company dnb url.",
            }
        d_and_b_data = crawl_by_url(url)
        return {
            "status": True,
            "message": "Congratulations! Your dnb url crawled successfully.",
            "result": d_and_b_data
        }


@api.route('/crawlUrls')
class dandbfoCrawlUrlController(Resource):
    @api.doc(params={'urls': {'description': 'DnB urls', 'in': 'body', 'type': 'json',
                              'example': {"urls": ["D&B_url1", "D&B_url2"]}}})
    def post(self):
        data = request.get_json()
        d_and_b_data_list = []
        for url in data['urls']:
            uls(url)
            res = uls(url)
            if res is True:
                pass
            else:
                return {
                    "status": False,
                    "message": "Sorry! Invalid Command please enter company dnb url."
                    ,
                }
            d_and_b_data_list.append(crawl_by_url(url))

        return {
            "status": True,
            "message": "Congratulations! Your list of DnB urls crawled successfully.",
            "result": d_and_b_data_list
        }


@api.route('/crawlFile')
@api.expect(upload_parser)
class dandbCrawlUrlController(Resource):
    # @api.doc(params={'file': {'description': 'dnd urls in file', 'in': 'files', 'type': 'file'}})
    def post(self):
        if 'file' not in request.files:
            return {
                "status": False,
                "message": "Sorry! file not passed.",
            }
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        if file.filename == '':
            return {
                "status": False,
                "message": "Sorry! file not passed.",
            }
        file_path = ConstantService.data_in_path() + '/' + file.filename
        file.save(file_path)
        dnd_validation(file_path)
        res = dnd_validation(file_path)
        if res is True:
            pass
        else:
            os.remove(file_path)
            return {
                "status": False,
                "message": "Column Name Should be -  Urls, urls anyone at once! file not passed",
            }
        out_path = ConstantService.fetched_scraped_data()
        output_file_name = execute(file_path, out_path)
        # output_file_name = crawl_by_file(file_path)

        return {
            "status": True,
            "message": "Congratulations! Your list of dnd urls crawled successfully.",
            "download_link": "http://" + ConstantService.server_host() + "/dandb/download?output_file_name=" + output_file_name
        }


@api.route('/download')
class dandbCrawlUrlController(Resource):
    @api.doc(
        params={'output_file_name': {'description': 'dnb crawled data output file name', 'in': 'query', 'type': 'str'}})
    def get(self):
        if request.args.get('output_file_name', None) == None:
            return {
                "status": False,
                "message": "Sorry! Please insert pitchbook crawled data output file name."
            }
        output_file_name = request.args.get('output_file_name')
        down(output_file_name)
        res = down(output_file_name)
        if res is True:
            pass
        else:
            return {
                "status": False,
                "message": "Sorry! Please insert pitchbook crawled data output file name.",
            }
        out_file_path = os.path.join(ConstantService.data_processed_path(), output_file_name)
        if os.path.exists(out_file_path):
            return send_file(out_file_path, as_attachment=True)

        abort(404, description="Crawled data not found")


def dnd_validation(file_path):
    name, file_type = os.path.splitext(file_path)
    file_type = file_type.lower()
    if file_type in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    elif file_type == '.csv':
        df = pd.read_csv(file_path)
    else:
        print("Unsupported file extension " + file_type + "! We are supporting only (csv, xls, xlsx).")
        return False
    url_com = ["Url", "url", "Urls", "urls"]
    for i in df.columns:
        if i in url_com:
            return True
        else:
            return False


def rl(url):
    a = 'https://www.dnb.com/'
    if a in url:
        return True
    else:
        return False


def uls(url):
    a = "https://www.dnb.com/"
    if a in url:
        return True
    else:
        return False


def down(output_file_name):
    a = ".xlsx"
    if a in output_file_name:
        return True
    else:
        return False
