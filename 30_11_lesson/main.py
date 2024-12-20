import multiprocessing
import re
import time
from collections import Counter
from functools import reduce
from multiprocessing import Pool
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


# Функции для обработки текста
def clean_word(word):
    """Очистка слова от спецсимволов и приведение к нижнему регистру"""
    return re.sub(r'[^\w\s]', '', word).lower()


def word_not_in_stopwords(word):
    """Проверка, что слово не является стоп-словом и состоит из букв"""
    return word and word.isalpha() and word not in ENGLISH_STOP_WORDS


# Основные функции MapReduce
def mapper(text):
    """Mapper: токенизация, очистка, фильтрация и подсчёт слов"""
    tokens_in_text = text.split()
    tokens_in_text = map(clean_word, tokens_in_text)
    tokens_in_text = filter(word_not_in_stopwords, tokens_in_text)
    return Counter(tokens_in_text)


def reducer(cnt1, cnt2):
    """Reducer: объединение двух счётчиков"""
    cnt1.update(cnt2)
    return cnt1


def chunk_mapper(chunk):
    """Обработка одного блока данных с использованием MapReduce"""
    mapped = map(mapper, chunk)
    return reduce(reducer, mapped)


# Разбиение данных на части
def chunkify(data, number_of_chunks):
    """Разбиение списка на заданное количество частей"""
    chunk_size = len(data) // number_of_chunks
    return [data[i * chunk_size:(i + 1) * chunk_size] for i in range(number_of_chunks)]


news = fetch_20newsgroups(subset='all')
data = news.data*10
num_chunks = multiprocessing.cpu_count()

if __name__ == "__main__":
    start_time = time.time()
    pool = Pool(num_chunks)
    data_chunks = chunkify(data, num_chunks)

    # Шаг 1: Распараллеленный mapper + частичное уменьшение
    mapped = pool.map(chunk_mapper, data_chunks)

    # Шаг 2: Финальное объединение результатов
    final_result = reduce(reducer, mapped)

    # Завершение пула процессов
    pool.close()
    pool.join()

    # Время выполнения
    elapsed_time = time.time() - start_time

    # Спрашиваем у пользователя слово
    user_word = input("Enter a word to check its occurrences (or press Enter to show top 10 words): ").strip().lower()

    if user_word:
        # Очистка пользовательского слова
        clean_user_word = clean_word(user_word)
        count = final_result.get(clean_user_word, 0)
        print(f"\nThe word '{user_word}' appears {count} times in the dataset.")
    else:
        # Вывод топ-10 слов
        print("\nTop 10 most common words:")
        print("-" * 30)
        for rank, (word, count) in enumerate(final_result.most_common(10), start=1):
            print(f"{rank:>2}. {word:<15} - {count:>6} occurrences")
        print("-" * 30)

    print(f"Processing completed in {elapsed_time:.2f} seconds.")
