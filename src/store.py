class Store[V]:
    def __init__(self) -> None:
        self.memory: dict[int, V] = {}
        self.allocated_blocks: dict[int, int] = {}
        self.next_free = 0

    def malloc(self, size: int) -> int:
        base = self.next_free
        self.allocated_blocks[base] = size
        self.next_free += size
        return base

    def __setitem__(self, address: tuple[int, int], value: V) -> None:
        base, offset = address
        match self.allocated_blocks.get(base):
            case int(size) if offset in range(0, size):
                self.memory[base + offset] = value
            case _:  # pragma: no cover
                raise IndexError(f"Invalid address: {base}+{offset}")

    def __getitem__(self, address: tuple[int, int]) -> V:
        base, offset = address
        match self.allocated_blocks.get(base):
            case int(size) if offset in range(0, size):
                return self.memory[base + offset]
            case _:  # pragma: no cover
                raise IndexError(f"Invalid address: {base}+{offset}")
