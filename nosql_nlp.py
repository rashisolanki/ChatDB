import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Templates for matching different query operations
templates = {
    'find': re.compile(r"(find|search)\s*for\s*(\w+)\s*where\s*(.*)", re.IGNORECASE),
    'count': re.compile(r"count\s*(\w+)\s*where\s*(.*)", re.IGNORECASE),
    'distinct': re.compile(r"get\s*distinct\s*(\w+)\s*from\s*(\w+)", re.IGNORECASE),
    'aggregate': re.compile(r"aggregate\s*(\w+)\s*by\s*(\w+)", re.IGNORECASE),
    'contains': re.compile(r"Retrieve\s*all\s*(\w+)\s*containing\s*\"([^\"]+)\"", re.IGNORECASE),
    'startswith_number': re.compile(r"Recipes\s*with\s*ingredients\s*starting\s*with\s*a\s*number", re.IGNORECASE),
    'more_than_ingredients': re.compile(r"Find\s*recipes\s*with\s*more\s*than\s*(\d+)\s*ingredients", re.IGNORECASE),
}

# Collection mappings based on common terms
collection_mappings = {
    "recipes": ["recipe", "title", "ingredients", "instructions", "nutrients", "continent", "country_state"],
    "ingredients": ["ingredient", "recipe_id", "ingredient_name"],
    "instructions": ["instruction", "step_number", "recipe_id"],
    "nutrients": ["calories", "carbohydrateContent", "cholesterolContent", "fiberContent", "proteinContent"]
}

# Function to find which collection the query pertains to
def identify_collection(query):
    query = query.lower()
    for collection, keywords in collection_mappings.items():
        for keyword in keywords:
            if keyword in query:
                return collection
    return None  # In case no collection is identified

# Function to clean up conditions
def clean_condition(condition):
    # Remove unnecessary words like 'is' and 'and', and properly format the condition
    condition = condition.lower().replace("is", "").replace("and", "").strip()
    # Check if the condition is a number or string and return it accordingly
    if condition.isdigit():
        return condition
    else:
        return f"'{condition}'"  # Enclose string values in quotes

# Function to process and generate MongoDB query
def translate_to_mongo(query):
    doc = nlp(query.lower())
    
    collection = identify_collection(query)
    if not collection:
        return "Collection not recognized."

    for operation, pattern in templates.items():
        match = pattern.search(query)
        if match:
            if operation == 'find':
                field = match.group(2)
                condition = match.group(3)
                condition_str = clean_condition(condition)
                return f'db.{collection}.find({{"{field}": {condition_str}}})'
            elif operation == 'count':
                field = match.group(1)
                condition = match.group(2)
                condition_str = clean_condition(condition)
                return f'db.{collection}.count({{"{field}": {condition_str}}})'
            elif operation == 'distinct':
                field = match.group(1)
                return f'db.{collection}.distinct("{field}")'
            elif operation == 'aggregate':
                group_by = match.group(2)
                return f'db.{collection}.aggregate([{{ "$group": {{"_id": "${group_by}"}} }}])'
            elif operation == 'contains':
                collection_name = match.group(1)
                keyword = match.group(2)
                return f'db.{collection_name}.find({{ "ingredient_name": //{keyword}//i }})'
            elif operation == 'startswith_number':
                return 'db.ingredients.find({ "ingredient_name": /^[0-9]/ })'
            elif operation == 'more_than_ingredients':
                ingredient_count = match.group(1)
                return f'db.ingredients.aggregate([{{ "$group": {{"_id": "$recipe_id", "count": {{ "$sum": 1 }} }} }}, {{ "$match": {{ "count": {{ "$gt": {ingredient_count} }} }} }}])'
    
    return "Query format not recognized."

# Example usage
queries = [
    "count ingredients where recipe_id is 1",
    "get distinct ingredient_name from ingredients",
    "aggregate recipes by title",
    "Recipes with ingredients starting with a number",
    "Find recipes with more than 5 ingredients"
]

for q in queries:
    print(f"Input: {q}\nOutput: {translate_to_mongo(q)}\n")
