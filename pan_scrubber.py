import re

def scrub(pan: str, first: int=6, last: int=-4) -> str:
    pan = pan.strip()
    fst, lst = pan[:first], pan[last:]
    r_pan = pan[first:last]
    txt = (fst + r_pan.replace(r_pan, ("."*len(r_pan))) + lst)

    return txt


def is_full_pan(n: str) -> bool:
    is_pan = False
    pattern = r"^[0-9]{13,19}"
    if re.match(pattern, n):
        is_pan = True
    return is_pan

