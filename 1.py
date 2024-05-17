#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Разработать приложение, в котором выполнить решение вычислительной задачи
# (например, задачи из области физики, экономики, математики, статистики и
# т. д.) с помощью паттерна “Производитель-Потребитель”.

import math
from threading import Thread, Barrier

barrier = Barrier(2)
result_p_0 = []
result_p_omk = []


def P_0(p, N, l):
    sum_series = sum([(p**k) / math.factorial(k) for k in range(N+1)])
    extra_term = ((p**(N+1)) / (N * math.factorial(N))) * \
        ((1 - (p/N)**l) / (1 - p/N))
    result_p_0.append((sum_series + extra_term)**(-1))
    barrier.wait()


def P_omk(p, N, l):
    barrier.wait()
    result_p_omk.append(
        ((p/N)**l) * ((p**N) / math.factorial(N)) * result_p_0[0])


def main():
    p = 0.25  # интенсивность трафика
    N = 2     # Количество продавцов
    l = 5     # Максимум в очереди

    thread1 = Thread(target=P_0, args=(p, N, l))
    thread2 = Thread(target=P_omk, args=(p, N, l))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("P_0:", result_p_0[0])
    print("P_omk:", result_p_omk[0])


if __name__ == "__main__":
    main()
