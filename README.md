# sagery
- create new migration: ```alembic revision --autogenerate -m "Init migration"```
- apply new migration: ```alembic upgrade head```
- run server: ```hypercorn sagery.api.main:app --bind 127.0.0.1:8090 --reload --debug```

## Need for all new migrations at the beginning:
```python
op.execute('DROP TYPE IF EXISTS Status')
op.execute('DROP TYPE IF EXISTS ObjectStatus')
op.execute('DROP TYPE IF EXISTS VarStatus')
```

## Downgrade to previous migration:
```shell
alembic downgrade -1
```

## Upgrade to last migration:
```shell
alembic downgrade head
```

## Create new migration
```shell
alembic revision --autogenerate
```


## Run debug web:
```shell
uvicorn sagery.api:app --reload
```
