import os
from datetime import datetime
import pandas as pd
from flask_restplus import Resource
from flask import request, send_file, abort
from werkzeug.datastructures import FileStorage
from ..util.dto import PitchbookDto
from ..util.pitchbook_thread import execute
from ..service.pitchbook_service import crawl_by_url
from ..service.constant_service import ConstantService
from ..service.mailer_service import MailUtilities

api = PitchbookDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/crawlUrl')
class PitchbookCrawlUrlController(Resource):
    @api.doc(params={'url': {'description': 'pitchbook url', 'in': 'query', 'type': 'str'}})
    def get(self):
        url = request.args.get('url')
        if request.args.get('url', None) == None:
            return {
                "status": False,
                "message": "Sorry! Invalid Command  please enter company pitchbook url."
            }
        rl(url)
        res = rl(url)
        if res is True:
            pass
        else:
            return {
                "status": False,
                "message": "Sorry! Invalid Command  please enter company pitchbook url."
                ,
            }
        pitchbook_data = crawl_by_url(url)
        return {
            "status": True,
            "message": "Congratulations! Your website url crawled on Pitchbook successfully.",
            "result": pitchbook_data
        }


@api.route('/crawlUrls')
class PitchbookCrawlUrlsController(Resource):
    @api.doc(params={'urls': {'description': 'pitchbook urls', 'in': 'body', 'type': 'json',
                              'example': {"urls": ["pitchbook_url1", "pitchbook_url2"]}}})
    def post(self):
        data = request.get_json()
        pitchbook_data_list = []
        for url in data['urls']:
            uls(url)
            res = uls(url)
            if res is True:
                pass
            else:
                return {
                    "status": False,
                    "message": "Sorry! Invalid Command please enter company Pitchbook url.",
                }
            pitchbook_data_list.append(crawl_by_url(url))

        return {
            "status": True,
            "message": "Congratulations! Your website urls crawled on pitchbook successfully.",
            "result": pitchbook_data_list
        }


@api.route('/crawlFile')
@api.expect(upload_parser)
class PitchbookCrawlFileController(Resource):
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
        pichbook_validation(file_path)
        res = pichbook_validation(file_path)
        if res is True:
            pass
        else:
            os.remove(file_path)
            return {
                "status": False,
                "message": "Column Name Should be - Urls, urls anyone at once! file not passed.",
            }
        try:
            now = datetime.now()
            dt_start = now.strftime("%d/%m/%Y %H:%M:%S")
        # output_file_name = crawl_by_file(file_path)
            out_path = ConstantService.fetched_scraped_data()
            output_file_name = execute(file_path, out_path)
            download_link = "http://" + ConstantService.server_host() + "/pitchbook/download?output_file_name=" + output_file_name
            if email_id is not None:
                MailUtilities.send_success_notification(email_id, download_link, dt_start)

            return {
                    "status": True,
                    "message": "Congratulations! Your list of urls crawled successfully from pitchbook.",
                    "download_link": "http://" + ConstantService.server_host() + "/pitchbook/download?output_file_name=" + output_file_name
                    }
        except Exception as e:
            print(str(e))
            if email_id is not None:
                MailUtilities.send_failed_notification(email_id, str(e), dt_start)


@api.route('/download')
class PitchbookDownloadController(Resource):
    @api.doc(params={
        'output_file_name': {'description': 'pitchbook crawled data output file name', 'in': 'query', 'type': 'str'}})
    def get(self):
        if request.args.get('output_file_name', None) is None:
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


def pichbook_validation(file_path):
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
    a = "pitchbook.com/"
    if a in url:
        return True
    else:
        return False


def uls(url):
    a = "pitchbook.com/"
    if a in url:
        return True
    else:
        return False


def down(output_file_name):
    a = '.xlsx'
    b = '.zip'
    if a or b in output_file_name:
        return True
    else:
        return False
