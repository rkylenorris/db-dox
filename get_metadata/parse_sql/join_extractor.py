import sqlglot
from sqlglot import expressions as exp

def extract_joins(sql: str):
    """
    Extracts join information from a SQL query using sqlglot.
    Returns a list of dicts with left_table, right_table, columns, and join_type.
    """
    parsed = sqlglot.parse_one(sql)
    joins = []
    for join in parsed.find_all(exp.Join):
        join_type = join.args.get("kind", "INNER").upper()
        right_table_expr = join.this
        right_table = right_table_expr.sql() if right_table_expr else None
        # Find the left table by traversing up the tree
        left_table = None
        parent = join.parent
        while parent:
            if isinstance(parent, exp.From):
                left_table_expr = parent.this
                left_table = left_table_expr.sql() if left_table_expr else None
                break
            parent = getattr(parent, 'parent', None)
        # Extract join columns from ON expression
        columns = []
        on_expr = join.args.get("on")
        if on_expr:
            for eq in on_expr.find_all(exp.EQ):
                left_col = eq.left.sql()
                right_col = eq.right.sql()
                columns.append((left_col, right_col))
        joins.append({
            "left_table": columns[0][0].split('.')[0] if columns else left_table,
            "right_table": right_table,
            "columns": columns,
            "join_type": join_type
        })
    return joins

def extract_tables_and_aliases(sql: str):
    """
    Extracts all tables and their aliases from a SQL query using sqlglot.
    Returns a list of dicts with 'table' and 'alias' keys.
    """
    parsed = sqlglot.parse_one(sql)
    tables = []
    for table in parsed.find_all(exp.Table):
        table_name = table.name
        alias = None
        # Check if parent is an alias expression
        parent = table.parent
        if isinstance(parent, exp.Alias):
            alias = parent.alias_or_name
        tables.append({
            'table': table_name,
            'alias': alias
        })
    return tables

# Example usage
if __name__ == "__main__":
    sql = """
    SELECT * FROM a
    INNER JOIN b ON a.id = b.a_id
    LEFT JOIN c ON b.id = c.b_id AND c.flag = 1
    """
    for join in extract_joins(sql):
        print(join)
