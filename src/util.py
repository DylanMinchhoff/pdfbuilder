from collections import defaultdict


class SequentialNameGenerator:
    def __init__(self):
        self.cache = defaultdict[str, int](int)

    def __call__(self, prefix: str) -> str:
        count = self.cache[prefix]
        self.cache[prefix] = count + 1
        return f"_{prefix}{count}"
