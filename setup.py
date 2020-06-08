import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read().split('\n')[1]

setuptools.setup(
    name="intake-sql-adapter", # Replace with your own username
    version="0.0.1",
    author="Austin Weir",
    author_email="noreply@noreply.com",
    description=long_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aweir12/intake-sql-adapter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)