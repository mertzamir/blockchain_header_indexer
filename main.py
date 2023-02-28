import struct
from flask import Flask, jsonify, request


class BlockHeader:
    def __init__(self, version, prev_hash, merkle_hash, time, n_bits, nonce):
        self.version = version
        self.prev_hash = prev_hash
        self.merkle_hash = merkle_hash
        self.time = time
        self.n_bits = n_bits
        self.nonce = nonce

    def json(self):
        return {
            "version": self.version,
            "previous_block_header_hash": self.prev_hash,
            "merkle_root_hash": self.merkle_hash,
            "time": self.time,
            "n_bits": self.n_bits,
            "nonce": self.nonce,
        }


class Storage:
    def __init__(self):
        self.block_map = {}

    def add_block(self, block_height: int, block_header: BlockHeader):
        self.block_map[block_height] = block_header


def parse_file(file_name, storage):
    offset = 0
    block_height = 0
    with open(file_name, "rb") as f:
        byte_chunk = f.read()
        f.seek(0)

        while f.tell() < len(byte_chunk):
            # Set the pointer to the beginning of Size
            f.seek(4, 1)  # 4 forward from the current position

            # Find block size
            block_size = int.from_bytes(f.read(4), byteorder="little")

            # Parse Header and store
            version = hex(int.from_bytes(f.read(4), byteorder="little"))
            prev_hash = hex(int.from_bytes(f.read(32), byteorder="little"))
            merkle_hash = hex(int.from_bytes(f.read(32), byteorder="little"))
            time = hex(int.from_bytes(f.read(4), byteorder="little"))
            n_bits = hex(int.from_bytes(f.read(4), byteorder="little"))
            nonce = hex(int.from_bytes(f.read(4), byteorder="little"))
            storage.add_block(
                block_height,
                BlockHeader(version, prev_hash, merkle_hash, time, n_bits, nonce),
            )

            # Set next offset
            offset = offset + 8 + block_siz
            f.seek(offset)

            block_height += 1


# parse file and init the in-memory storage
storage = Storage()
parse_file("blk00000.dat", storage)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_block():
    args = request.args
    height = args.get("block", default=0, type=int)
    return jsonify(storage.block_map[height].json())
