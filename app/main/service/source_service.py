import os
import shutil
import time
import pandas as pd
from ..service.linkedin_service import prepare_linkedin_url, http_get_request
from ..service.linkedin_service import prepare_http_url, illegal_char_remover, get_url_to_scrap
from ..service.constant_service import ConstantService
from ..database.connection import get_data_linkedin, get_data_pitchbook


def fetch_by_file(file_path, source):
    try:
        start_time = time.time()
        retry = ConstantService.get_max_retry()
    # result = None
        data_list = []
        url_list = get_url_to_scrap(file_path)
        counter = 1
        for url in url_list:
            url = prepare_linkedin_url(url, 'GUEST')
            result = http_get_request(url)
            if result is None or result.status_code != 200:
                url = prepare_linkedin_url(url, 'SHOWCASE')
                result = http_get_request(url)
                if result is None or result.status_code != 200:
                    url = prepare_linkedin_url(url, '')
                # if result is None or result.status_code != 200:
            retry -= 1
            print(str(counter) + " - Url... " + str(url))
            data_list.append(fetch_by_url(url, source))
            counter += 1
        # Save result as excel
        base_file_name = os.path.basename(file_path).replace(' ', '')
        output_file_name = data_to_files(data_list, base_file_name.split('.')[0] + '-Out_file')

    # Move file to processed after completed the process
        if not os.path.exists(os.path.dirname(ConstantService.data_processed_path())):
            os.makedirs(os.path.dirname(ConstantService.data_processed_path()))
            shutil.move(file_path, os.path.join(ConstantService.data_processed_path(), os.path.basename(file_path)))
    # End Time
        end_time = time.time()
        print("Processing Time: ", '{:.3f} sec'.format(end_time - start_time))

    except Exception as e:
        return {"error": str(e)}
    return output_file_name


def fetch_by_url(org_url, source):
    try:
        data_dict = {
            'Id': '',
            'Company_Name': '',
            'Website': '',
            'Industries': '',
            'Headquarters': '',
            'Employee_Count': '',
            'Specialties': '',
            'About_Us': '',
            'Address': '',
            'CompanyType': '',
            'FundingRounds': '',
            'LastFundingOn': '',
            'LastFundingValue': '',
            'Investors': '',
            'Permalink': '',
            'CompanySize': '',
            'start_dt': '',
            'end_dt': '',
            'Source_url': ''
        }
        print("Processing Website... " + org_url)
        source = 'all' if source is None else str(source).lower().strip()
    # Get all sources
        if source == 'all':
            sources = list(ConstantService.all_sources().split(','))
        else:
            sources = list(source.split(','))
        for source in sources:
            source = source.lower().strip()
            print(source.capitalize() + '......')
            source_data = get_data_linkedin(org_url)
            final_data = source_data
            if final_data is not None:
                data_dict.update({
                    'Id': final_data[0],
                    'Company_Name': final_data[1],
                    'Website': final_data[2],
                    'Industries': final_data[3],
                    'Headquarters': final_data[4],
                    'Employee_Count': final_data[5],
                    'Specialties': final_data[6],
                    'About_Us': final_data[7],
                    'Address': final_data[8],
                    'CompanyType': final_data[9],
                    'FundingRounds': final_data[10],
                    'LastFundingOn': final_data[11],
                    'LastFundingValue': final_data[12],
                    'Investors': final_data[13],
                    'Permalink': final_data[14],
                    'CompanySize': final_data[15],
                    'start_dt': final_data[16],
                    'end_dt': final_data[17],
                    'Source_url': final_data[18]
                })
                print("Scraped From DB Fetching Done!-->", org_url)
            else:
                print("Given Url Not matched!-->", org_url)

    except Exception as e:
        return {"error": str(e)}

    return data_dict


def fetch_by_files(file_path, source):
    try:
        start_time = time.time()
        data_list = []
        url_list = get_url_to_scrap(file_path)
        counter = 1
        for url in url_list:
            print(str(counter) + " - Url... " + str(url))
            data_list.append(fetching_by_url(url, source))
            counter += 1
        # Save result as excel
        base_file_name = os.path.basename(file_path).replace(' ', '')
        output_file_name = data_to_files(data_list, base_file_name.split('.')[0] + '-Out_file')

    # Move file to processed after completed the process
        if not os.path.exists(os.path.dirname(ConstantService.data_processed_path())):
            os.makedirs(os.path.dirname(ConstantService.data_processed_path()))
            shutil.move(file_path, os.path.join(ConstantService.data_processed_path(), os.path.basename(file_path)))
    # End Time
        end_time = time.time()
        print("Processing Time: ", '{:.3f} sec'.format(end_time - start_time))

    except Exception as e:
        return {"error": str(e)}
    return output_file_name


def fetching_by_url(url, source):
    try:
        data_dict = {
            'Id': '',
            'Company_Name': '',
            'Website': '',
            'Founded': '',
            'Status': '',
            'Employees': '',
            'Revenue': '',
            'Net_Income': '',
            'About_Us': '',
            'Ownership_Status': '',
            'Financing_Status': '',
            'Primary_Industry': '',
            'Primary_Office': '',
            'Address': '',
            'Source_Url': '',
            'start_dt': '',
            'end_dt': '',
        }
        print("Processing Website... " + url)
        source = 'all' if source is None else str(source).lower().strip()
        # Get all sources
        if source == 'all':
            sources = list(ConstantService.all_sources().split(','))
        else:
            sources = list(source.split(','))
        for source in sources:
            source = source.lower().strip()
            print(source.capitalize() + '......')
            source_data = get_data_pitchbook(url)
        # for i in range(len(final_data)):
        #     print(i, final_data[i]) to check tuple length
            final_data = source_data
            if final_data is not None:
                data_dict.update({
                    'Id': final_data[0],
                    'Company_Name': final_data[1],
                    'Website': final_data[2],
                    'Founded': final_data[3],
                    'Status': final_data[4],
                    'Employees': final_data[5],
                    'Revenue': final_data[6],
                    'Net_Income': final_data[7],
                    'About_Us': final_data[8],
                    'Ownership_Status': final_data[9],
                    'Financing_Status': final_data[10],
                    'Primary_Industry': final_data[11],
                    'Primary_Office': final_data[12],
                    'Address': final_data[13],
                    'Source_Url': final_data[14],
                    'start_dt': final_data[15],
                    'end_dt': final_data[16]
                })
                print("Scraped From DB Fetching Done!-->", url)
            else:
                print("Given Url Not matched!-->", url)

    except Exception as e:
        return {"error": str(e)}

    return data_dict


def data_to_files(data_set, output_file_name):
    file_path = ConstantService.data_out_path() + '/'
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    writer = pd.ExcelWriter(file_path + output_file_name + '.xlsx')
    df = pd.DataFrame.from_dict(data_set)
    df = df.applymap(illegal_char_remover)
    df.to_excel(writer, sheet_name='Scrapped_data', index=False)
    writer.save()

    return output_file_name + '.xlsx'
