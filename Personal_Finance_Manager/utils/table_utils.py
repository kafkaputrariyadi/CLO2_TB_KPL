def display_table(headers, rows):
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    format_str = " | ".join(["{:<" + str(width) + "}" for width in col_widths])

    print("\n" + format_str.format(*headers))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))

    for row in rows:
        print(format_str.format(*row))
