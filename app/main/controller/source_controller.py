import os
import time
from datetime import datetime
import pandas as pd
from flask import request, send_file, abort
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage
from ..util.dto import SourceDto
from ..service.mailer_service import MailUtilities
from ..service.source_service import fetch_by_files
from ..service.source_service import fetch_by_file
from ..service.constant_service import ConstantService

api = SourceDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/data_by_file')
@api.expect(upload_parser)
class RawFetchSourceController(Resource):
    @api.doc(params={'source': {'description': 'source (Ex - linkedin or pitchbook)', 'in': 'query', 'type': 'str'},
                     'email_id': {'description': 'Specify Email_id', 'in': 'query', 'type': 'string'}
                     })
    def post(self):
        # Start time
        start_time = time.time()
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
        validation(file_path)
        res = validation(file_path)
        if res is True:
            pass
        else:
            os.remove(file_path)
            return {
                "status": False,
                "message": "Column Name Should be - Url or url,  file not passed.",
            }
        source = request.args.get('source')
        sou(source)
        res = sou(source)
        if res is True:
            pass
        else:
            return {
                "status": False,
                "message": "Sorry! Please Insert the  Source...",
            }
        if request.args.get('source', None) is None:
            return {
                "status": False,
                "message": "Source Should be - (linkedin or pitchbook)"
            }
        try:
            now = datetime.now()
            dt_start = now.strftime("%d/%m/%Y %H:%M:%S")

            if 'linkedin' in source:
                output_file_name = fetch_by_file(file_path, source)
            else:
                output_file_name = fetch_by_files(file_path, source)
            download_link = "http://" + ConstantService.server_host() + "/sdmanager/getdata_by_File?output_file_name=" + output_file_name
            if email_id is not None:
                MailUtilities.send_success_notification(email_id, download_link, dt_start)
        # End time
            end_time = time.time()
            return {
                    "status": True,
                    'time_taken': '{:.3f} sec'.format(end_time - start_time),
                    "message": "Congratulations! Your list of downloadable Data prepared successfully.",
                    "download_link": "http://" + ConstantService.server_host() + "/sdmanager/getdata_by_File?output_file_name=" + output_file_name
                    }
        except Exception as e:
            print(str(e))
            if email_id is not None:
                MailUtilities.send_failed_notification(email_id, str(e), dt_start)


@api.route('/download_file')
class SourceDownloadController(Resource):
    @api.doc(params={
        'output_file_name': {'description': 'Scrape_Downloader crawled data output file name', 'in': 'query',
                             'type': 'str'}})
    def get(self):
        if request.args.get('output_file_name', None) is None:
            return {
                "status": False,
                "message": "Sorry! Please Enter Valid File Name."
            }
        output_file_name = request.args.get('output_file_name')
        down(output_file_name)
        res = down(output_file_name)
        if res is True:
            pass
        else:
            return {
                "status": False,
                "message": "Sorry! Please enter Scrape_Downloader data output file name.",
            }
        out_file_path = os.path.join(ConstantService.data_out_path(), output_file_name)
        print(out_file_path)
        if os.path.exists(out_file_path):
            return send_file(out_file_path, as_attachment=True)

        abort(404, description="Invalid File Name, - 404 not found")


def validation(file_path):
    name, file_type = os.path.splitext(file_path)
    file_type = file_type.lower()
    if file_type in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    elif file_type == '.csv':
        df = pd.read_csv(file_path)
    else:
        print("Unsupported file extension " + file_type + "! We are supporting only (csv, xls, xlsx).")
        return False
    url_com = ["Website", "website", "Url", "url", "Urls", "urls"]
    for i in df.columns:
        if i in url_com:
            return True
        else:
            return False


def sou(source):
    web = ["linkedin", "pitchbook"]
    if source in web:
        return True
    else:
        return False


def down(output_file_name):
    a = ".xlsx"
    if a in output_file_name:
        return True
    else:
        return False
