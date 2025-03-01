def generate_binary_format(fields:list):
    """
    Converts a schema into a struct format string for binary storage.
    """
    format_string = ["i"] # 4-byte delete flag 0 = active / 1 = deleted
    for field in fields:
        if field.type == "int":
            format_string.append("i")  # 4-byte integer
        elif field.type == "str":
            format_string.append(f"{field.max_size}s")  # fixed size string

    return "".join(format_string)



