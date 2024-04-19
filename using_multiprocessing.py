from multiprocessing import Process, Queue, cpu_count, current_process
from pathlib import Path
from collections import defaultdict
import sys
import time


def search_words_in_file(filepath, keywords):
    """Search words in file"""
    result = defaultdict(list)
    try:
        with open(filepath) as f:
            content = f.read()

        for word in keywords:
            if word in content:
                result[word].append(str(filepath))

    except IOError as e:
        print(f"Cannot open {filepath}: {e}")

    return result


def worker(files, keywords, queue):
    """Thread function"""
    print(f"Process {current_process().name} started")

    try:
        for file in files:
            result = search_words_in_file(file, keywords)
            for key, value in result.items():
                queue.put((key, value))

    except Exception as e:
        print(f"Process {current_process().name} failed with error: {e}")
        sys.exit(1)
    finally:
        queue.put(None)  # Signal that this worker has finished processing
    print(f"Process {current_process().name} finished")


if __name__ == "__main__":
    file_paths = [Path(f"data/file_{i}.txt") for i in range(1, 51)]
    keywords = ["Python", "project", "data", "analysis", "research"]

    num_processes = cpu_count()
    processes = []
    results = defaultdict(list)
    results_queue = Queue()

    # Distribute files among processes
    files_per_process = len(file_paths) // num_processes
    reminder = len(file_paths) % num_processes
    start_index = 0

    start_time = time.time()

    for i in range(num_processes):
        end_index = start_index + files_per_process + (1 if i < reminder else 0)
        files = file_paths[start_index:end_index]
        p = Process(
            target=worker, name=f"Process_{i}", args=(files, keywords, results_queue)
        )
        print(f"Process {i} handles files from {start_index} to {end_index}")
        processes.append(p)
        p.start()
        start_index = end_index

    # Collect results
    finished_processes = 0
    while finished_processes < num_processes:
        result = results_queue.get()
        if result is None:
            finished_processes += 1
        else:
            key, value = result
            results[key].extend(value)

    for p in processes:
        p.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f"\nMultiprocessing version took {duration:.2f} seconds\n")

    for key, value in results.items():
        print(f"\n{key}: {value}")
