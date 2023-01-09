import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setuptools.setup(
        name="SMNCopyNumberCaller",
        version="0.0.0.1",
        author="ILMN",
        author_email="na@na.gov",
        description="Just making this installable via conda",
        long_description="see description",
        long_description_content_type="text/markdown",
        url="thub.com/iamh2o/SMNCopyNumberCaller",
        project_urls={
            "Bug Tracker": "https://github.com/iamh2o/SMNCopyNumberCaller",
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: PolyForm Strict License 1.0.0",
            "Operating System :: OS Independent",
        ],
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
        scripts=[
            "bin/smn_caller.py",
	    "bin/smn_charts.py"
        ],
        python_requires=">=3.7",
        install_requires=[
            "reportlab",
            "numpy >=1.16",
            "scipy >=1.2",
            "pysam >=0.15.3",
            "statsmodels >=0.9",
        ],
    )
    
