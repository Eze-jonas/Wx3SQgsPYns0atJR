def classify_momentum(momentum: float) -> str:
    if momentum > 0:
        return "UP"
    elif momentum < 0:
        return "DOWN"
    else:
        return "FLAT"