## purpose

this project is sort of review, for my coding skills, just for fun.

this repo require a working mongodb uri to run, just set it in enviroment.

## tech stacks

 - python
 - mongodb
 - react
 - fastapi

## enviroments
 - XD_API_KEY: <some key>
 - VITE_XD_API_KEY: <same key>
 - BASE_URL: <production url>
 - VITE_BASE_URL: <same url>
 - MONGO_URI: <working database>

## example docker compose file

```yaml
version: "3.8"

services:

  file_server:
    image: "xdream76/simple-file-server"
    container_name: "file_server"
    restart: unless-stopped
    ports:
      - "8001:8001"
    volumes:
      - /etc/localtime:/etc/localtime:ro
    environment:
      TZ: Asia/Hong_Kong
      XD_API_KEY: XXXXXXXXXX
      VITE_XD_API_KEY: XXXXXXXXXX
      BASE_URL: UUUUUUUUUU.UUU
      VITE_BASE_URL: UUUUUUUUUU.UUU
      MONGO_URI: MMMMMMMMMMM
```


## TODO

 - add download times count
 - add select filters
 - finish delete

## note
