from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cattle-msa-processor",
    version="0.1.0",
    author="richardcarleliot-sz",
    description="A high-performance toolkit for processing multi-species alignment (MAF) data for genome modeling.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/richardcarleliot-sz/cattle-msa-processor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.20",
        "zarr>=2.10",
        "pandas>=1.3",
        "pyarrow>=5.0",
        "biopython>=1.79",
        "tqdm>=4.62",
    ],
    entry_points={
        "console_scripts": [
            "cattle-msa-processor=cattle_msa_processor.cli:main",
        ],
    },
)