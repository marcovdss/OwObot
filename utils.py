def format_duration(ms):
    seconds = (ms // 1000) % 60
    minutes = (ms // 1000) // 60
    return f"{minutes}m {seconds}s"

def clean_character_name(name):
    return name.replace("_", " ")
