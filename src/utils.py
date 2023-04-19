def convert_ms_to_min_sec(ms: int) -> dict:
    seconds = int((ms/1000)%60)
    minutes = int((ms/(1000*60))%60)
    return {
        "minutes": minutes,
        "seconds": seconds
    }

def convert_ms_to_readable(ms: int) -> str:
    min_sec_dict = convert_ms_to_min_sec(ms)
    return f"{min_sec_dict['minutes']}m{min_sec_dict['seconds']}s"