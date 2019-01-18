import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.readlines()

setuptools.setup(
    name="acquantum_connector",
    version="0.0.1",
    author="Carsten Blank",
    author_email="blank@data-cybernetics.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carstenblank/acquantum-connector",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3 :: Only',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
