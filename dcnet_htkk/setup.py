from setuptools import setup, find_packages

setup(
    name="dcnet_htkk",
    version="0.0.1",
    description="Automatic Tax Declaration (HTKK) for ERPNext Vietnam",
    author="DCNET",
    author_email="dev@dcnet.vn",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
)
