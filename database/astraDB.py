from astrapy import DataAPIClient
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

cloud_config= {
  'secure_connect_bundle': 'c:/Users/theex/SuperBenjiUbuntuServer/database/secure-connect-superbenjidb.zip'
}

keyspace = "super_benji_client_information"

default_client_style = (1, [], [], 
                        "this is a message to a very important person. Use more formal language and tone throughout",
                        "be positive about the content regarding the prospect but not too positive",
                        "professional",
                        "Invite the prospect to a lunch",
                        "reply to this email to sign up",
                        "Hi, [ProspectName]",
                        "Kind regards,",
                        "UK English",
                        0.5)

def connectToNormalDB():
    with open("c:/Users/theex/SuperBenjiUbuntuServer/database/SuperBenjiDB-token.json") as f:
        secrets = json.load(f)

    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    DBsession = cluster.connect()

    row = DBsession.execute("select release_version from system.local").one()
    if row:
        print(row[0])
    else:
        print("An error occurred.")
    
    return(DBsession)

def createTablesDB():
    session.execute((
        "DROP TABLE IF EXISTS {keyspace}.client_data;"
    ).format(keyspace=keyspace))

    session.execute((
        "DROP TABLE IF EXISTS {keyspace}.client_identity;"
    ).format(keyspace=keyspace))

    session.execute((
        "DROP TABLE IF EXISTS {keyspace}.prospect_sequence;"
    ).format(keyspace=keyspace))

    session.execute((
        "CREATE TABLE IF NOT EXISTS {keyspace}.client_data (client_id INT PRIMARY KEY, "
        "first_name TEXT, "
        "last_name TEXT, "
        "job_title TEXT, "
        "email TEXT, "
        "company_name TEXT, "
        "overview TEXT, "
        "phone_number TEXT);"
    ).format(keyspace=keyspace))

    print("Client_Data Table Created.")

    session.execute((
        "CREATE TABLE IF NOT EXISTS {keyspace}.client_identity ("
        "client_id INT, "
        "campaign_id TEXT, "
        "campaign_type INT, "
        "prospect_ids LIST<INT>, "
        "context_email_ids LIST<INT>, "
        "formality TEXT, "
        "flattery TEXT, "
        "style TEXT, "
        "hook TEXT, "
        "CTA TEXT, "
        "greeting TEXT, "
        "sign_off TEXT, "
        "language TEXT, "
        "temperature FLOAT, "
        "PRIMARY KEY (client_id, campaign_id) );"
    ).format(keyspace=keyspace))

    print("Client_Identity Table Created.")

    session.execute((
        "CREATE TABLE IF NOT EXISTS {keyspace}.prospect_sequence ("
        "prospect_id INT PRIMARY KEY, "
        "email_one UUID, "
        "email_two UUID, "
        "email_three UUID, "
        "email_four UUID, "
        "reply TEXT, "
        "linkedin_connection_request UUID, "
        "accepted BOOLEAN, "
        "linkedin_one UUID, "
        "linkedin_two UUID, "
        "linkedin_three UUID, "
        "linkedin_four UUID, "
        "linkedin_reply TEXT); "
    ).format(keyspace=keyspace))

    print("Prospect_Sequence Table Created.")


def addDataToTable():
    text_blocks = [
        (1,	"Helen", "Soden", "CEO", "helen@wearehullabaloo.com", "Hullabaloo", "Hullabaloo is a dynamic storytelling agency dedicated to helping brands connect with young audiences by leveraging engaging, narrative-driven content across various media platforms. Founded by three experienced content creators, Hullabaloo pursues both critical and commercial success, enhancing audience growth and interaction through innovative storytelling. The agency specialises in content appealing to children and families, collaborating with established brands like Disney, Apple, and Netflix to craft compelling narratives. With a talented team including industry veterans such as Helen Soden, Matt René, and Jack Jameson, Hullabaloo consistently delivers warmth, humour, and integrity in its productions. Their expertise extends to devising social media strategies for high-profile personalities, underlining their adaptability in an ever-evolving marketplace. Hullabaloo encourages potential clients to initiate partnerships via their contact form, bolstering their social media presence on platforms such as LinkedIn and Instagram. Their services are meticulously tailored to amplify brand narratives and forge meaningful connections with youthful demographics worldwide.", "7734346619"),
        (2,	"Aidan", "Lethem", "CEO", "aidan.lethem@cocubed.com", "CoCubed", "Co:cubed partners with corporate leaders to accelerate innovation by connecting them to a global network of 12 million startups. They help corporates build and execute startup collaboration programmes, aiming to drive impactful and scalable solutions to significant challenges. Co:cubed's offerings include upfront strategic consulting, event-based engagements, curated startup access, and a white-labelled online platform for collaboration and workflow management. Their unique Co:Create process transforms ideas into in-market pilots within three months, fostering a future of more collaborative, innovative, and sustainable corporate operations. Trusted by Fortune 200 companies, Co:cubed is dedicated to reshaping corporate innovation landscapes.", "7735527191"),
    ]

    for block in text_blocks:
        client_id, first_name, last_name, job_title, email, company_name, overview, phone_number = block
        session.execute(
            f"INSERT INTO {keyspace}.client_data (client_id, first_name, last_name, job_title, email, company_name, overview, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (client_id, first_name, last_name, job_title, email, company_name, overview, phone_number)
        )

def addClientToDB(client_info, campaign_id):
    client_id, first_name, last_name, job_title, email, company_name, overview, phone_number = client_info
    session.execute(
            f"INSERT INTO {keyspace}.client_data (client_id, first_name, last_name, job_title, email, company_name, overview, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (client_id, first_name, last_name, job_title, email, company_name, overview, phone_number)
        )
    
    campaign_type, prospect_ids, context_email_ids, formality, flattery, style, hook, CTA, greeting, sign_off, language, temperature = default_client_style
    session.execute(
            f"INSERT INTO {keyspace}.client_identity (client_id, campaign_id, campaign_type, prospect_ids, context_email_ids, formality, flattery, style, hook, CTA, greeting, sign_off, language, temperature) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (client_id, campaign_id, campaign_type, prospect_ids, context_email_ids, formality, flattery, style, hook, CTA, greeting, sign_off, language, temperature)
        )

def findDataFromTable(client_id):
    query = (f"SELECT * FROM {keyspace}.client_data WHERE client_id = {client_id};")

    for row in session.execute(query):
        print(f"Client Found: {row}")

def searchClientData(query_parameters):
    query = (f"SELECT * FROM {keyspace}.client_data WHERE {query_parameters[0]} = {query_parameters[1]};")
    result = []
    for row in session.execute(query):
        result.append(row)
    return(result)

def searchClientIdentity(query_parameters):
    query = (f"SELECT * FROM {keyspace}.client_identity WHERE {query_parameters[0]} = {query_parameters[1]};")
    result = []
    for row in session.execute(query):
        result.append(row)
    return(result)

def searchProspectSequence(query_parameters):
    query = (f"SELECT * FROM {keyspace}.prospect_sequence WHERE {query_parameters[0]} = {query_parameters[1]};")
    result = []
    for row in session.execute(query):
        result.append(row)
    return(result)

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

def connectToVectorDB():
    # Initialize the client
    client = DataAPIClient("AstraCS:XEoqcammeNWBnzGrtsvrQNoZ:915b924d73ef9ff809c52836077fdb964884133f50aff352b27e026999a8afa5")
    db = client.get_database_by_api_endpoint(
    "https://fc1dfd40-466b-495a-b5ff-765b49d908d1-us-east-2.apps.astra.datastax.com",
        keyspace="new_keyspace",
    )

        
    print(f"Connected to Astra DB: {db.list_collection_names()}")

# addDataToCollection()
# vectorSearch()
session = connectToNormalDB()
createTablesDB()
#addDataToTable()

connectToVectorDB()

test_client_info = (1,	"Helen", "Soden", "CEO", "helen@wearehullabaloo.com", "Hullabaloo", "Hullabaloo is a dynamic storytelling agency dedicated to helping brands connect with young audiences by leveraging engaging, narrative-driven content across various media platforms. Founded by three experienced content creators, Hullabaloo pursues both critical and commercial success, enhancing audience growth and interaction through innovative storytelling. The agency specialises in content appealing to children and families, collaborating with established brands like Disney, Apple, and Netflix to craft compelling narratives. With a talented team including industry veterans such as Helen Soden, Matt René, and Jack Jameson, Hullabaloo consistently delivers warmth, humour, and integrity in its productions. Their expertise extends to devising social media strategies for high-profile personalities, underlining their adaptability in an ever-evolving marketplace. Hullabaloo encourages potential clients to initiate partnerships via their contact form, bolstering their social media presence on platforms such as LinkedIn and Instagram. Their services are meticulously tailored to amplify brand narratives and forge meaningful connections with youthful demographics worldwide.", "7734346619")
addClientToDB(test_client_info, "ABC")
addClientToDB(test_client_info, "ABCDE")
print(searchClientIdentity(("client_id", 1)))