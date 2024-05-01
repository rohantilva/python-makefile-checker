# python-makefile-checker
Verify that scripts in your project's makefile actually exist. Use from within your GitHub actions workflow file or from python code itself!

## Context
During a development cycle, it's common for files to be renamed during the end-to-end development of a pull request
or project. Batch jobs that run make targets in python projects must have these files present in a filesystem to run
successfully, and so renames / edits to python scripts that aren't reflected in the Makefile can have unintended
consequences. It would be great to catch these errors early, before a PR is merged.

## What it does
This python project publishes a script that one can use to verify that scripts listed in a Makefile actually exist
within a filesystem. Since this utility is a script, it can be called from github actions itself, or from within
python code itself.

## How to use

If using in a Github Actions workflow file, you can follow these steps below.

### First install the package
```
pip install makefile-checker
```

## Add the following step to your workflow file:

```
  - name: Check Makefile(s)
    shell: bash
    working-directory: <your working directory>
    run: |
      poetry run check-makefile
```