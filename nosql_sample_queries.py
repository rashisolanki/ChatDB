import random

# Sample MongoDB query patterns and descriptions
query_patterns = {
    "find": [
        'db.{collection}.find({{ "{field}": {value} }});',
        'db.{collection}.find({{ "{field}": {{ "$gt": {value} }} }});',
        'db.{collection}.find({{ "{field}": {{ "$lt": {value} }} }});',
        'db.{collection}.find({{ "{field}": {{ "$gte": {value} }} }});',
        'db.{collection}.find({{ "{field}": {{ "$lte": {value} }} }});'
    ],
    # "aggregate": [
    #     'db.{collection}.aggregate([{{ "$group": {{ "_id": "$${group_by_field}", "{agg_function}": {{ "$${agg_function}": "$${aggregate_field}" }} }} }}]);'       
    #     # 'db.{collection}.aggregate([{{ "$match": {{ "{field}": {value} }} }}]);'
    # ],
    "aggregate": [
        'db.recipes.aggregate([{ "$group": { "_id": "$instructions", "sum": { "$sum": "$cook_time" } } }]);',
        'db.recipes.aggregate([{ "$group": { "_id": "$Country_State", "max": { "$max": "$rating" } } }]);', 
        'db.recipes.aggregate([{ "$group": { "_id": "$Continent", "recipeCount": { "$sum": 1 } } }]);',  
        'db.recipes.aggregate([{ "$group": { "_id": "$total_time", "recipeCount": { "$sum": 1 } } }]);'  
    ],
    "count": [
        'db.{collection}.count({{ "{field}": {value} }});',
        'db.{collection}.count({{ "{field}": {{ "$gt": {value} }} }});',
        'db.{collection}.count({{ "{field}": {{ "$lt": {value} }} }});',
        'db.{collection}.count({{ "{field}": {{ "$gte": {value} }} }});'
    ],
    "distinct": [
        'db.{collection}.distinct("{field}");'
        # 'db.{collection}.distinct("{field}", {{ "{filter_field}": {filter_value} }});'
    ],
    "join": [
        'db.{collection1}.aggregate([{{ "$lookup": {{ "from": "{collection2}", "localField": "{local_field}", "foreignField": "{foreign_field}", "as": "{as_field}" }} }}]);'
        # 'db.{collection1}.aggregate([{{ "$match": {{ "{match_field}": {match_value} }} }}, {{ "$lookup": {{ "from": "{collection2}", "localField": "{local_field}", "foreignField": "{foreign_field}", "as": "{as_field}" }} }}]);'
    ]
}

nl_descriptions = {
    "find": [
        "Find documents in {collection} where {field} is {value}.",
        "Find documents in {collection} where {field} is greater than {value}.",
        "Find documents in {collection} where {field} is less than {value}.",
        "Find documents in {collection} where {field} is greater than or equal to {value}.",
        "Find documents in {collection} where {field} is less than or equal to {value}."
    ],
    "aggregate": [
        "Group by query using aggregate.",
        # "Group documents in {collection} by {group_by_field} and aggregate {aggregate_field} using {agg_function}."
        # "Match documents in {collection} where {field} is {value}."
    ],
    "count": [
        "Count documents in {collection} where {field} is {value}.",
        "Count documents in {collection} where {field} is greater than {value}.",
        "Count documents in {collection} where {field} is less than {value}.",
        "Count documents in {collection} where {field} is greater than or equal to {value}."
    ],
    "distinct": [
        "Get distinct values of {field} in {collection}.",
        "Get distinct values of {field} in {collection} where {filter_field} is {filter_value}."
    ],
    "join": [
        "Join {collection1} with {collection2} using {local_field} and {foreign_field}.",
        "Join {collection1} with {collection2} using {local_field} and {foreign_field}, where {match_field} is {match_value}."
    ]
}

# Sample metadata structure for collections and their attributes
metadata = {
    "ingredients": {
        "fields": ["ingredient_name", "recipe_id"]
    },
    "instructions": {
        "fields": ["recipe_id", "Step 1", "Step 2"]
    },
    "nutrients": {
        "fields": [
            "calories", "carbohydrateContent", "cholesterolContent", "fiberContent",
            "proteinContent", "saturatedFatContent", "sodiumContent", "sugarContent",
            "fatContent", "unsaturatedFatContent", "recipe_id"
        ]
    },
    "recipes": {
        "fields": [
            "Continent", "Country_State", "title", "rating", "total_time", "prep_time",
            "cook_time", "description", "serves", "ingredients", "instructions", "nutrients"
        ]
    }
}

def generate_queries(clause, attributes, collection=None):
    queries = []
    if not attributes:
        return queries

    if clause == "find":
        for field in random.sample(attributes["fields"], min(4, len(attributes["fields"]))):
            value = f'"{random.randint(1, 100)}"' if isinstance(field, str) else random.randint(1, 100)
            query = random.choice(query_patterns[clause]).format(
                collection=collection,
                field=field,
                value=value
            )
            description = random.choice(nl_descriptions[clause]).format(
                collection=collection,
                field=field,
                value=value.strip('"')
            )
            queries.append((description, query))
    
    elif clause == "aggregate":
        for _ in range(4):
            group_by_field = random.choice(attributes["fields"])
            aggregate_field = random.choice(attributes["fields"])
            agg_function = random.choice(["sum", "avg", "min", "max"])

            # query = random.choice(query_patterns[clause]).format(
            #     collection=collection,
            #     group_by_field=group_by_field,
            #     agg_function=agg_function,
            #     aggregate_field=aggregate_field
            # )

            query = random.choice(query_patterns[clause])

            description = nl_descriptions[clause]
            
            # description = nl_descriptions[clause][0].format(
            #     collection=collection,
            #     group_by_field=group_by_field,
            #     aggregate_field=aggregate_field,
            #     agg_function=agg_function.lstrip('$')
            # )
            queries.append((description, query))

    elif clause == "count":
        for field in random.sample(attributes["fields"], min(4, len(attributes["fields"]))):
            value = random.randint(1, 100)
            query = random.choice(query_patterns[clause]).format(
                collection=collection,
                field=field,
                value=value
            )
            description = random.choice(nl_descriptions[clause]).format(
                collection=collection,
                field=field,
                value=value
            )
            queries.append((description, query))

    elif clause == "distinct":
        for field in random.sample(attributes["fields"], min(4, len(attributes["fields"]))):
            filter_field = "ingredient_name"
            filter_value = '"sugar"'
            query = random.choice(query_patterns[clause]).format(
                collection=collection,
                field=field,
                filter_field=filter_field,
                filter_value=filter_value
            )
            description = random.choice(nl_descriptions[clause]).format(
                collection=collection,
                field=field,
                filter_field=filter_field,
                filter_value=filter_value.strip('"')
            )
            queries.append((description, query))

    return queries[:4]

def generate_join_queries():
    join_queries = []
    collections = list(metadata.keys())
    for _ in range(4):
        collection1 = random.choice(collections)
        collection2 = random.choice([c for c in collections if c != collection1])
        local_field = random.choice(metadata[collection1]["fields"])
        foreign_field = random.choice(metadata[collection2]["fields"])
        as_field = f"{collection2}_data"
        query_pattern = random.choice(query_patterns["join"])
        if "$match" in query_pattern:
            match_field = random.choice(metadata[collection1]["fields"])
            match_value = f'"{random.randint(1, 100)}"' if isinstance(match_field, str) else random.randint(1, 100)
            query = query_pattern.format(
                collection1=collection1,
                collection2=collection2,
                local_field=local_field,
                foreign_field=foreign_field,
                as_field=as_field,
                match_field=match_field,
                match_value=match_value
            )
            description = nl_descriptions["join"][1].format(
                collection1=collection1,
                collection2=collection2,
                local_field=local_field,
                foreign_field=foreign_field,
                match_field=match_field,
                match_value=match_value.strip('"')
            )
        else:
            query = query_pattern.format(
                collection1=collection1,
                collection2=collection2,
                local_field=local_field,
                foreign_field=foreign_field,
                as_field=as_field
            )
            description = nl_descriptions["join"][0].format(
                collection1=collection1,
                collection2=collection2,
                local_field=local_field,
                foreign_field=foreign_field
            )
        join_queries.append((description, query))
    return join_queries

def main():
    print("You can ask for sample queries using clauses like 'find', 'aggregate', 'count', 'distinct', or 'join'.\n")
    user_input = input("Enter your request: ").strip().lower()
    clauses = ["find", "aggregate", "count", "distinct", "join"]
    clause = next((c for c in clauses if c in user_input), None)

    if clause:
        if clause == "join":
            selected_queries = generate_join_queries()
        else:
            all_queries = []
            for collection, attributes in metadata.items():
                all_queries.extend(generate_queries(clause, attributes, collection))
            selected_queries = random.sample(all_queries, min(4, len(all_queries)))

        if selected_queries:
            print(f"\nHere are sample queries for the '{clause}' clause:\n")
            for i, query in enumerate(selected_queries, 1):
                print(f"{i}. {query[0]}\n   {query[1]}\n")
        else:
            print(f"No queries generated for the '{clause}' clause.")
    else:
        print(f"Sorry, I couldn't generate any queries for the input: '{user_input}'. Please use 'find', 'aggregate', 'count', 'distinct', or 'join' in your request.")

if __name__ == "__main__":
    main()