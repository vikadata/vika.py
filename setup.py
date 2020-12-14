import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vika",
    version="0.0.9",
    author="vikadata",
    author_email="dev@vikadata.com",
    description="维格表官方 Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vikadata/vika.py",
    packages=["vika"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["requests", "pydantic", "environs"],
)
