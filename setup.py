'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''
from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]: 
    """
    This function reads a requirements file and returns a list of dependencies.
    It ignores comments and empty lines.
    """
    requirement_lst = []
    try:
        with open("requirements.txt", 'r') as file:
            requirements = file.readlines()
            for line in requirements:
                requirement = line.strip()
                ## Ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)

            
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists in the project directory.")
    
    return requirement_lst

setup(
    name='Network Security',
    version='0.1.0',
    author='Kishlay',
    packages= find_packages(),
    install_requires=get_requirements()
)