# from ..service.dandb_service import crawl_by_file, get_url_to_scrap
# from ..service.dandb_service import data_to_file , zipdir
# from ..service.constant_service import ConstantService
# from threading import Barrier, Thread
# import math
# import pandas as pd
# import os
# import shutil
# import time
# df2 = pd.DataFrame()
#
#
# def run(url_list, file_path, barrier, out_path ):
#     global df2
#     data_set = crawl_by_file(url_list, file_path)
#     df = pd.DataFrame.from_dict(data_set)
#     df2 = df2.append(df, ignore_index=True)
#     # barrier.wait()
#     df2.drop_duplicates(keep=False)
#     data_to_file(df2, "dnb_scrapped_data_out", out_path)
#
#
#
# def execute(file_path, out_path):
#     try:
#         start_time = time.time()
#         thread_count = 30
#         url_list = get_url_to_scrap(file_path)
#         if len(url_list) == 0:
#             return ""
#         if len(url_list) < 100:
#             thread_count = 2
#             # chunk = math.ceil(len(url_list) / thread_count)
#             chunk = 2
#             chunk_list = [url_list[i:i + chunk] for i in range(0, len(url_list), chunk)]
#             thread_size = len(chunk_list)
#             barrier = Barrier(thread_size)
#         else:
#             chunk = math.ceil(len(url_list) / thread_count)
#             chunk_list = [url_list[i:i + chunk] for i in range(0, len(url_list), chunk)]
#             thread_size = len(chunk_list)
#             barrier = Barrier(thread_size)
#         threads = []
#         for i in range(thread_size):
#             threads.append(Thread(target=run, args=(chunk_list[i], file_path, barrier, out_path)))
#             print("Thread is starting", threads[i])
#             threads[-1].start()
#             time.sleep(2)
#
#         for thread in threads:
#             thread.join()
#
#         # Move file to processed after completed the process
#         if not os.path.exists(os.path.dirname(ConstantService.data_processed_path())):
#             os.makedirs(os.path.dirname(ConstantService.data_processed_path()))
#         shutil.move(file_path, os.path.join(ConstantService.data_processed_path(), os.path.basename(file_path)))
#         dest_path = ConstantService.data_processed_path()
#         zip_file_path = zipdir(out_path, dest_path)
#
#         global df2
#         df2 = pd.DataFrame()
#         end_time = time.time()
#         print("Processing Time: ", '{:.3f} sec'.format(end_time - start_time))
#         return zip_file_path
#     except Exception as e:
#         print(str(e))