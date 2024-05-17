#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 9
# С использованием многопоточности для заданного значения x найти сумму ряда S
# с точностью члена ряда по абсолютному значению e=10^-7 и произвести
# сравнение полученной суммы с контрольным значением функции y для двух
# бесконечных рядов.
# Варианты 16 и 17

# 10
# Для своего индивидуального задания лабораторной работы 2.23 необходимо
# организовать конвейер, в котором сначала в отдельном потоке вычисляется
# значение первой функции, после чего результаты вычисления должны передаваться
# второй функции, вычисляемой в отдельном потоке. Потоки для вычисления
# значений двух функций должны запускаться одновременно.

import math
from threading import Thread, Barrier

epsilon = 1e-7
barrier = Barrier(3)


def func(x, result):
    sum = 0
    n = 0
    term = 1
    while abs(term) > epsilon:
        sum += term
        n += 1
        term = (-1)**n * x**(2 * n) / math.factorial(n)
    result.append(sum)
    barrier.wait()


def func2(x, result):
    sum = 0
    n = 1
    while True:
        term = 1 / (2 * n - 1) * ((x - 1) / (x + 1))**(2 * n - 1)
        if abs(term) < epsilon:
            break
        else:
            sum += term
            n += 1
    result.append(sum)
    barrier.wait()


def test(result1, result2):
    # Ожидание, пока обе функции завершат свою работу, чтобы потом проверить правильность результатов
    barrier.wait()
    sum_func = result1[0]
    sum_func2 = result2[0]

    test1 = math.exp(-(-0.7)**2)
    test2 = 1/2 * math.log(0.6)

    print(f"Результат функции 1: {sum_func}")
    print(f"Контрольное значение для функции 1: {test1}")
    print(f"Результат функции 2: {sum_func2}")
    print(f"Контрольное значение для функции 2: {test2}")

    if abs(sum_func - test1) < epsilon:
        print("func: Верно.")
    else:
        print("func: Неверно.")

    if abs(sum_func2 - test2) < epsilon:
        print("func2: Верно.")
    else:
        print("func2: Неверно.")


def main():
    result1 = []
    result2 = []

    thread1 = Thread(target=func, args=(-0.7, result1))
    thread2 = Thread(target=func2, args=(0.6, result2))
    thread3 = Thread(target=test, args=(result1, result2))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()


if __name__ == "__main__":
    main()
