# APACHE SUPERSET

### 1. Start the server

`docker run -d -p 8080:8088 -e "SUPERSET_SECRET_KEY=your_secret_key_here" --name superset apache/superset`

Example:\
`docker run -d -p 8080:8088 -e "SUPERSET_SECRET_KEY=superset" --name superset apache/superset:91301bc-dev`

### 2. Create a user

This will create a new admin user

```
docker exec -it superset superset fab create-admin \
--username admin \
--firstname Superset \
--lastname Admin \
--email admin@superset.com \
--password admin
```

### 3. Migrate Local DB to latest

`docker exec -it superset superset db upgrade`

### 4. Load Examples

`docker exec -it superset superset load_examples`

### 5. Setup roles

`docker exec -it superset superset init`

# KAFKA

### 1. Create a topic

```
kafka-topics.sh --create \
--bootstrap-server 192.168.33.10:9092 \
--replication-factor 1 \
--partitions 3 \
--topic place_bet
```
