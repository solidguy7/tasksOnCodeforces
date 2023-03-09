from typing import List

def append_params(param: str or int, lst: List[str or int]) -> None:
    if param not in lst:
        lst.append(param)