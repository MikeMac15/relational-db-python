def display_table_results(table_name:str,fields:list,records:dict):
    if records:
        headers = [field.name for field in fields]
        column_widths = [max(len(str(record[field.name])) for record in records) for field in fields]
        column_widths = [max(len(header), width) for header, width in zip(headers, column_widths)]  # Ensure headers fit

        # Print Header
        header_row = " | ".join(header.ljust(column_widths[i]) for i, header in enumerate(headers))
        print(f"\nRecords in table: {table_name}")
        print("=" * len(header_row))  # Top border
        print(header_row)
        print("=" * len(header_row))  # Separator line

        # Print Rows
        for record in records:
            row = " | ".join(str(record[field.name]).ljust(column_widths[i]) for i, field in enumerate(fields))
            print(row)

        print("=" * len(header_row))  # Bottom border
    else:
        print("No records found.")
