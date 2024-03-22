# cis4301-project

### Requirements
* Angular CLI
* Python 3.10 or newer
* Docker Desktop
* All library requirements are present in included in the *backend/requirements.txt* file. Instructions on how to download these included in the Setup section.

### Setup
**NOTE:** If you have multiple versions of Python installed, you may have to change the given commands slightly to specify your version. *pip3.x* and *py -3.x* should work as alternatives to *pip* and *python* aliases.

1. Install Python 3.10 or newer
2. Install Angular [here](https://angular.io/guide/setup-local)
3. Pull down the most recent version of this repository to a local location.
4. Setup environment (create .env and virtual environment):
    ```
    cd [repository]
    ./setup.sh
    ./run.sh
    ```

NOTE: if on Windows, shell scripts should be run in Git Bash to ensure compatibility.

### Running CompoDoc Documentation
This project utilizes CompoDoc to automatically generate documentation for the Angular web application. To run this documentation
either use the *run_docs.sh* script or use the following commands:
```
cd [repository]/frontend
npm run compodoc:serve-and-build
```

### Helpful Links/Docs
* [Pydantic Dev Docs](https://docs.pydantic.dev/latest/) - Docs for Pydantic, the tool we use for backend validation and transformation

* [Angular DevTools](https://angular.dev/tools/devtools) - This is a useful browser extension for debugging angular applications.

### Other Tips
* FastAPI endpoints can quickly be tested locally without requiring the front-end by either visiting localhost:8000/docs or with the use of third-party tools such as [Postman](https://www.postman.com/).