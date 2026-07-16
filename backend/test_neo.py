from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687",
    auth=("neo4j", "12345678")
)

with driver.session() as session:
    result = session.run("RETURN 'Neo4j Connected!' AS message")

    for record in result:
        print(record["message"])

driver.close()

from services.neo4j_service import get_repository_graph

graph = get_repository_graph(
     "014329f0-1aeb-4957-9b1b-1db29df4e5e4"
)

print(graph)