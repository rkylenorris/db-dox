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
    # Process FROM clauses
    for from_clause in parsed.find_all(exp.Table):
        print(from_clause.args)
        source = from_clause.args.get("this")
        print(source)
        if isinstance(source, exp.TableAlias):
            table_expr = source.this
            alias = source.alias
            table_name = table_expr.name if isinstance(table_expr, exp.Table) else table_expr.sql()
            tables.append({'table': table_name, 'alias': alias})
        elif isinstance(source, exp.Table):
            tables.append({'table': source.name, 'alias': None})

    # Process JOIN clauses
    for join_clause in parsed.find_all(exp.Join):
        source = join_clause.args.get("this")
        
        if isinstance(source, exp.Alias):
            source_split = str(source).split('AS')
            print(source_split)
            table_expr = exp.Table(name=source_split[0].strip())
            alias = source_split[1].strip() if len(source_split) > 1 else None
            table_name = table_expr.name if isinstance(table_expr, exp.Table) else table_expr.sql()
            tables.append({'table': table_name, 'alias': alias})
        elif isinstance(source, exp.Table):
            tables.append({'table': source.name, 'alias': None})
    return tables



def print_tables_and_aliases(sql: str):
    """
    Parses the given SQL string and prints the table name and alias (if any) for each table used.
    
    Args:
        sql (str): The SQL query string to analyze.
    """
    parsed = sqlglot.parse_one(sql)
    for table in parsed.find_all(exp.Table):
        table_name = table.name  # actual table name
        alias = None

        # Check if the parent node is an alias expression
        parent = table.parent
        if isinstance(parent, exp.From) or isinstance(parent, exp.Join):
            alias = parent.alias_or_name

        print(f"Table: {table_name}, Alias: {alias or 'None'}")


# Example usage
if __name__ == "__main__":
    # sql = """
    # SELECT * FROM act as a
    # INNER JOIN bad as b ON a.id = b.a_id
    # LEFT JOIN cat as c ON b.id = c.b_id AND c.flag = 1
    # """
    # for join in extract_joins(sql):
    #     print(join)
    # for tbl in extract_tables_and_aliases(sql):
    #     print(tbl)
        
    sql = """
    SELECT u.name, o.amount
    FROM users u
    JOIN orders o ON u.id = o.user_id
    """
    print_tables_and_aliases(sql)
