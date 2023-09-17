from typing import List
from pprint import pprint
from .utils import Stats, DataReader
# from w1.utils import Stats, DataReader
from tqdm import tqdm
import os


class DataProcessor:
    def __init__(self, file_path: str) -> None:
        self._fp = file_path
        self._col_names = []
        self._sep = ","
        self._stats = None
        self._file_name = os.path.basename(file_path)
        self._n_rows = 0

        self._set_col_names()
        self.data_reader = DataReader(fp=file_path, sep=self._sep, col_names=self._col_names)
        self._set_n_rows()

    @staticmethod
    def to_float(val):
        try:
            return float(val)
        except:
            return None

    def _set_n_rows(self) -> None:
        # get generator from data_reader
        data_reader_gen = (row for row in self.data_reader)

        _ = next(data_reader_gen)

        # The below line will show the outputs of tqdm
        # for _ in tqdm(data_reader_gen):
        for _ in data_reader_gen:
            self._n_rows += 1

    def _set_col_names(self) -> None:
        with open(self._fp) as f:
            first_row = f.readline().strip('\n')

        col_names = first_row.split(self._sep)
        self._col_names = col_names

    def describe(self, column_names: List[str]):
        # get generator from data_reader
        data_reader_gen = (row for row in self.data_reader)

        # skip first row as it is the column name
        _ = next(data_reader_gen)

        # key is the column name and value is the stats object
        stats = {name: Stats() for name in column_names}

        # update stats as we iterate through the file
        # The below line will show the outputs of tqdm
        # for row in tqdm(data_reader_gen):
        for row in data_reader_gen:
            for column_name in column_names:
                stats[column_name].update_stats(val=row[column_name])

        self._stats = stats
        for column_name, value in self._stats.items():
            pprint(column_name)
            pprint(value.get_stats())

    def aggregate(self, column_name: str) -> float:
        """
        Input : List[str]
        Output : Dict

        This method should use the generator method assigned to self.data_reader and return aggregate
        of the column mentioned in the `column_name` variable

        For example if the `column_name` -> 'TotalPrice' and the file format is as below:

        StockCode    , Description    , UnitPrice  , Quantity, TotalPrice , Country
        22180        , RETROSPOT LAMP , 19.96      , 4       , 79.84      , Russia
        23017        , APOTHECARY JAR , 24.96      , 1       , 24.96      , Germany
        84732D       , IVORY CLOCK    , 0.39       , 2       , 0.78       ,India

        aggregate should be 105.58
        """
        ######################################## YOUR CODE HERE ##################################################

        # get generator from (out of) data_reader
        # make it as a generator with generator comprehension with row for row in
        # for loop over the generator and update the aggregate variable
        data_reader_gen = (row for row in self.data_reader)

        # skip first row as it is the column name header
        # we call next and this is how we skip the first column for each row
        _ = next(data_reader_gen)

        # initialize the aggregate variable, which is zero
        # when we start, we have no numbers yet
        aggregate = 0

        # iterate over the data reader generator with a for loop
        # The below line will show the outputs of tqdm
        # for row in tqdm(data_reader_gen):
        for row in data_reader_gen:
            if self.to_float(row[column_name]): 
                # accumulate the number of values of the column name
                # for each row, aggregate the row with name, when it's a string, we want to enclose it as float
                # row[column_name]
                aggregate += self.to_float(row[column_name])
        
        return aggregate

        ######################################## YOUR CODE HERE ##################################################

# Run script as a standalone module
if __name__ == "__main__":
    # Define the path to the sample data, the separator, and the columns
    filepath = "../data/tst/2021.csv"
    separator = ","
    columns = ['StockCode', 'Description', 'UnitPrice', 'Quantity', 'TotalPrice', 'Country']

    # Create an instance of the DataReader
    processor = DataProcessor(filepath)

    # Use the `describe` method to print the stats of the columns
    # print("\nStatistics for the specified columns:")
    # processor.describe(['TotalPrice', 'UnitPrice'])

    # Use the `aggregate` method to print the aggregate for the specified column: TotalPrice
    total_price_aggregate = round(processor.aggregate('TotalPrice'), 2)
    print(f"\nAggregate for TotalPrice: {total_price_aggregate}")

    # Loop through the generator and print each row
    # for row in processor.data_reader:
    #     print(row)
