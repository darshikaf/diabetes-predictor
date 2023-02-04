import os
from pathlib import Path

from setuptools import find_packages, setup

name = "app"
pysrc_dir = "."
packages = [p for p in find_packages(pysrc_dir) if not p.startswith("tests")]
package_dir = {"": pysrc_dir}

# Often, additional files need to be installed into a package. These files are often data that’s closely related to
# the package’s implementation, or text files containing documentation that might be of interest to programmers using
# the package. These files are called package data.
# Source: https://docs.python.org/3/distutils/setupscript.html
package_data = {name: []}

# Only add the version if it exists
version_fname = Path(f"{name}/_version")
if version_fname.exists():
    package_data[name].append("_version")
    with version_fname.open("r") as f:
        version = f.read().strip()
else:
    version = os.getenv("VERSION", "0.0.0")

# The data_files option can be used to specify additional files needed by the module distribution: configuration files,
# message catalogs, data files, anything which doesn’t fit in the previous categories.
# Source: https://docs.python.org/3/distutils/setupscript.html
data_files = [
    "LICENSE",
]

entry_points = {"console_scripts": []}

with open("LICENSE") as f:
    _license = f.read()

setup(
    name=name,
    version=version,
    description="Progression predictions for diabetes records.",
    url="https://github.com/darshikaf/diabetes-predictor",
    author="Darshika Fernando",
    author_email="",
    license=_license,
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    data_files=data_files,
    include_package_data=True,
    zip_safe=False,
)
