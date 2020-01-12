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

    for i in range(3):
        start_time = time.perf_counter()
        count = count_words(sen)
        stop_time = time.perf_counter()
        print("Exec #{} time: {:.9f}".format(i, stop_time-start_time))
