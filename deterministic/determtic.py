import collections
import functools
import time


@functools.lru_cache(maxsize=200)
def count_words(sentence):
    _count = collections.Counter()
    for w in str(sentence).split():
        _count[w] += 1
    return _count


if __name__ == "__main__":

    sen = """In mathematics, computer science and physics, 
            a deterministic system is a system in which no 
            randomness is involved in the development of future states of the system"""

    times = []

    for i in range(3):
        start_time = time.perf_counter()
        count = count_words(sen)
        stop_time = time.perf_counter()
        time_taken = stop_time-start_time
        times.append(time_taken)
        print("Exec #{} time: {:.9f} performance gain {:%}".format(i, time_taken, 1-times[i]/times[0]))
