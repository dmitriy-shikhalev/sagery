# sagery
- create new migration: ```alembic revision --autogenerate -m "Init migration"```
- apply new migration: ```alembic upgrade head```
- run server: ```hypercorn sagery.api.main:app --bind 127.0.0.1:8090 --reload --debug```