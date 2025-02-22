def generate_binary_format(fields:list):
    """
    Converts a schema into a struct format string for binary storage.
    """
    format_string = []
    for field in fields:
        if field.type == "int":
            format_string.append("i")  # 4-byte integer
        elif field.type == "str":
            format_string.append(f"{field.max_size}s")  # Fixed-size string

    return "".join(format_string)



