# docker-utils-api
A simple API exposing endpoints to run docker commands.


## How to run:
1. Create `.env` following the `.env_example`.
2. Install requirements in a python virtual env.
3. Run application on desired port using a command like this one `uvicorn main:app --port <port_number>`.
4. Access API documentation at `/docs` for example `http://127.0.0.1:8080/docs` if deployed on localhost port 8080.

