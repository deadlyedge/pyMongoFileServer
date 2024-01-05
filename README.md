## purpose

this project is sort of review, for my coding skills, just for fun.

this repo require a working mongodb uri to run, set it in enviroment.

I throught it may useful when someone have a vps and want to add a bit more
workload to it, and may make some test work easier.

I choose mongodb with gridFS support, because I love mongo, and I have had a mongodb running, and it looks less code to write.

## tech stacks

 - python
 - mongodb
 - react
 - fastapi

## enviroments

variable start with VITE_ is required by vitejs, it means from frontend for me,
so just keep them same as for backend.

 - XD_API_KEY: {some key}
 - VITE_XD_API_KEY: {same key}
 - BASE_URL: {production url} # not necessary
 - VITE_BASE_URL: {same url}
 - MONGO_URI: {working database}

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
 - port to nextjs

## note
