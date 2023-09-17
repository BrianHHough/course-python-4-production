import os
import sys
# print(sys.path)

CURRENT_FOLDER_NAME = os.path.dirname(os.path.abspath(__file__))
PARENT_DIRECTORY = os.path.abspath(os.path.join(CURRENT_FOLDER_NAME, os.pardir))
sys.path.append(PARENT_DIRECTORY)

from w1.data_processor import DataProcessor

import time
from typing import List, Dict
from tqdm import tqdm

import multiprocessing

import constants
from global_utils import get_file_name, make_dir, plot_sales_data
import json
import argparse
from datetime import datetime
from pprint import pprint


class DP(DataProcessor):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

    def get_file_path(self) -> str:
        return self._fp

    def get_file_name(self) -> str:
        return self._file_name

    def get_n_rows(self) -> int:
        return self._n_rows


def revenue_per_region(dp: DP) -> Dict:
    data_reader = dp.data_reader
    data_reader_gen = (row for row in data_reader)

    # skip first row as it is the column name
    _ = next(data_reader_gen)

    aggregate = dict()

    for row in tqdm(data_reader_gen):
        if row[constants.OutDataColNames.COUNTRY] not in aggregate:
            aggregate[row[constants.OutDataColNames.COUNTRY]] = 0
        aggregate[row[constants.OutDataColNames.COUNTRY]] += dp.to_float(row[constants.OutDataColNames.TOTAL_PRICE])

    return aggregate


def get_sales_information(file_path: str) -> Dict:
    # Initialize
    dp = DP(file_path=file_path)

    # print stats
    dp.describe(column_names=[constants.OutDataColNames.UNIT_PRICE, constants.OutDataColNames.TOTAL_PRICE])

    # return total revenue and revenue per region
    return {
        'total_revenue': dp.aggregate(column_name=constants.OutDataColNames.TOTAL_PRICE),
        'revenue_per_region': revenue_per_region(dp),
        'file_name': get_file_name(file_path)
    }


# batches the files based on the number of processes - split file paths into even number of batches
# make each process have same number of files to process
# if there are more processes than the number of files, then don't create any batches... no processes will be spawned for processing
def batch_files(file_paths: List[str], n_processes: int) -> List[List[int]]:
    # If number of processes is greater than the number of files, return empty list
    if n_processes > len(file_paths):
        return []

    # Calculate how many files will be in each batch initially
    n_per_batch = len(file_paths) // n_processes

    # Calculate the leftover files after initial batches are created
    leftovers = len(file_paths) % n_processes 

    # Create batches using lists to preserve order
    batches = []

    current_file_index = 0
    for i in range(n_processes):
        current_batch = []
        
        # Add the initial files to the batch
        for _ in range(n_per_batch):
            current_batch.append(file_paths[current_file_index])
            current_file_index += 1

        batches.append(current_batch)

    # Add leftover files to the batches sequentially
    for i in range(leftovers):
        batches[i].append(file_paths[current_file_index])
        current_file_index += 1

    return batches


# file_paths = 10
# n_processes = 3
# [{3}, {3], {3}}] [1] - with one file left over
# [{3+1}, {3], {3}}] - what we would do


# Fetch the revenue data from a file
def run(file_names: List[str], n_process: int) -> List[Dict]:
    st = time.time()

    print("Process : {}".format(n_process))
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    file_paths = [os.path.join(folder_path, file_name) for file_name in file_names]
    revenue_data = [get_sales_information(file_path) for file_path in file_paths]

    en = time.time()

    print(f"Batch for process-{n_process} time taken {en - st}")
    return revenue_data


def flatten(lst: List[List]) -> List:
    return [item for sublist in lst for item in sublist]


def main() -> List[Dict]:
    """
    Use the `batch_files` method to create batches of files that needs to be run in each process
    Use the `run` method to fetch revenue data for a given batch of files

    Use multiprocessing module to process batches of data in parallel
    Check `multiprocessing.Pool` and `pool.starmap` methods to help you wit the task

    At the end check the overall time taken in this code vs the time taken in W1 code


    :return: Revenue data in the below format

    [{
        'total_revenue': float,
        'revenue_per_region': {
                                'China': float,
                                'France': float,
                                'Germany': float,
                                'India': float,
                                'Italy': float,
                                'Japan': float,
                                'Russia': float,
                                'United Kingdom': float,
                                'United States': float},
        'file_name': str
    },{
        'total_revenue': float,
        'revenue_per_region': {
                                'China': float,
                                'France': float,
                                'Germany': float,
                                'India': float,
                                'Italy': float,
                                'Japan': float,
                                'Russia': float,
                                'United Kingdom': float,
                                'United States': float},
        'file_name': str
    },
    ....
    ....
    ....
    ]
    """

    st = time.time()
    n_processes = 3 # you may modify this number - check out multiprocessing.cpu_count() as well

    parser = argparse.ArgumentParser(description="Choose from one of these : [tst|sml|bg]")
    parser.add_argument('--type',
                        default='tst',
                        choices=['tst', 'sml', 'bg'],
                        help='Type of data to generate')
    args = parser.parse_args()

    data_folder_path = os.path.join(CURRENT_FOLDER_NAME, '..', constants.DATA_FOLDER_NAME, args.type)
    files = [str(file) for file in os.listdir(data_folder_path) if str(file).endswith('csv')]

    output_save_folder = os.path.join(CURRENT_FOLDER_NAME, '..', 'output', args.type,
                                      datetime.now().strftime("%B %d %Y %H-%M-%S"))
    make_dir(output_save_folder)
    file_paths = [os.path.join(data_folder_path, file_name) for file_name in files]

    batches = batch_files(file_paths=file_paths, n_processes=n_processes)

    ######################################## YOUR CODE HERE ##################################################
    with multiprocessing.Pool(processes=n_processes) as pool:
        params = [(file_paths, n_process) for n_process, file_paths in enumerate(batches)]
        revenue_data = pool.starmap(run, params)
        revenue_data = flatten(revenue_data)

        pool.close()
        # wait until all processes done, produce some result, and then after that, go to next
        pool.join()
        
    ######################################## YOUR CODE HERE ##################################################

    en = time.time()
    print("Overall time taken : {}".format(en-st))

    ######################################## YOUR CODE HERE ##################################################
    for yearly_data in revenue_data:
        # 1 - save data as JSON
        # 2 - save plot as png

        # 1 - save data as JSON
        with open(os.path.join(output_save_folder, f'{yearly_data["file_name"]}.json'), 'w') as f:
            # dump dictionary into json string and write it to the file
            f.write(json.dumps(yearly_data))

        # 2 - save plot as png
        plot_sales_data(
            yearly_revenue=yearly_data['revenue_per_region'], 
            year=yearly_data["file_name"],
            plot_save_path=os.path.join(output_save_folder, f'{yearly_data["file_name"]}.png'))

        

    ######################################## YOUR CODE HERE ##################################################
        
    # should return revenue data
    return revenue_data #### [YOUR CODE HERE] ####


if __name__ == '__main__':
    # res = main()
    # pprint(res)
    file_paths = list(range(9))
    n_processes = 3

    batches = batch_files(file_paths, n_processes)

    print(batches)