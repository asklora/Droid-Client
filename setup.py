import setuptools
from setuptools import find_packages

# Load the README and requirements
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open('requirements.txt', "r", encoding="utf-8") as f:
    required = f.read().splitlines()

setuptools.setup(
    name = 'LoraDroidClient',
    version = '0.1.0',
    description = 'Python client for connecting to LORA Technologies\' bot services.',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    url = 'asklora.ai',
    install_requires=required,
    author = 'LORA Tech',
    author_email = 'asklora@loratechai.com',
    package_dir = {
            '': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    zip_safe = False
)
