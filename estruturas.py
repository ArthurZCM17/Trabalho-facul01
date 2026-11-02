import heapq
import itertools


class FilaPrioridade:
    """Fila de prioridade implementada sobre um heap binário mínimo (heapq).

    Sai primeiro quem tem a MENOR tupla de prioridade. Se a prioridade empatar,
    sai quem entrou antes (contador de chegada), então a ordem é sempre estável.
    Inserir e remover custam O(log n); espiar custa O(1).
    """

    def __init__(self):
        self._heap = []
        self._contador = itertools.count()

    def inserir(self, item, *prioridade):
        # (prioridade, contador, item): o contador é único, então o heap
        # nunca precisa comparar os itens entre si
        heapq.heappush(self._heap, (prioridade, next(self._contador), item))

    def remover(self):
        if self.vazia():
            return None
        return heapq.heappop(self._heap)[2]

    def espiar(self):
        return None if self.vazia() else self._heap[0][2]

    def vazia(self):
        return not self._heap

    def __len__(self):
        return len(self._heap)

    def em_ordem(self):
        """Itens na ordem em que serão atendidos, sem remover da fila."""
        return [entrada[2] for entrada in sorted(self._heap)]
