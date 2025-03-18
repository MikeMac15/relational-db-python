def print_data(data):
    if not data:
        print("No records found.")
        return

    # Assuming data is a list of dictionaries
    headers = data[0].keys()
    column_widths = [max(len(str(record[key])) for record in data) for key in headers]
    column_widths = [max(len(header), width) for header, width in zip(headers, column_widths)]  # Ensure headers fit

    # Print Header
    header_row = " | ".join(header.ljust(column_widths[i]) for i, header in enumerate(headers))
    print(header_row)
    print("=" * len(header_row))  # Separator line

    # Print Rows
    for record in data:
        row = " | ".join(str(record[key]).ljust(column_widths[i]) for i, key in enumerate(headers))
        print(row)

    print("=" * len(header_row))  # Bottom border