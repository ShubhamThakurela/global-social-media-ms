import os
import pandas as pd
from datetime import datetime
from flask import request, send_file, abort
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage
from ..util.dto import LnkedininDto
from ..service.linkedin_service import crawl_by_url
from ..service.constant_service import ConstantService
from ..service.mailer_service import MailUtilities
from ..util.linkedin_thread import execute


api = LnkedininDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/crawlUrl')
class LinkedinCrawlUrlController(Resource):
    @api.doc(params={'url': {'description': 'linkedin url', 'in': 'query', 'type': 'str'}})
    def get(self):
        url = request.args.get('url')
        if request.args.get('url', None) is None:
            return {
                "status": False,
                "message": "Sorry! Invalid Command please enter company linkedin url."
            }
        rl(url)
        res = rl(url)
        if res is True:
            pass
        else:
            return {
                "status": False,
                "message": "Sorry! Invalid Command please enter company linkedin url.",
            }
        linkedin_data = crawl_by_url(url)
        return {
            "status": True,
            "message": "Congratulations! Your linkedin url crawled successfully.",
            "result": linkedin_data
        }


@api.route('/crawlUrls')
class LinkedinCrawlUrlsController(Resource):
    @api.doc(params={'urls': {'description': 'linkedin urls', 'in': 'body', 'type': 'json',
                              'example': {"urls": ["linkedin_url1", "linkedin_url2"]}}})
    def post(self):
        data = request.get_json()
        linkedin_data_list = []
        for url in data['urls']:
            uls(url)
            res = uls(url)
            if res is True:
                pass
            else:
                return {
                    "status": False,
                    "message": "Sorry! Invalid Command please enter company linkedin url.",
                }
            linkedin_data_list.append(crawl_by_url(url))
        return {
            "status": True,
            "message": "Congratulations! Your list of linkedin urls crawled successfully.",
            "result": linkedin_data_list
        }


@api.route('/crawlFile')
@api.expect(upload_parser)
class LinkedinCrawlFileController(Resource):
    @api.doc(params={'email_id': {'description': 'Specify Email_id', 'in': 'query', 'type': 'string'}})
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
        email_id = None
        if 'email_id' in request.args:
            email_id = request.args.get('email_id')    
            
        file_path = ConstantService.data_in_path() + '/' + file.filename
        file.save(file_path)
        likedin_validation(file_path)
        res = likedin_validation(file_path)
        if res is True:
            pass
        else:
            os.remove(file_path)
            return {
                "status": False,
                "message": "Column Name Should be -  Urls, urls anyone at once! file not passed.",
            }
        try:
            now = datetime.now()
            dt_start = now.strftime("%d/%m/%Y %H:%M:%S")

            out_path = ConstantService.fetched_scraped_data()
            output_file_name = execute(file_path, out_path)
            download_link = "http://" + ConstantService.server_host() + "/linkedin/download?output_file_name=" + output_file_name
            if email_id is not None:
                MailUtilities.send_success_notification(email_id, download_link, dt_start)
        
            return {
                "status": True,
                "message": "Congratulations! Your list of linkedin urls crawled successfully.",
                "download_link": "http://" + ConstantService.server_host() + "/linkedin/download?output_file_name=" + output_file_name
            }
        except Exception as e:
            print(str(e))
            if email_id is not None:
                MailUtilities.send_failed_notification(email_id, str(e), dt_start)    


@api.route('/download')
class LinkedinDownloadController(Resource):
    @api.doc(params={
        'output_file_name': {'description': 'linkedin crawled data output file name', 'in': 'query', 'type': 'str'}})
    def get(self):
        if request.args.get('output_file_name', None) == None:
            return {
                "status": False,
                "message": "Sorry! Please enter linkedin crawled data output file name."
            }
        output_file_name = request.args.get('output_file_name')
        down(output_file_name)
        res = down(output_file_name)
        if res is True:
            pass
        else:
            return {
                "status": False,
                "message": "Sorry! Please enter linkedin crawled data output file name.",
            }
        output_file_name = request.args.get('output_file_name')
        out_file_path = os.path.join(ConstantService.data_processed_path(), output_file_name)
        if os.path.exists(out_file_path):
            return send_file(out_file_path, as_attachment=True)

        abort(404, description="Crawled data not found")


def likedin_validation(file_path):
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
    a = "www.linkedin.com/"
    b = "www.de.linkedin.com/"
    if a or b in url:
        return True
    else:
        return False


def uls(url):
    a = "www.linkedin.com/"
    if a in url:
        return True
    else:
        return False


def down(output_file_name):
    a = ".zip"
    b = ".csv"
    if a or b in output_file_name:
        return True
    else:
        return False
