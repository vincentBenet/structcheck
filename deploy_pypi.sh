poetry version patch
git add .
git commit -m "new version"
git push
poetry publish --build
pip uninstall structcheck
pip install structcheck
