# Intermediate Python - Week 2

## Overview:
I learned how to use Python's `multi-processing` module to optimize code execution, for situations like analyzing, generating, or processing large datasets or complex calculations.

`Multiprocessing` means run multiple tasks/processes in parallel; leads to speed/performance enhancements. Creates a new process to execute code to run it separately from the main process of the code. This approach utilizes available computing power, so the code can run faster and more efficiently.

Python's Global Interpreter Lock (GIL) means we can only execute one thread to run Python bytecode at a time... so with many cores available, only one thread can utilize them at a time. Multiprocessing overcomes GIL by creating many processes and distributes the workload across them during execution.

# Part 1: `batch_files()` method:
- we have multiple files to process, so we will batch them into even chunks so same amount of data is processed each time for optimized utilization.
- we need to break down the list of files (file_paths) into smaller batches for parallel processing

### Running the file with PYTHONPATH
PYTHONPATH required - file path isn't pythonic... subdirectories are separate containing code that isn't interfering with each other, but in some cases, we want to import some code from week 1... some cases where we want to import outside of sub-directory.

### Run a virtual env:

Create virtual environment: `virtualenv env`

Initialize environment: `source env/bin/activate`

### 🐞: Unable to find `utils` from `w1` directory - path import error

I tried to run after `cd`-ing into `w2` and running `python main.py`, I got this error:
```bash
Traceback (most recent call last):
  File "/Users/.../.../.../.../.../course-python-4-production/w2/main.py", line 14, in <module>
    from w1.data_processor import DataProcessor
  File "/Users/.../.../.../.../.../course-python-4-production/w1/data_processor.py", line 3, in <module>
    from utils import Stats, DataReader
ModuleNotFoundError: No module named 'utils'
```

The `utils.py` is inside the `w1` directory, so it should be accessible to `data_processor.py` as they are both in the same `w1` directory, and utils is a relative import compared to data_processor.

But when we are running `w2/main.py`, this file needs import a file that makes a relative import. Python doesn't automatically know this

So I had to edit `w1/data_processor.py` and update this line:
```py
from w1.utils import Stats, DataReader
```
to be a relative import:
```py
from .utils import Stats, DataReader
```

This ensures that we treat `w1/utils.py` from within `w1/data_processor.py` as a relative import when we run `w2/main.py`.

✅ Now when we run `python main.py` in the w2 directory, we get this as an output:
```bash
[{0, 1, 2, 9}, {10, 3, 4, 5}, {8, 6, 7}]
```

### 🐞: The output of the groups from the multiprocessing with `batch_files()` - why we are using `sets` and not `lists` and what that means for order of the items.

In my initial implementation of `batch_files()`, it split files into batches and then deals with leftovers in the second pass.

In the original version, I had this: 
```py
def batch_files(file_paths: List[str], n_processes: int) -> List[set]:
    if n_processes > len(file_paths):
        return []

    n_per_batch = len(file_paths) // n_processes 

    first_set_len = n_processes * n_per_batch
    first_set = file_paths[0:first_set_len]
    second_set = file_paths[first_set_len:]

    batches = [set(file_paths[i:i + n_per_batch]) for i in range(0, len(first_set), n_per_batch)]
    for ind, each_file in enumerate(second_set):
        batches[ind].add(each_file)

    return batches
```

Going through the code, it would return the following:
```bash
[{0, 1, 2, 9}, {10, 3, 4, 5}, {8, 6, 7}]
```

I wasn't exactly understanding why the numbers get added to the groups in the way that’s shown in my terminal like this above. 

Let’s say we have 11 `file_paths` and 3 `n_processes`. I thought it should go…

**First Pass:**
0,1,2 (3)
3,4,5 (6)
6,7,8 (9)

**Second Pass:**
0,1,2,9 (10)
3,4,5,10 (11)
6,7,8

Instead, I saw 9 after 2 (group 1), but then the opposite with: 10 before 3 (group 2), and 8 before 6 (group 3).

The issue is with the for loop, where when I split the file paths into 2 sets (`first_set` and `second_set`), the first set contains the majority of the file paths, and the second set contains the "leftovers".

In the example above, `first_set` = 9 filepaths (0 - 8, inclusive); `second_set` = 2 file paths (9-10, inclusive)

The ISSUE there is that when adding the leftover paths from the `second_set` to the `batches`, it adds the 1st file from the `second_set` to the first group of `batches` and so on, which leads to the mismatch.

In this way, the `9` of `second_set` gets added to the first set in `batches`, while the `10` in the set gets added to the second set in `batches`.

We need to fix the segment that adds leftovers to the batches by changing the overall function to this:

```py
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
```

✅ When this runs where `file_paths = 9` and `n_processes = 3`, this will output: `[[0, 1, 2], [3, 4, 5], [6, 7, 8]]` exactly like what we expect!

BUT... now it's a different data structure. This is a `LIST`, not a `SET`!

Here are some notes on Sets vs. Lists
- **Lists:** line of objects stringed together, and you know what order they're all in.
    - Example: `[1, 2, 3]`
- **Sets:** group of objects in a plane, with random organization, and order is not important or logged.
    - Example: `{1, 2, 3}` might sometimes look like `{2, 1, 3}` or `{3, 1, 2}`

In our code example, we were breaking the items into small batches and they were wandering about in the sets (converted lists to sets), with no attention to order. Items can be ordered before putting them into a set, but once they're in the set, the order isn't guaranteed. Sets don't remember the order like a list does.



# Part II: `run()` method
## Run the process:

When I run the following:
```py
if __name__ == '__main__':
    res = main()
```

This is the output:
```bash
Process : 0
Process : 1
Process : 2
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.211510830769738,
 'median': None,
 'min': 0.001,
 'std': 314.13738240948175}
'TotalPrice'
{'25': 2.55,
 '50': 6.58,
 '75': 14.96,
 'max': 142691.68,
 'mean': 33.573793953841665,
 'median': None,
 'min': 0.001,
 'std': 1193.563308179154}
'UnitPrice'
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.251292749998372,
 'median': None,
 'min': 0.001,
 'std': 304.7065793845803}
'TotalPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 11.291125247057265,
 'median': None,
 'min': 0.001,
 'std': 326.33789059131743}
'TotalPrice'
{'25': 2.55,
 '50': 6.6,
 '75': 14.95,
 'max': 160528.13999999998,
 'mean': 33.799728674996885,
 'median': None,
 'min': 0.001,
 'std': 1190.5829118072277}
{'25': 2.55,
 '50': 6.6,
 '75': 15.0,
 'max': 178364.59999999998,
 'mean': 40.535017341173344,
 'median': None,
 'min': 0.001,
 'std': 1450.293352932578}
65000it [00:00, 852255.64it/s]
80000it [00:00, 835036.33it/s]
85000it [00:00, 844778.22it/s]
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.996214966667246,
 'median': None,
 'min': 0.001,
 'std': 327.7099314175273}
'TotalPrice'
{'25': 2.55,
 '50': 6.6,
 '75': 14.92,
 'max': 142691.68,
 'mean': 37.75857793332999,
 'median': None,
 'min': 0.001,
 'std': 1300.1082879602784}
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 11.330868586665728,
 'median': None,
 'min': 0.001,
 'std': 334.1514598566704}
'TotalPrice'
0it [00:00, ?it/s]{'25': 2.55,
 '50': 6.6,
 '75': 14.92,
 'max': 160528.13999999998,
 'mean': 38.06841777332996,
 'median': None,
 'min': 0.001,
 'std': 1373.0997878996477}
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.192059144442679,
 'median': None,
 'min': 0.001,
 'std': 305.12369162688367}
'TotalPrice'
{'25': 2.55,
 '50': 6.58,
 '75': 14.940000000000001,
 'max': 142691.68,
 'mean': 34.022147577775236,
 'median': None,
 'min': 0.001,
 'std': 1215.827969633452}
60000it [00:00, 866636.50it/s]
Batch for process-2 time taken 0.6118268966674805
75000it [00:00, 878035.22it/s]
Batch for process-1 time taken 0.7311551570892334
90000it [00:00, 886663.80it/s]
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 8.994602442857856,
 'median': None,
 'min': 0.001,
 'std': 271.6167592177564}
'TotalPrice'
{'25': 2.55,
 '50': 6.58,
 '75': 14.940000000000001,
 'max': 142691.68,
 'mean': 29.73535868571067,
 'median': None,
 'min': 0.001,
 'std': 1031.4268413150558}
70000it [00:00, 907675.58it/s]
Batch for process-0 time taken 1.1232740879058838
Overall time taken : 1.6723368167877197
```

There are 3 processes, and this is on test dataset, so we see how multiprocessing is helping to run these 3 separate `run()` methods in parallel efficiently and quickly using Python.



# Part III: Compare runtime

How to check the `cpu_count` for the machine you are running:

Initalize python:
```bash
python
```

Import multiprocessing:
```bash
import multiprocessing
```

Run the command the get the cpu_count:
```bash
multiprocessing.cpu_count()
```

For my system, it logged `10`


### Running the `tst` dataset with: `python main.py --type tst`

```bash
Process : 0
Process : 1
Process : 2
...
85000it [00:00, 882685.62it/s]
Batch for process-0 time taken 1.1351821422576904
Overall time taken : 1.627197027206421
```

### Run on the `small` dataset with: `python main.py --type sml`
```bash
Process : 0
Process : 1
Process : 2
...
850000it [00:00, 941513.96it/s]
Batch for process-0 time taken 11.141692876815796
Overall time taken : 11.635273933410645
```

### Run on the `big` dataset with: `python main.py --type bg`
```bash
Process : 0
Process : 1
Process : 2
...
5000000it [00:05, 939102.77it/s]
Batch for process-0 time taken 79.8315258026123
Overall time taken : 80.32834506034851
```

# 🧪 Run tests with prints 

```bash
PYTHONPATH=../ pytest test.py -s
```

✅ This worked and log is here:
```bash
================================================== test session starts ==================================================
platform darwin -- Python 3.11.3, pytest-7.2.2, pluggy-1.3.0
rootdir: /Users/.../.../.../.../.../course-python-4-production/w2
plugins: anyio-4.0.0
collected 2 items                                                                                                       

test.py {'Country': 'France',
 'Date': '2015/04/06',
 'Description': 'HEART BUTTONS JEWELLERY BOX',
 'InvoiceNo': 'f1bce1a2-5032-11ee-826f-2e9565c92f30',
 'Quantity': '1',
 'StockCode': '82095',
 'TotalPrice': '4.96',
 'UnitPrice': '4.96'}
85000it [00:00, 864333.21it/s]
90000it [00:00, 872726.47it/s]
80000it [00:00, 891840.59it/s]
75000it [00:00, 890969.44it/s]
60000it [00:00, 900264.87it/s]
65000it [00:00, 892381.74it/s]
70000it [00:00, 886758.42it/s]
[{'file_path': '/Users/.../.../.../.../.../course-python-4-production/w2/../data/tst/2020.csv',
  'revenue_data': {'file_name': '2020',
                   'revenue_per_region': {'Canada': 256482.2130000059,
                                          'China': 74452.31599999977,
                                          'France': 514502.14100000897,
                                          'Germany': 237569.27600000473,
                                          'India': 285563.4710000039,
                                          'Italy': 119300.51499999993,
                                          'Japan': 143328.8380000012,
                                          'Russia': 151627.47000000102,
                                          'United Kingdom': 857583.2950000089,
                                          'United States': 805066.9390000126},
                   'total_revenue': 3445476.4739997345}},
 {'file_path': '/Users/.../.../.../.../.../course-python-4-production/w2/../data/tst/2021.csv',
  'revenue_data': {'file_name': '2021',
                   'revenue_per_region': {'Canada': 224466.37800000276,
                                          'China': 178841.42299999972,
                                          'France': 573300.703000005,
                                          'Germany': 310207.3060000097,
                                          'India': 372652.3250000077,
                                          'Italy': 118157.19199999984,
                                          'Japan': 160583.25300000157,
                                          'Russia': 133398.88599999968,
                                          'United Kingdom': 452913.5850000163,
                                          'United States': 537472.2310000153},
                   'total_revenue': 3061993.281999771}},
 {'file_path': '/Users/.../.../.../.../.../course-python-4-production/w2/../data/tst/2019.csv',
  'revenue_data': {'file_name': '2019',
                   'revenue_per_region': {'Canada': 175110.00200000269,
                                          'China': 55695.04999999969,
                                          'France': 163828.34700000272,
                                          'Germany': 344793.15700000414,
                                          'India': 219366.78700000426,
                                          'Italy': 100696.18999999945,
                                          'Japan': 104515.45399999959,
                                          'Russia': 128354.35799999995,
                                          'United Kingdom': 713101.2420000108,
                                          'United States': 698517.7070000046},
                   'total_revenue': 2703978.2939997506}},
 {'file_path': '/Users/.../.../.../.../.../course-python-4-production/w2/../data/tst/2018.csv',
  'revenue_data': {'file_name': '2018',
                   'revenue_per_region': {'Canada': 287601.0460000032,
                                          'China': 58386.56099999999,
                                          'France': 188809.5070000001,
                                          'Germany': 253318.01300000332,
                                          'India': 287511.7260000068,
                                          'Italy': 392247.32000000175,
                                          'Japan': 417741.0010000028,
                                          'Russia': 87113.61999999965,
                                          'United Kingdom': 441788.1390000169,
                                          'United States': 440614.4000000158},
                   'total_revenue': 2855131.3329997472}},
 {'file_path': '/Users/.../.../.../.../.../course-python-4-production/w2/../data/tst/2015.csv',
  'revenue_data': {'file_name': '2015',
                   'revenue_per_region': {'Canada': 247533.6530000024,
                                          'China': 51774.16399999985,
                                          'France': 119369.79100000022,
                                          'Germany': 204774.97300000163,
                                          'India': 201626.9990000025,
                                          'Italy': 67568.26399999991,
                                          'Japan': 44309.01699999988,
                                          'Russia': 60171.94899999968,
                                          'United Kingdom': 685182.7670000093,
                                          'United States': 583203.0990000105},
                   'total_revenue': 2265514.6759997993}},
 {'file_path': '/Users/.../.../.../.../.../course-python-4-production/w2/../data/tst/2016.csv',
  'revenue_data': {'file_name': '2016',
                   'revenue_per_region': {'Canada': 207364.0540000017,
                                          'China': 169964.3000000024,
                                          'France': 174285.64300000158,
                                          'Germany': 228622.34300000183,
                                          'India': 97026.50399999924,
                                          'Italy': 138269.71300000025,
                                          'Japan': 71622.25999999979,
                                          'Russia': 45781.22699999985,
                                          'United Kingdom': 630323.3500000136,
                                          'United States': 419037.2130000155},
                   'total_revenue': 2182296.6069997083}},
 {'file_path': '/Users/.../.../.../.../.../course-python-4-production/w2/../data/tst/2017.csv',
  'revenue_data': {'file_name': '2017',
                   'revenue_per_region': {'Canada': 130638.25999999946,
                                          'China': 265652.0400000029,
                                          'France': 237453.06700000254,
                                          'Germany': 184073.31300000224,
                                          'India': 112640.22499999957,
                                          'Italy': 57025.70499999982,
                                          'Japan': 195540.3990000015,
                                          'Russia': 109440.61199999988,
                                          'United Kingdom': 332955.9580000077,
                                          'United States': 456055.5290000164},
                   'total_revenue': 2081475.1079997467}}]
.

=================================================== 2 passed in 2.60s ===================================================
```


# Run tests without prints 
```
PYTHONPATH=../ pytest test.py
```

✅ This worked and logged the output:
```bash
================================================== test session starts ==================================================
platform darwin -- Python 3.11.3, pytest-7.2.2, pluggy-1.3.0
rootdir: /Users/.../.../.../.../.../course-python-4-production/w2
plugins: anyio-4.0.0
collected 2 items                                                                                                       

test.py ..                                                                                                        [100%]

=================================================== 2 passed in 2.59s ===================================================
```
