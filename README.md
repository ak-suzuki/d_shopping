# prod

## 環境立ち上げ後の"role "postgres" does not exist" について

### dbコンテナに接続

```
docker exec -it Postgresdb bash
```

### postgresに接続

```
psql -U postgres-prod
```

### postgresにロールを追加

```
CREATE ROLE postgres WITH LOGIN PASSWORD '[.envのPOSTGRES_PASSWORD]';
```

### ロールが追加されたか確認

```
\du
```

## django admin create superuser

- docker compose up された状態でアプリケーションの中に入る

```
$ docker exec -it app /bin/bash
```

```
$ python manage.py createsuperuser
Username (leave blank to use 'xxx'): admin
    Email address: xxx@xxx
    Password:
    Password (again):
    Superuser created successfully.
```

- http://127.0.0.1/admin/ でログイン
