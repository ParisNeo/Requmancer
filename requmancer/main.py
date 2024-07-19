"""
Requmancer: Summon Your Project's Dependencies

Requmancer is a powerful Python library and command-line tool that analyzes your
Python project and generates a comprehensive requirements file. It automatically
detects imported packages, determines their versions, and creates either a
pip-compatible requirements.txt or a Poetry-style pyproject.toml section.

With Requmancer, managing your project's dependencies becomes a breeze, ensuring
reproducibility and easier setup for other developers.

Author: ParisNeo
License: Apache 2.0
Version: 0.1.0
"""

import os
import ast
import sys
import argparse
import pkg_resources
import logging
from typing import Set, Dict, Optional, List

class RequirementsGenerator:
    """
    A class to generate requirements files from Python projects.

    This class analyzes a Python project directory, identifies third-party
    imports, determines their versions, and generates a requirements file
    in either pip or Poetry format.
    """

    def __init__(self, directory: str, output_file: str = 'requirements.txt', format: str = 'pip'):
        """
        Initialize the RequirementsGenerator.

        Args:
            directory (str): Path to the project directory.
            output_file (str, optional): Name of the output file. Defaults to 'requirements.txt'.
            format (str, optional): Output format ('pip' or 'poetry'). Defaults to 'pip'.
        """
        self.directory: str = directory
        self.output_file: str = output_file
        self.format: str = format
        self.imports: Set[str] = set()
        self.versions: Dict[str, str] = {}
        self.std_lib: Set[str] = set(sys.stdlib_module_names)

        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    def find_imports(self, file_path: str) -> Set[str]:
        """
        Find all imports in a Python file.

        Args:
            file_path (str): Path to the Python file.

        Returns:
            Set[str]: Set of imported module names.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                tree = ast.parse(file.read())
            except SyntaxError:
                logging.warning(f"Couldn't parse {file_path} due to syntax error")
                return set()
        
        imports: Set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0:  # Absolute import
                    imports.add(node.module.split('.')[0])
        
        return imports - self.std_lib  # Remove standard library modules

    def get_project_imports(self) -> None:
        """
        Scan the project directory and collect all imports.
        """
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self.imports.update(self.find_imports(file_path))

    def get_package_versions(self) -> None:
        """
        Determine the installed versions of the imported packages.
        """
        for package in self.imports:
            try:
                self.versions[package] = pkg_resources.get_distribution(package).version
            except pkg_resources.DistributionNotFound:
                logging.warning(f"Couldn't find version for {package}")
                self.versions[package] = 'Unknown'

    def write_requirements_file(self) -> None:
        """
        Write the requirements to a file in the specified format.
        """
        with open(self.output_file, 'w') as f:
            if self.format == 'pip':
                for package, version in self.versions.items():
                    if version != 'Unknown':
                        f.write(f"{package}=={version}\n")
                    else:
                        f.write(f"{package}\n")
            elif self.format == 'poetry':
                f.write("[tool.poetry.dependencies]\n")
                f.write('python = "^3.6"\n')
                for package, version in self.versions.items():
                    if version != 'Unknown':
                        f.write(f'{package} = "^{version}"\n')
                    else:
                        f.write(f'{package} = "*"\n')
            else:
                raise ValueError("Unsupported format. Choose 'pip' or 'poetry'.")

    def generate(self) -> None:
        """
        Generate the requirements file by running the entire workflow.
        """
        try:
            self.get_project_imports()
            self.get_package_versions()
            self.write_requirements_file()
            logging.info(f"Requirements file created: {self.output_file}")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

def main() -> None:
    """
    Main function to handle command-line usage of Requmancer.
    """
    parser = argparse.ArgumentParser(description="Generate requirements file from Python project")
    parser.add_argument("directory", help="Path to the project directory")
    parser.add_argument("-o", "--output", default="requirements.txt", help="Output file name")
    parser.add_argument("-f", "--format", choices=['pip', 'poetry'], default='pip', help="Output format")
    args = parser.parse_args()

    generator = RequirementsGenerator(args.directory, args.output, args.format)
    generator.generate()

if __name__ == "__main__":
    main()