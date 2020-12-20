from dinic import Graph
import time
import matplotlib.pyplot as plt
import numpy as np


vertices = range(5, 101)

edges = []
time_results = []
f = open('results/time.txt', 'w')
for i in vertices:
    time_i = []
    for j in range(10):
        g = Graph(i)
        start_time = time.time()
        g.Dinic()
        work_time = time.time() - start_time
        time_i.append(work_time * 100)
    edges.append(g.m)
    work_time = np.array(time_i).mean()
    time_results.append(work_time)
    f.write(str(work_time) + '\n')
f.close()


def plt_time_results():
    plt.title('Результаты работы алгоритма')
    plt.xlabel('n - количество вершин в графе, шт')
    plt.ylabel('Время работы алгоритма, мс')
    plt.scatter(vertices, time_results)
    # plt.show()
    plt.savefig('results/time_results.png')
    plt.close()


def plt_ratio_to_theoretical():
    plt.title('Отношение измеренной трудоемкости к теоретической')
    plt.xlabel('n - количество вершин в графе, шт')
    theoretical_results = [n**2 * m for n, m in zip(vertices, edges)]
    ratio = [emp/th for emp, th in zip(time_results, theoretical_results)]
    plt.scatter(vertices, ratio, s=5, c='r')
    plt.plot(vertices, ratio)
    # plt.show()
    plt.savefig('results/ratio_to_theoretical.png')
    plt.close()


def plt_ratio_to_doubled():
    time_results_doubled = []
    for i in vertices:
        g_doubled = Graph(i * 2)
        start_time = time.time()
        g_doubled.Dinic()
        work_time = time.time() - start_time
        time_results_doubled.append(work_time * 100)
    plt.title('Отношение значений трудоемкости\nпри удвоении размера входных данных')
    plt.xlabel('n - количество вершин в графе, шт')
    ratio = [t1/t2 for t1, t2 in zip(time_results, time_results_doubled)]
    plt.scatter(vertices, ratio)
    plt.plot(vertices, ratio)
    # plt.show()
    plt.savefig('results/ratio_to_doubled_size.png')
    plt.close()


plt_time_results()
plt_ratio_to_theoretical()
plt_ratio_to_doubled()
