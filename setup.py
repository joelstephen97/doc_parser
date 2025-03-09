from setuptools import setup, find_packages

setup(
    name="doc_parser",
    version="0.1.0",
    description="A powerful document parser for resumes and general documents.",
    author="Joel Stephen",
    author_email="jojostev@gmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
