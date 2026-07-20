import os
import re

from services.file_service import read_file


NAMESPACE_PATTERN = re.compile(r'namespace\s+([\w\.]+)')
CLASS_PATTERN = re.compile(
    r'(?:public|private|internal|protected)?\s*'
    r'(?:abstract\s+|sealed\s+)?'
    r'class\s+(\w+)'
)
INTERFACE_PATTERN = re.compile(
    r'(?:public|internal)?\s*interface\s+(\w+)'
)

METHOD_PATTERN = re.compile(
    r'(?:public|private|protected|internal)\s+'
    r'(?:async\s+)?'
    r'[\w<>\[\],]+\s+'
    r'(\w+)\s*\('
)
# Class inheritance / interface implementation
CLASS_DECLARATION_PATTERN = re.compile(
    r'class\s+(\w+)\s*:\s*([^{]+)'
)

# Object creation
OBJECT_CREATION_PATTERN = re.compile(
    r'new\s+(\w+)\s*\('
)

# Method calls
METHOD_CALL_PATTERN = re.compile(
    r'(\w+)\.(\w+)\s*\('
)

def extract_class_relationships(content):
    """
    Extract inheritance, implemented interfaces,
    object creation and method calls.
    """

    relationships = []

    declarations = CLASS_DECLARATION_PATTERN.findall(content)

    for class_name, inheritance in declarations:

        inherits = []
        implements = []

        parents = [
            item.strip()
            for item in inheritance.split(",")
        ]

        for parent in parents:

            if parent.startswith("I"):
                implements.append(parent)
            else:
                inherits.append(parent)

        relationships.append({

            "class": class_name,

            "inherits": inherits,

            "implements": implements

        })

    object_dependencies = OBJECT_CREATION_PATTERN.findall(content)

    method_calls = METHOD_CALL_PATTERN.findall(content)

    return {

        "relationships": relationships,

        "object_dependencies": object_dependencies,

        "method_calls": method_calls

    }

def parse_repository(repo_path, code_files):
    """
    Parse all C# files inside the repository.
    """

    parsed_files = []

    for file in code_files:

        content = read_file(repo_path, file["path"])

        if not content:
            continue

        parsed_files.append(parse_file(file, content))

    return parsed_files


def parse_file(file_info, content):
    """
    Extract basic information from a C# file.
    """

    namespace = None

    namespace_match = NAMESPACE_PATTERN.search(content)

    if namespace_match:
        namespace = namespace_match.group(1)

    classes = CLASS_PATTERN.findall(content)

    interfaces = INTERFACE_PATTERN.findall(content)

    methods = METHOD_PATTERN.findall(content)
    relationships = extract_class_relationships(content)

    return {

    "name": file_info["name"],

    "path": file_info["path"],

    "namespace": namespace,

    "classes": classes,

    "interfaces": interfaces,

    "methods": methods,

    "relationships": relationships["relationships"],

    "object_dependencies": relationships["object_dependencies"],

    "method_calls": relationships["method_calls"],

    "content": content
}