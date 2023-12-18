import heapq

class BestCost:

    def __init__(self):
        self.so_far = {}
        self.queue = []

    def should_add(self, state, cost):
        if not state in self.so_far:
            return True

        entry = self.so_far[state]
        prev_cost, prev_state, processed = entry
        if prev_cost <= cost:
            return False

        entry[2] = True
        return True
    
    def add(self, state, cost):
        if self.should_add(state, cost):
            entry = [cost, state, False]
            heapq.heappush(self.queue, entry)
            self.so_far[state] = entry

    def get_next(self):
        while self.queue:
            entry = heapq.heappop(self.queue)
            cost, state, processed = entry
            if not processed:
                entry[2] = True
                return (entry[0], entry[1])
        return None
