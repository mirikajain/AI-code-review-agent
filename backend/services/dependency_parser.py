import os
import xml.etree.ElementTree as ET
import json
import re


DEPENDENCY_FILES = {
    ".csproj",
    ".props",
    ".targets",
    ".config",
    ".json"
}


def parse_dependencies(repo_path, metadata_files):
    """
    Parse dependency-related metadata from a .NET repository.

    Args:
        repo_path: Absolute repository path.
        metadata_files: metadata_files returned by repository_scanner.

    Returns:
        Dictionary containing project metadata.
    """

    result = {
        "frameworks": [],
        "sdk": None,
        "packages": [],
        "project_references": [],
        "nullable": None,
        "implicit_usings": None,
        "lang_version": None,
        "global_json": None,
        "source_dependencies": []
    }

    for file in metadata_files:

        extension = file["extension"]

        if extension == ".csproj":
            parse_csproj(
                os.path.join(repo_path, file["path"]),
                result
            )

        elif file["name"].lower() == "global.json":
            parse_global_json(
                os.path.join(repo_path, file["path"]),
                result
            )
    for root, _, files in os.walk(repo_path):

        for filename in files:

            if filename.endswith(".cs"):

                full_path = os.path.join(root, filename)

                dependency = parse_source_dependencies(
                    repo_path,
                    full_path
                    )

                result["source_dependencies"].append(
                    dependency
                    )

    return result


def parse_csproj(file_path, result):
    """
    Extract information from a .csproj file.
    """

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

    except Exception:
        return

    # SDK

    if "Sdk" in root.attrib:
        result["sdk"] = root.attrib["Sdk"]

    # PropertyGroup

    for prop in root.findall(".//PropertyGroup"):

        framework = prop.find("TargetFramework")

        if framework is not None:
            result["frameworks"].append(framework.text)

        frameworks = prop.find("TargetFrameworks")

        if frameworks is not None:

            result["frameworks"].extend(
                [f.strip() for f in frameworks.text.split(";")]
            )

        nullable = prop.find("Nullable")

        if nullable is not None:
            result["nullable"] = nullable.text

        implicit = prop.find("ImplicitUsings")

        if implicit is not None:
            result["implicit_usings"] = implicit.text

        lang = prop.find("LangVersion")

        if lang is not None:
            result["lang_version"] = lang.text

    # PackageReference

    for package in root.findall(".//PackageReference"):

        result["packages"].append({

            "name": package.attrib.get("Include"),

            "version": package.attrib.get("Version")
        })

    # ProjectReference

    for project in root.findall(".//ProjectReference"):

        result["project_references"].append(
            project.attrib.get("Include")
        )


def parse_global_json(file_path, result):
    """
    Parse global.json SDK information.
    """

    try:

        with open(file_path, "r", encoding="utf-8") as f:

            data = json.load(f)

        result["global_json"] = data

    except Exception:
        pass


def parse_source_dependencies(repo_path, file_path):
    """
    Parse C# source file dependencies.
    """

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

    except Exception:

        return {
            "path": "",
            "imports": []
        }

    imports = re.findall(

        r'using\s+([\w\.]+)\s*;',

        content

    )

    return {

        "path": os.path.relpath(
            file_path,
            repo_path
        ),

        "imports": imports

    }