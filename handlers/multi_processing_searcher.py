from multiprocessing import Process, Queue, current_process
from collections import defaultdict
from utils import constants
import sys
import timeit


def worker(files, keywords, queue):
    print(constants.process_started.format(current_process().name))

    try:
        for file in files:
            result = search_words_in_file(file, keywords)
            for key, value in result.items():
                queue.put((key, value))

    except Exception as e:
        print(constants.process_failed.format(current_process().name, e))
        sys.exit(1)
    finally:
        queue.put(None)
    print(constants.process_finished.format(current_process().name))


def search_words_in_file(filepath, keywords):
    result = defaultdict(list)
    try:
        with open(filepath) as f:
            content = f.read()

        for word in keywords:
            if word in content:
                result[word].append(str(filepath))

    except IOError as e:
        print(constants.cannot_open_file.format(filepath, e))

    return result


def parallel_file_search(files, keywords, num_processes):
    print(constants.search_multiprocessing)

    processes = []
    results = defaultdict(list)
    results_queue = Queue()

    files_per_process = len(files) // num_processes
    reminder = len(files) % num_processes
    start_index = 0

    for i in range(num_processes):
        end_index = start_index + files_per_process + (1 if i < reminder else 0)
        process_files = {
            file_name: content
            for file_name, content in list(files.items())[start_index:end_index]
        }
        process = Process(
            target=worker,
            name=constants.process_name.format(i),
            args=(process_files, keywords, results_queue),
        )
        print(constants.process_handles.format(i, start_index, end_index))
        processes.append(process)
        process.start()
        start_index = end_index

    # Collect results
    for _ in processes:
        while True:
            result = results_queue.get()
            if result is None:
                break
            key, value = result
            results[key].extend(value)

    for process in processes:
        process.join()

    print(constants.search_multiprocessing_finished)
    return dict(results)


def get_multiprocess_results(files, keywords, num_processes):
    start_time = timeit.default_timer()
    thread_results = parallel_file_search(files, keywords, num_processes)
    duration = timeit.default_timer() - start_time

    print(constants.multiprocessing_info.format(duration))

    for key, value in thread_results.items():
        print(f"{key}: {value}\n")
