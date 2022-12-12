poetry version patch
git add .
git commit -m "new version"
git push
poetry publish --build
pip uninstall -y structcheck
pip install structcheck


# poetry config http-basic.foo <username> <password>
# poetry config pypi-token.pypi my-token