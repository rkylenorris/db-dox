from sqlglot import transpile

def format_sql(sql: str, dialect: str = "tsql"):
    """
    Formats the given SQL string to the specified dialect using sqlglot.
    
    Args:
        sql (str): The SQL query string to format.
        dialect (str): The target SQL dialect (default is 'tsql').
        
    Returns:
        str: The formatted SQL query string.
    """
    try:
        formatted_sql = transpile(sql, read=dialect, write=dialect)
        return formatted_sql[0] if formatted_sql else sql
    except Exception as e:
        print(f"Error formatting SQL: {e}")
        return sql
