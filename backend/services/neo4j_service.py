from neo4j import GraphDatabase

from config import (
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD
)


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def close_driver():
    driver.close()


def execute_query(query, parameters=None):
    """
    Execute a Cypher query.
    """

    with driver.session() as session:
        session.run(query, parameters or {})


def create_repository(repo_id):
    """
    Create repository node.
    """

    query = """
    MERGE (r:Repository {id:$repo_id})
    """

    execute_query(query, {
        "repo_id": repo_id
    })


def create_file(repo_id, parsed_file):
    """
    Create file node.
    """

    query = """
    MATCH (r:Repository {id:$repo_id})

    MERGE (f:File {
        path:$path
    })

    SET
        f.name=$name,
        f.namespace=$namespace

    MERGE (r)-[:CONTAINS]->(f)
    """

    execute_query(query, {

        "repo_id": repo_id,

        "path": parsed_file["path"],

        "name": parsed_file["name"],

        "namespace": parsed_file["namespace"]
    })


def create_class(file_path, class_name):
    """
    Create class node.
    """

    query = """
    MATCH (f:File {path:$file})

    MERGE (c:Class {
        name:$class
    })

    MERGE (f)-[:CONTAINS]->(c)
    """

    execute_query(query, {

        "file": file_path,

        "class": class_name
    })


def create_interface(file_path, interface_name):
    """
    Create interface node.
    """

    query = """
    MATCH (f:File {path:$file})

    MERGE (i:Interface {
        name:$interface
    })

    MERGE (f)-[:CONTAINS]->(i)
    """

    execute_query(query, {

        "file": file_path,

        "interface": interface_name
    })


def create_method(file_path, method_name):
    """
    Create method node.
    """

    query = """
    MATCH (f:File {path:$file})

    MERGE (m:Method {
        name:$method
    })

    MERGE (f)-[:CONTAINS]->(m)
    """

    execute_query(query, {

        "file": file_path,

        "method": method_name
    })

def create_inheritance(child, parent):
    """
    Create inheritance relationship.
    """

    query = """
    MERGE (c:Class {name:$child})
    MERGE (p:Class {name:$parent})

    MERGE (c)-[:INHERITS]->(p)
    """

    execute_query(
        query,
        {
            "child": child,
            "parent": parent
        }
    )

def create_interface_implementation(class_name, interface_name):
    """
    Create implementation relationship.
    """

    query = """
    MERGE (c:Class {name:$class})
    MERGE (i:Interface {name:$interface})

    MERGE (c)-[:IMPLEMENTS]->(i)
    """

    execute_query(
        query,
        {
            "class": class_name,
            "interface": interface_name
        }
    )

def create_class_dependency(class_name, dependency):
    """
    Create dependency relationship.
    """

    query = """
    MERGE (c1:Class {name:$class})
    MERGE (c2:Class {name:$dependency})

    MERGE (c1)-[:DEPENDS_ON]->(c2)
    """

    execute_query(
        query,
        {
            "class": class_name,
            "dependency": dependency
        }
    )

def create_library(name):
    """
    Create a library/package node.
    """

    query = """
    MERGE (l:Library {
        name:$name
    })
    """

    execute_query(query, {

        "name": name

    })

def create_project(repo_id, project_name):
    """
    Create a project node.
    """

    query = """
    MATCH (r:Repository {id:$repo_id})

    MERGE (p:Project {
        name:$project
    })

    MERGE (r)-[:CONTAINS]->(p)
    """

    execute_query(query, {

        "repo_id": repo_id,

        "project": project_name

    })

def create_library_dependency(file_path, library_name):
    """
    Connect File -> Library.
    """

    query = """
    MATCH (f:File {path:$file})

    MERGE (l:Library {
        name:$library
    })

    MERGE (f)-[:USES]->(l)
    """

    execute_query(query, {

        "file": file_path,

        "library": library_name

    })

def create_project_dependency(project_name, reference):
    """
    Connect Project -> Project.
    """

    query = """
    MERGE (p1:Project {
        name:$project
    })

    MERGE (p2:Project {
        name:$reference
    })

    MERGE (p1)-[:DEPENDS_ON]->(p2)
    """

    execute_query(query, {

        "project": project_name,

        "reference": reference

    })

def store_repository_graph(repo_id, parsed_files):
    """
    Store complete repository graph.
    """

    create_repository(repo_id)

    for parsed_file in parsed_files:

        create_file(repo_id, parsed_file)

        for cls in parsed_file["classes"]:
            create_class(
                parsed_file["path"],
                cls
            )

        for interface in parsed_file["interfaces"]:
            create_interface(
                parsed_file["path"],
                interface
            )

        for method in parsed_file["methods"]:
            create_method(
                parsed_file["path"],
                method
            )


def create_issue(
    file_path,
    rule,
    severity,
    description,
    recommendation,
    owasp=""
):
    """
    Store issue found by LLM.
    """

    query = """
    MATCH (f:File {path:$file})

    CREATE (i:Issue {

        rule:$rule,

        severity:$severity,

        description:$description,

        recommendation:$recommendation,

        owasp:$owasp

    })

    MERGE (f)-[:HAS_ISSUE]->(i)
    """

    execute_query(query, {

        "file": file_path,

        "rule": rule,

        "severity": severity,

        "description": description,

        "recommendation": recommendation,

        "owasp": owasp
    })


def clear_repository(repo_id):
    """
    Delete an existing repository graph.
    """

    query = """
    MATCH (r:Repository {id:$repo_id})

    OPTIONAL MATCH (r)-[*]->(n)

    DETACH DELETE r,n
    """

    execute_query(query, {

        "repo_id": repo_id
    })


def get_graph_statistics():
    """
    Return graph statistics.
    """

    with driver.session() as session:

        result = session.run("""

        MATCH (n)

        RETURN labels(n)[0] AS label,
               count(*) AS count

        """)

        stats = []

        for record in result:

            stats.append({

                "label": record["label"],

                "count": record["count"]

            })

        return stats
    

def get_repository_graph(repo_id):
    """
    Return repository graph for React Force Graph.
    """

    with driver.session() as session:

        # Get all nodes reachable from repository
        node_result = session.run(
            """
            MATCH (r:Repository {id:$repo_id})
            OPTIONAL MATCH (r)-[*0..]->(n)
            RETURN DISTINCT r,n
            """,
            {"repo_id": repo_id}
        )

        nodes = {}
        links = []

        for record in node_result:

            for node in [record["r"], record["n"]]:

                if node is None:
                    continue

                node_id = str(node.element_id)

                if node_id not in nodes:

                    nodes[node_id] = {
                        "id": node_id,
                        "label":
                            node.get("name")
                            or node.get("path")
                            or node.get("id")
                            or "Node",
                        "type": list(node.labels)[0]
                    }

        # Get all relationships
        rel_result = session.run(
            """
            MATCH (r:Repository {id:$repo_id})
            OPTIONAL MATCH p=(r)-[*1..]->(n)
            UNWIND relationships(p) AS rel
            RETURN DISTINCT rel
            """,
            {"repo_id": repo_id}
        )

        for record in rel_result:

            rel = record["rel"]

            if rel is None:
                continue

            links.append({

                "source": str(rel.start_node.element_id),

                "target": str(rel.end_node.element_id),

                "label": rel.type
            })

        return {
            "nodes": list(nodes.values()),
            "links": links
        }
    
def get_node_details(node_id):
    """
    Return complete information for a node.
    """

    query = """
    MATCH (n)

    WHERE elementId(n)=$node_id

    OPTIONAL MATCH (n)-[r]->(m)

    RETURN
        labels(n) AS labels,
        properties(n) AS props,
        collect({
            relationship:type(r),
            target:labels(m),
            properties:properties(m)
        }) AS children
    """

    with driver.session() as session:

        result = session.run(query, {

            "node_id": node_id

        }).single()

        if result is None:
            return None

        return {

            "type": result["labels"][0],

            "properties": result["props"],

            "children": result["children"]

        }    
    
def store_dependency_graph(repo_id, dependencies):
    """
    Store dependency graph in Neo4j.
    """

    # -----------------------------------
    # Store project nodes
    # -----------------------------------

    project_name = "MainProject"

    create_project(
        repo_id,
        project_name
    )

    # -----------------------------------
    # Project References
    # -----------------------------------

    for reference in dependencies["project_references"]:

        create_project_dependency(
            project_name,
            reference
        )

    # -----------------------------------
    # NuGet Packages
    # -----------------------------------

    for package in dependencies["packages"]:

        create_library(

            package["name"]

        )

    # -----------------------------------
    # Source Dependencies
    # -----------------------------------

    for source in dependencies["source_dependencies"]:

        for library in source["imports"]:

            create_library_dependency(

                source["path"],

                library

            )

def store_class_relationships(parsed_files):
    """
    Store inheritance, interfaces and dependencies.
    """

    for file in parsed_files:

        if not file["classes"]:
            continue

        current_class = file["classes"][0]

        # -----------------------
        # Inheritance / Interfaces
        # -----------------------

        for relation in file["relationships"]:

            for parent in relation["inherits"]:

                create_inheritance(
                    relation["class"],
                    parent
                )

            for interface in relation["implements"]:

                create_interface_implementation(
                    relation["class"],
                    interface
                )

        # -----------------------
        # Object dependencies
        # -----------------------

        for dependency in file["object_dependencies"]:

            create_class_dependency(
                current_class,
                dependency
            )