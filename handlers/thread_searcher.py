from collections import defaultdict
from threading import Thread, Lock, current_thread
from utils import constants
import logging
import timeit


def search_words_in_file(filepath, keywords):
    result = defaultdict(list)
    try:
        with open(filepath) as f:
            content = f.read()
        for word in keywords:
            if word in content:
                result[word].append(str(filepath))

    except IOError as e:
        logging.error(e)

    return result


def worker(files, keywords, results, lock):
    print(constants.thread_started.format(current_thread().name))
    for file in files:
        result = search_words_in_file(file, keywords)
        for key, value in result.items():
            with lock:
                results[key].extend(value)

    print(constants.thread_finished.format(current_thread().name))


def parallel_file_search(files, keywords, num_threads):
    print(constants.search_threads)
    threads = []
    results = defaultdict(list)
    lock = Lock()

    # Distribute files among threads
    files_per_thread = len(files) // num_threads
    reminder = len(files) % num_threads
    start_index = 0

    for i in range(num_threads):
        end_index = start_index + files_per_thread + (1 if i < reminder else 0)
        process_files = {
            file_name: content
            for file_name, content in list(files.items())[start_index:end_index]
        }
        t = Thread(
            target=worker,
            name=constants.thread_name.format(i),
            args=(process_files, keywords, results, lock),
        )
        threads.append(t)
        t.start()
        start_index = end_index

    for thread in threads:
        thread.join()

    print(constants.search_threads_finished)
    return results


def get_thread_results(files, keywords, num_threads):
    start_time = timeit.default_timer()
    thread_results = parallel_file_search(files, keywords, num_threads)
    duration = timeit.default_timer() - start_time

    print(constants.thread_info.format(duration))
    for key, value in thread_results.items():
        print(f"{key}: {value}\n")
