import random

# Sample SQL query patterns and descriptions
query_patterns = {
    "group_by": [
        "SELECT {categorical}, SUM({quantitative}) FROM {table} GROUP BY {categorical};",
        "SELECT {categorical}, AVG({quantitative}) FROM {table} GROUP BY {categorical};",
        "SELECT {categorical}, MAX({quantitative}) FROM {table} GROUP BY {categorical};",
        "SELECT {categorical}, MIN({quantitative}) FROM {table} GROUP BY {categorical};",
        "SELECT {categorical}, COUNT({quantitative}) FROM {table} GROUP BY {categorical};"
    ],
    "order_by": [
        "SELECT {columns} FROM {table} ORDER BY {categorical} {order};",
        "SELECT {columns} FROM {table} ORDER BY {categorical} DESC;",
        "SELECT {columns} FROM {table} ORDER BY {categorical} ASC;",
        "SELECT {columns} FROM {table} ORDER BY {categorical} {order}, {quantitative} DESC;"
    ],
    "having": [
        "SELECT {categorical}, SUM({quantitative}) FROM {table} GROUP BY {categorical} HAVING SUM({quantitative}) > {threshold};",
        "SELECT {categorical}, MIN({quantitative}) FROM {table} GROUP BY {categorical} HAVING MIN({quantitative}) > {threshold};",
        "SELECT {categorical}, AVG({quantitative}) FROM {table} GROUP BY {categorical} HAVING AVG({quantitative}) > {threshold};",
        "SELECT {categorical}, MAX({quantitative}) FROM {table} GROUP BY {categorical} HAVING MAX({quantitative}) > {threshold};",
        "SELECT {categorical}, COUNT({quantitative}) FROM {table} GROUP BY {categorical} HAVING COUNT({quantitative}) > {threshold};"
    ],
    "join": [
        # "SELECT {column} FROM {table} t JOIN {join_table} p ON t.product_id = p.product_id;",
        # "SELECT t.{base_column}, p.{join_column} FROM {table} t JOIN {join_table} p ON t.product_id = p.product_id;",
        "SELECT t.{base_column}, p.{join_column} FROM {table} t JOIN {join_table} p ON t.store_id = p.store_id;"
    ],
    "aggregation": [
        "SELECT {agg_function}({quantitative}) FROM {table};",
        "SELECT {agg_function}({quantitative}) AS result FROM {table};",
        "SELECT {agg_function}({quantitative}) FROM {table} WHERE {condition};",
        "SELECT {agg_function}({quantitative}) FROM {table} GROUP BY {categorical};"
    ]
}

nl_descriptions = {
    "group_by": [
        "Total {quantitative} by {categorical}.",
        "Average {quantitative} by {categorical}.",
        "Maximum {quantitative} by {categorical}.",
        "Minimum {quantitative} by {categorical}.",
        "Count of {quantitative} by {categorical}."
    ],
    "order_by": [
        "All records ordered by {categorical} in {order} order.",
        "All records ordered by {categorical} in descending order.",
        "All records ordered by {categorical} in ascending order.",
        "All records sorted by {categorical} and {quantitative} in {order} order."
    ],
    "having": [
        "Filter records where SUM({quantitative}) is greater than {threshold}.",
        "Filter records where MIN({quantitative}) is greater than {threshold}.",
        "Filter records where AVG({quantitative}) is greater than {threshold}.",
        "Filter records where MAX({quantitative}) is greater than {threshold}.",
        "Filter records where COUNT({quantitative}) is greater than {threshold}."
    ],
    "join": [
        "Join transactions with products on product_id.",
        "Join transactions and products where product_id matches.",
        "Join transactions with products on store_id.",
        "Join transactions with products using INNER JOIN based on product_id."
    ],
    "aggregation": [
        "The {agg_function} of {quantitative} from {table}.",
        "Get the {agg_function} of {quantitative} from {table}.",
        "Aggregate {quantitative} using {agg_function} from {table}.",
        "Calculate {agg_function} of {quantitative} from {table}."
    ]
}

# Sample metadata structure for tables and their attributes
metadata = {
    "transactions": {
        "categorical": ["transaction_id", "product_id", "store_id"],
        "quantitative": ["transaction_qty"]
    },
    "products": {
        "categorical": ["product_id", "store_id", "product_type", "product_category"],
        "quantitative": ["unit_price"]
    }
}

# Function to generate queries dynamically
def generate_queries(clause, attributes, table=None, max_queries=4):
    queries = []

    # Check if the table has quantitative and categorical attributes
    has_quantitative = "quantitative" in attributes if attributes else False
    has_categorical = "categorical" in attributes if attributes else False

    if clause == "having" and has_quantitative and has_categorical:
        operators = ["=", ">", "<", ">=", "<="]  # Define operators for flexibility
        for quantitative in attributes["quantitative"]:
            for categorical in attributes["categorical"]:
                operator = random.choice(operators)
                threshold = random.randint(10, 100)

                # Generate SQL query
                query = (
                    f"SELECT {categorical}, {random.choice(['SUM', 'AVG', 'MIN', 'MAX', 'COUNT'])}({quantitative}) "
                    f"FROM {table} "
                    f"GROUP BY {categorical} "
                    f"HAVING {random.choice(['SUM', 'AVG', 'MIN', 'MAX', 'COUNT'])}({quantitative}) {operator} {threshold};"
                )

                # Generate description
                description = (
                    f"Filter {categorical} records where {quantitative} {operator} {threshold}."
                )

                queries.append((query.strip(), description))

    elif clause == "group_by" and has_quantitative and has_categorical:
        for quantitative in attributes["quantitative"]:
            for categorical in attributes["categorical"]:
                query = query_patterns[clause][0].format(
                    quantitative=quantitative,
                    categorical=categorical,
                    table=table
                )
                description = nl_descriptions[clause][0].format(
                    quantitative=quantitative,
                    categorical=categorical
                )
                queries.append((query, description))

    elif clause == "order_by" and has_categorical:
        for categorical in attributes["categorical"]:
            order = random.choice(["ASC", "DESC"])

            # Randomly select columns for query (not always *)
            columns = random.sample(attributes["categorical"] + attributes["quantitative"], k=random.randint(1, 2))
            columns_str = ", ".join(columns)

            query = query_patterns[clause][0].format(
                columns=columns_str,
                categorical=categorical,
                table=table,
                order=order
            )
            description = nl_descriptions[clause][0].format(
                categorical=categorical,
                order="ascending" if order == "ASC" else "descending"
            )
            queries.append((query, description))

    elif clause == "join" and attributes is None:  # Handle join case where attributes is None
        join_table = "stores"  # Example join table
        base_table = "products"  # Example base table

        # Define some sample columns for variation
        # base_columns = ["transaction_id", "product_id", "transaction_qty"]
        # join_columns = ["product_id", "product_category", "unit_price"]

        base_columns = ["product_id", "unit_price", "product_category", "product_type", "product_detail", "store_id"]
        join_columns = ["store_id", "store_location"]

        for _ in range(max_queries):
            base_column = random.choice(base_columns)
            join_column = random.choice(join_columns)
            query = random.choice(query_patterns[clause]).format(
                # column=f"{base_table}.{base_column}, {join_table}.{join_column}",
                base_column=base_column,
                join_column=join_column,
                table=base_table,
                join_table=join_table
            )
            description = random.choice(nl_descriptions[clause])
            queries.append((query, description))

    elif clause == "aggregation" and has_quantitative:
        for quantitative in attributes["quantitative"]:
            agg_function = random.choice(["SUM", "AVG", "MIN", "MAX", "COUNT"])
            query = query_patterns[clause][0].format(
                agg_function=agg_function,
                quantitative=quantitative,
                table=table
            )
            description = nl_descriptions[clause][0].format(
                agg_function=agg_function.lower(),
                quantitative=quantitative,
                table=table
            )
            queries.append((query, description))
        
    elif clause == "sql_queries":
        # Generate one query and its description for each type in query_patterns
        for query_type, patterns in query_patterns.items():
            if query_type == "group_by" and has_quantitative and has_categorical:
                for quantitative in attributes["quantitative"]:
                    for categorical in attributes["categorical"]:
                        query = patterns[0].format(
                            quantitative=quantitative,
                            categorical=categorical,
                            table=table
                        )
                        description = nl_descriptions[query_type][0].format(
                            quantitative=quantitative,
                            categorical=categorical
                        )
                        queries.append((query, description))
                        break
                    break
            elif query_type == "order_by" and has_categorical:
                for categorical in attributes["categorical"]:
                    order = random.choice(["ASC", "DESC"])
                    columns = random.sample(
                        attributes["categorical"] + attributes["quantitative"], 
                        k=random.randint(1, 2)
                    )
                    columns_str = ", ".join(columns)
                    query = patterns[0].format(
                        columns=columns_str,
                        categorical=categorical,
                        table=table,
                        order=order
                    )
                    description = nl_descriptions[query_type][0].format(
                        categorical=categorical,
                        order="ascending" if order == "ASC" else "descending"
                    )
                    queries.append((query, description))
                    break

            elif query_type == "having" and has_quantitative and has_categorical:
                for quantitative in attributes["quantitative"]:
                    for categorical in attributes["categorical"]:
                        operator = random.choice(["=", ">", "<", ">=", "<="])
                        threshold = random.randint(10, 100)
                        query = patterns[0].format(
                            quantitative=quantitative,
                            categorical=categorical,
                            table=table,
                            threshold=threshold
                        )
                        description = nl_descriptions[query_type][0].format(
                            quantitative=quantitative,
                            threshold=threshold
                        )
                        queries.append((query, description))
                        break
                    break

            elif query_type == "aggregation" and has_quantitative:
                for quantitative in attributes["quantitative"]:
                    agg_function = random.choice(["SUM", "AVG", "MIN", "MAX", "COUNT"])
                    query = patterns[0].format(
                        agg_function=agg_function,
                        quantitative=quantitative,
                        table=table
                    )

                    description = nl_descriptions[query_type][0].format(
                        agg_function=agg_function,
                        quantitative=quantitative,
                        table=table
                    )
                    queries.append((query, description))
                    break

            elif query_type == "join":
                join_table = "products"
                base_table = "transactions"
                query = patterns[0].format(
                    column=f"{base_table}.transaction_id, {join_table}.product_name",
                    table=base_table,
                    join_table=join_table
                )
                description = nl_descriptions[query_type][0]
                queries.append((query, description))

    return queries


    # Shuffle and return a random subset
    random.shuffle(queries)
    return queries[:random.randint(3, max_queries)]

# Main function to handle user input and generate queries
def main():
    print("You can ask for sample queries using clauses like 'group by', 'order by', 'having', 'join', 'aggregation', or 'sql queries'.\n")
    clause = input("Enter your request: ").strip().lower()

    # Match the clause for 'order by', 'having', etc., with different possible variations
    if "order by" in clause:
        clause = "order_by"
    elif "having" in clause:
        clause = "having"
    elif "group by" in clause:
        clause = "group_by"
    elif "aggregation" in clause:
        clause = "aggregation"
    elif "join" in clause:
        clause = "join"
    elif "sql queries" in clause or "sample sql queries" in clause:
        clause = "sql_queries"
    else:
        print(f"Sorry, I couldn't generate any queries for the '{clause}' clause.")
        return

    queries = []

    if clause in ["group_by", "order_by", "having", "aggregation"]:
        for table, attributes in metadata.items():
            queries.extend(generate_queries(clause, attributes, table))
    elif clause == "join":
        queries.extend(generate_queries(clause, attributes=None))
    elif clause == "sql_queries":
        for table, attributes in metadata.items():
            queries.extend(generate_queries(clause, attributes, table))

    # Check if queries were generated and display them
    if queries:
        print(f"\nHere are sample queries for the '{clause}' clause:\n")
        for i, query in enumerate(queries, 1):
            print(f"{i}. SQL Query: {query[0]}\n   Description: {query[1]}\n")
    else:
        print(f"No queries generated for the '{clause}' clause.")

if __name__ == "__main__":
    main()