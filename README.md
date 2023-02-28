# Simple Blockchain Header Indexer
This simple Flask server maintains an in-memory storage for storing the
block headers downloaded from "https://storage.googleapis.com/psl-careers/blk00000.dat" and serves
the data in json format.
*It only has one endpoint to query the block header data (json) by the block height.

#### Running
```
wget https://storage.googleapis.com/psl-careers/blk00000.dat
export FLASK_APP=main.py
flask run
```

Then query the server from another terminal by providing the block height in the 
query parameters. Example:
```
curl "http://127.0.0.1:5000/?block=8"
```
