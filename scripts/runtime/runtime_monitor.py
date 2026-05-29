import time

def format_runtime(start_time: float) -> str:
    runtime_seconds = int(time.time() - start_time)

    hours = runtime_seconds // 3600
    minutes = (runtime_seconds % 3600) // 60
    seconds = runtime_seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"