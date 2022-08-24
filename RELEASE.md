# Semantic Releases 

PyPrql uses python semantic-release to automate the release process ( https://python-semantic-release.readthedocs.io/en/latest/)

To trigger a release, in the commit message add the terms `fix: `, `perf: `, or `feat: `. 

The version number will get updated automatically there is no need to update them ( in pyproject.toml and pyprql/__init__.py ) manually.

You might need to disable the main branch protection on prql/PyPrql , it seems to not respsect the user bypass.
