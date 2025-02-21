from astrapy import DataAPIClient
import pandas as pd

def vectorSearch():
    # Perform a vector search
    query = "I'd like emails addressed to John, Mark, Henry, and James"
    results = db.emails.find(
        {"$and":[ 
            {"emailNumber": "email1"}
        ]},
        sort={"$vectorize": query},
        limit=10,
        projection={"$vectorize": True},
        include_similarity=True,
    )
    print(f"Vector search results for '{query}':")
    for document in results:
        print("    ", document)


def addDataToCollection():
    # Load CSV file (replace 'your_file.csv' with the actual file name)
    df = pd.read_csv(r"C:\Users\theex\SuperBenjiUbuntuServer\database\emails.csv")

    # Specify the column containing text to vectorize (replace 'text_column' with the actual column name)
    text_column = "Body"
    email_id_column = "emailId"
    email_number_collumn = "EmailNumber"

    # Convert CSV rows into vectorizable document format with `emailId`
    documents = [
        {"emailId": row[email_id_column], "$vectorize": row[text_column], "emailNumber": row[email_number_collumn]}
        for _, row in df.dropna(subset=[text_column, email_id_column]).iterrows()
    ]

    # Insert documents into the collection
    insertion_result = db.emails.insert_many(documents)
    print(f"* Inserted {len(insertion_result.inserted_ids)} items.\n")


# Initialize the client
client = DataAPIClient("AstraCS:dQaxkjUvivZJeWDdrfnbcuSn:6f36d7f85947db1d3c5dc8d73aa5aa0b8f2836630b47233a563a4c40a2041ad0")
db = client.get_database_by_api_endpoint(
  "https://4d87ec51-7223-4c2f-acda-7a363be02047-us-east-2.apps.astra.datastax.com",
    keyspace="testing_keyspace",
)

      
print(f"Connected to Astra DB: {db.list_collection_names()}")

# addDataToCollection()
vectorSearch()





