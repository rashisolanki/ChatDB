import spacy

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Example collection mapping (you can customize this according to your schema)
def map_columns(query):
    column_mappings = {
        "rating": "review_score",
        "ingredients": "item_list",
        "country": "nation",
        "recipes": "dish_collection",
        "average": "avg",
        "review": "review_score"
    }

    # Replace column names in the query according to the mapping
    for key, value in column_mappings.items():
        query = query.replace(key, value)
    return query

# Function to process the query using spaCy's NLP pipeline
def process_query(query):
    # Step 1: Apply column mapping first
    query_with_columns = map_columns(query)
    
    # Step 2: Process the query using spaCy NLP pipeline (lemmatization and stopword removal)
    doc = nlp(query_with_columns)
    
    # Lemmatization and stop word removal
    processed_tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    
    # Extract entities (e.g., country, dish type) using spaCy's NER
    entities = {ent.label_: ent.text for ent in doc.ents}
    
    return processed_tokens, entities

# Function to map keywords to appropriate collections
def get_collection_name(query):
    # Simple mapping of query keywords to collections
    if "recipe" in query or "dish" in query:
        return "dish_collection"
    elif "review" in query or "rating" in query:
        return "user_reviews"
    elif "ingredient" in query:
        return "ingredient_collection"
    elif "user" in query:
        return "user_data"
    else:
        return "default_collection"  # In case no collection is matched

# Function to translate the processed NLP query into a NoSQL query
def translate_nlp_to_nosql_query_string(nlp_statement):
    # Process the query (lemmatization, stopword removal)
    tokens, entities = process_query(nlp_statement)
    
    # Determine which collection to query
    collection_name = get_collection_name(nlp_statement)
    
    # Initialize empty query string
    query_string = ""

    # Example rules for different types of queries
    if "avg" in tokens or "average" in tokens:
        if "review_score" in tokens and "recipes" in tokens:
            if "country" in entities:  # e.g., "from the country India"
                country = entities.get("GPE", "India")  # Default to India if no country found
                query_string = f'db.{collection_name}.aggregate([{{"$match": {{"nation": "{country}"}}}},{{"$group": {{"_id": null, "averageRating": {{"$avg": "$review_score"}}}}}}])'
    
    elif "find" in tokens or "list" in tokens:
        if "recipes" in tokens:
            query_string = f'db.{collection_name}.find()'  # A general query for fetching all recipes
    
    elif "top" in tokens and "rating" in tokens:
        query_string = f'db.{collection_name}.find().sort({{"review_score": -1}}).limit(5)'  # Top rated recipes
    
    elif "group" in tokens and "continent" in tokens:
        query_string = f'db.{collection_name}.aggregate([{{"$group": {{"_id": "$continent", "count": {{"$sum": 1}}}}}}])'  # Example aggregation by continent
    
    # Add more NLP-based transformations as needed

    return query_string

# Main function to take user input and translate it into a NoSQL query
def main():
    print("Type your natural language query:")
    nlp_statement = input("Enter your query: ")

    query_string = translate_nlp_to_nosql_query_string(nlp_statement)
    if query_string:
        print("\nGenerated NoSQL Query:")
        print(query_string)
    else:
        print("Sorry, I couldn't understand your query.")

if __name__ == "__main__":
    main()