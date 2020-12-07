import numpy as np
import random

INF = 1000000000

class Graph:
    n = 0  # количество вершин
    m = 0  # количество рёбер
    s = 0  # исток
    t = 0  # сток
    D = np.array([])  # массив расстояний
    F = np.array([[]])  # матрица значений потоков
    C = np.array([[]])  # матрица значений пропускных способностей
    ptr = np.array([])  # указатель на "неудаленное" ребро для обхода в глубину

    def __init__(self, n):
        self.n = n
        self.s = 0
        self.t = n - 1
        self.C = np.zeros((n, n))
        self.F = np.zeros((n, n))
        self.D = np.zeros(n)
        self.ptr = np.zeros(n)
        for i in range(n):
            for j in range(i + 1, n):
                if j == i+1 or random.random() > 0.35:  # создание случайных ребер и создание ребер для одного гарантированного пути из s в t
                    c = random.randint(1, 300)  # случайная пропускная способность
                    self.C[i][j] = c
                    self.m += 1

    # breadth-first search
    def bfs(self):
        Q = []
        Q.append(self.s)
        self.D.fill(-1)  # заполняем массив расстояний -1
        self.D[self.s] = 0
        while Q:
            u = Q.pop(0)
            for v in range(u+1, self.n):  # проходимся по всевозможным ребрам (uv)
                if self.D[v] == -1 and self.F[u][v] < self.C[u][v]:  # если есть ребро между верщинами, если еще не определили расстояние до вершины и поток ребра меньше пропускной способности
                    self.D[v] = self.D[u] + 1  # расстояние до вершины v на 1 больше расстояния до вершины u
                    Q.append(v)
        return self.D[self.t] != -1

    # поиск блокирующего потока
    # depth-first search
    def dfs(self, u, flow):  # u — номер вершины, flow — минимальная пропускная способность дополняющей сети на пройденном dfs пути
        if not flow or u == self.t:
            return flow
        for v in range(int(self.ptr[u]), self.n):
            if self.D[v] == self.D[u] + 1:  # это условие эквивалентно поиску во вспомогательной слоистой сети
                delta = self.dfs(v, min(flow, self.C[u][v] - self.F[u][v]))
                if delta:
                    self.F[u][v] += delta  # насыщаем ребра по пути dfs
                    self.F[v][u] -= delta
                    return delta
            self.ptr[u] += 1  # сдвигаем указатель на первое "неудаленное" ребро
        return 0

    def Dinic(self):
        max_flow = 0
        while self.bfs():  # пересчитываем расстояния d, а заодно проверяем достижимость t из s
            self.ptr.fill(0)
            flow = self.dfs(self.s, INF)
            while flow:
                max_flow += flow
                flow = self.dfs(self.s, INF)
        return max_flow
