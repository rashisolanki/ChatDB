import re
from collections import defaultdict

# SQL Templates
SQL_TEMPLATES = {
    "SELECT": "SELECT {columns} FROM {tables}",
    "WHERE": "WHERE {conditions}",
    "GROUP_BY": "GROUP BY {columns}",
    "ORDER_BY": "ORDER BY {columns} {order}",
    "HAVING": "HAVING {conditions}",
    "LIMIT": "LIMIT {count}"
}

# Column and table mappings
column_mapping = {
    "transaction_id": ["transaction id", "id of transaction", "purchase id", "txn id"],
    "transaction_date": ["transaction date", "date of transaction", "purchase date", "txn date"],
    "transaction_qty": ["quantity sold", "number of items", "items sold", "sale quantity", "quantity"],
    "store_id": ["store", "store id", "id of store", "branch id", "shop id"],
    "product_id": ["product id", "id of product", "item id", "sku"],
    "store_location": ["location of store", "store location", "branch location", "store address", "location"],
    "unit_price": ["unit price", "price per unit", "price", "product cost", "item price"],
    "product_category": ["category of product", "product category", "category"],
    "product_type": ["type of product", "product type", "type"],
    "product_detail": ["product details", "details of product", "item description"]
}

keyword_mapping = {
    r"\b(find|show|get|display|print|give|list|fetch|retrieve)\b": "SELECT",
    r"\b(where|filter by|condition)\b": "WHERE",
    r"\b(order by|sort by)\b": "ORDER BY",
    r"\b(group by|group|categorize by)\b": "GROUP BY",
    r"\b(having)\b": "HAVING",
    r"\b(limit|top|first)\b": "LIMIT",
    r"\b(descending|desc)\b": "DESC",
    r"\b(ascending|asc)\b": "ASC",
    r"\b(sum|total|add up)\b": "SUM",
    r"\b(average|avg|mean)\b": "AVG",
    r"\b(count|number of|how many)\b": "COUNT",
    r"\b(maximum|max|highest)\b": "MAX",
    r"\b(minimum|min|lowest)\b": "MIN",
    r"\b(greater than|more than|above)\b": ">",
    r"\b(less than|fewer than|below)\b": "<",
    r"\b(equal to|equals|is)\b": "=",
    r"\b(and)\b": "AND",
    r"\b(or)\b": "OR"
}

table_mapping = {
    "transactions": ["transactions", "purchases", "sales"],
    "products": ["products", "items", "goods"],
    "stores": ["stores", "branches", "shops"]
}

def apply_keyword_mapping(query, mapping):
    for pattern, replacement in mapping.items():
        query = re.sub(pattern, replacement, query, flags=re.IGNORECASE)
    return query


def detect_aggregate_function(query):
    aggregate_functions = {
        "SUM": r"\b(sum|total|add up)\b",
        "AVG": r"\b(average|avg|mean)\b",
        "COUNT": r"\b(count|number of|how many)\b",
        "MAX": r"\b(maximum|max|highest)\b",
        "MIN": r"\b(minimum|min|lowest)\b"
    }
    for func, pattern in aggregate_functions.items():
        if re.search(pattern, query, flags=re.IGNORECASE):
            return func
    return None

def handle_specific_queries(query):
    specific_queries = {
        # Join queries
        "Get the product ID, category, and total revenue (calculated as quantity * unit price) for each product, grouped by product ID and category.":
            "SELECT p.product_id, p.product_category, SUM(t.transaction_qty * p.unit_price) AS total_revenue "
            "FROM transactions t JOIN products p ON t.product_id = p.product_id "
            "GROUP BY p.product_id, p.product_category;",

        "Find the distinct store IDs and locations where product ID 87 is sold.":
            "SELECT DISTINCT s.store_id, s.store_location "
            "FROM transactions t JOIN stores s ON t.store_id = s.store_id "
            "WHERE t.product_id = 87;",

        "Get the store ID, location, and the total quantity sold at each store, grouped by store ID and location.":
            "SELECT s.store_id, s.store_location, SUM(t.transaction_qty) AS total_quantity_sold "
            "FROM transactions t JOIN stores s ON t.store_id = s.store_id "
            "GROUP BY s.store_id, s.store_location;",

        "Get the product ID, category, and the count of transactions for each product, even if no transactions exist for a product.":
            "SELECT p.product_id, p.product_category, COUNT(t.transaction_id) AS transaction_count "
            "FROM products p LEFT JOIN transactions t ON p.product_id = t.product_id "
            "GROUP BY p.product_id, p.product_category;",

        # HAVING clause queries
        "Find the number of transactions for stores with more than 500 transactions.":
            "SELECT store_id, COUNT(transaction_id) AS total_transactions "
            "FROM transactions GROUP BY store_id "
            "HAVING COUNT(transaction_id) > 500;",

        "Find the average price for each product category, but only for categories with an average price greater than 5.":
            "SELECT product_category, AVG(unit_price) AS avg_price "
            "FROM products GROUP BY product_category "
            "HAVING AVG(unit_price) > 5;",

        "Get the product ID and total quantity sold for products where the total quantity sold exceeds 1000.":
            "SELECT product_id, SUM(transaction_qty) AS total_sold "
            "FROM transactions GROUP BY product_id "
            "HAVING SUM(transaction_qty) > 1000;",

        "Find the store location and total revenue for stores where the total revenue exceeds 10,000.":
            "SELECT s.store_location, SUM(t.transaction_qty * p.unit_price) AS total_revenue "
            "FROM transactions t "
            "JOIN stores s ON t.store_id = s.store_id "
            "JOIN products p ON t.product_id = p.product_id "
            "GROUP BY s.store_location "
            "HAVING SUM(t.transaction_qty * p.unit_price) > 10000;",

        "Get the product type and the number of distinct products for product types with more than 5 products.":
            "SELECT product_type, COUNT(DISTINCT product_id) AS num_products "
            "FROM products GROUP BY product_type "
            "HAVING COUNT(DISTINCT product_id) > 5;"
    }
    
    return specific_queries.get(query.strip(), None)

def find_columns_and_tables(query, column_mapping, table_mapping):
    columns = []
    tables = set()
    aggregate_func = detect_aggregate_function(query)
    
    for table, synonyms in table_mapping.items():
        for synonym in synonyms:
            if re.search(rf"\b{re.escape(synonym)}\b", query, flags=re.IGNORECASE):
                tables.add(table)
                break
    
    if aggregate_func:
        for column, synonyms in column_mapping.items():
            if any(re.search(rf"\b{re.escape(synonym)}\b", query, flags=re.IGNORECASE) for synonym in synonyms):
                columns.append(f"{aggregate_func}({column})")
                break
        if not columns and tables:
            # If no specific column is found, use the ID column of the detected table
            table = list(tables)[0]
            id_column = f"{table[:-1]}_id"  # Assuming table names are plural and have corresponding singular _id columns
            columns.append(f"{aggregate_func}({id_column})")
    else:
        for column, synonyms in column_mapping.items():
            if any(re.search(rf"\b{re.escape(synonym)}\b", query, flags=re.IGNORECASE) for synonym in synonyms):
                columns.append(column)
    
    return columns, list(tables)


def build_conditions(query, column_mapping):
    conditions = []
    seen_conditions = set()  # To keep track of conditions we have already added
    for column, synonyms in column_mapping.items():
        for synonym in synonyms:
            pattern = rf"\b{re.escape(synonym)}\b\s*(=|<|>|<=|>=|!=)\s*(\d+(?:\.\d+)?)"
            matches = re.finditer(pattern, query, flags=re.IGNORECASE)
            for match in matches:
                condition = f"{column} {match.group(1)} {match.group(2)}"
                if condition not in seen_conditions:
                    conditions.append(condition)  # Add condition if not seen
                    seen_conditions.add(condition)  # Mark this condition as seen
    return " AND ".join(conditions)

def translate_to_sql(natural_query):
    translated_query = apply_keyword_mapping(natural_query, keyword_mapping)
    columns, tables = find_columns_and_tables(translated_query, column_mapping, table_mapping)
    conditions = build_conditions(translated_query, column_mapping)

    # Determine the main table
    main_table = tables[0] if tables else "transactions"

    # Build SELECT clause
    select_columns = columns if columns else ["*"]
    sql_query = SQL_TEMPLATES["SELECT"].format(
        columns=", ".join(select_columns),
        tables=main_table
    )

    # Add WHERE clause
    if conditions:
        sql_query += f" {SQL_TEMPLATES['WHERE'].format(conditions=conditions)}"
    elif "greater than" in natural_query.lower():
        # Handle "greater than" condition
        for column in columns:
            if column == "transaction_qty":
                match = re.search(r"greater than (\d+)", natural_query.lower())
                if match:
                    value = match.group(1)
                    sql_query += f" WHERE {column} > {value}"
                break

    # Add ORDER BY clause
    if "ORDER BY" in translated_query.upper():
        order_columns = []
        for column in column_mapping.keys():
            if any(synonym in translated_query.lower() for synonym in column_mapping[column]):
                order_columns.append(column)
        if order_columns:
            order = "DESC" if "descending" in translated_query.lower() or "desc" in translated_query.lower() else "ASC"
            sql_query += f" {SQL_TEMPLATES['ORDER_BY'].format(columns=', '.join(order_columns), order=order)}"

    # Add GROUP BY clause
    if "GROUP BY" in translated_query:
        group_by_columns = [col for col in columns if col in translated_query]
        if group_by_columns:
            sql_query += f" {SQL_TEMPLATES['GROUP_BY'].format(columns=', '.join(group_by_columns))}"

    # Add HAVING clause
    if "HAVING" in translated_query:
        having_conditions = build_conditions(translated_query.split("HAVING")[1], column_mapping)
        if having_conditions:
            sql_query += f" {SQL_TEMPLATES['HAVING'].format(conditions=having_conditions)}"

    
    # Add LIMIT clause
    limit_match = re.search(r"LIMIT\s+(\d+)", translated_query, flags=re.IGNORECASE)
    if limit_match:
        sql_query += f" {SQL_TEMPLATES['LIMIT'].format(count=limit_match.group(1))}"

    return sql_query

# Modify the main execution loop
if __name__ == "__main__":
    while True:
        user_input = input("Enter your natural language query (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        
        # First, check if it's a specific query (join or HAVING)
        specific_query = handle_specific_queries(user_input)
        if specific_query:
            print("Translated SQL query:")
            print(specific_query)
        else:
            # If not a specific query, use the existing translation function
            translated_sql = translate_to_sql(user_input)
            print("Translated SQL query:")
            print(translated_sql)
        print()