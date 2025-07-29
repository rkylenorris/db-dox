import sqlglot
from sqlglot import expressions as exp

def extract_joins(sql: str):
    """
    Extracts join information from a SQL query using sqlglot.
    Returns a list of dicts with left_table, right_table, columns, and join_type.
    """
    parsed = sqlglot.parse_one(sql)
    tables_and_aliases = get_tables_and_aliases(sql)
    tables = tables_and_aliases["tables"]
    aliases = tables_and_aliases["aliases"]
    print(tables, aliases)
    joins = []
    for join in parsed.find_all(exp.Join):
        join_type = join.args.get("kind", "INNER").upper()
        right_table_expr = join.this
        right_table = right_table_expr.sql().split('AS')[0] if right_table_expr else None
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
        
        left_alias = columns[0][0].split('.')[0] if columns else left_table
        print(left_alias)
        if left_alias in aliases:
            index = aliases.index(left_alias)
            print(index)
            left_table = tables[index]
            print(left_table)
        
        joins.append({
            "left_table": left_table,
            "right_table": right_table,
            "columns": columns,
            "join_type": join_type
        })
    return joins


def get_tables_and_aliases(sql: str) -> dict[str, list[str]]:
    """
    Parses the given SQL string and prints the table name and alias (if any) for each table used.
    
    Args:
        sql (str): The SQL query string to analyze.
    """
    parsed = sqlglot.parse_one(sql)
    
    tables = {
        "tables": [],
        "aliases": []
    }
    for table in parsed.find_all(exp.Table):
        table_name = table.name  # actual table name
        alias = None

        # Check if the parent node is an alias expression
        parent = table.parent
        if isinstance(parent, exp.From) or isinstance(parent, exp.Join):
            alias = parent.alias_or_name
        
        tables["tables"].append(table_name)
        tables["aliases"].append(alias or None)
    
    return tables


# Example usage
if __name__ == "__main__":
    sql = """
    SELECT * FROM act as a
    INNER JOIN bad as b ON a.id = b.a_id
    LEFT JOIN cat as c ON b.id = c.b_id AND c.flag = 1
    """
    for join in extract_joins(sql):
        print(join)
    
    # sql = """
    # SELECT u.name, o.amount
    # FROM users u
    # JOIN orders o ON u.id = o.user_id
    # """
    # get_tables_and_aliases(sql)
