import hashlib
import os

def generate_hash(config, include_init=True):
    if include_init:
        hash_input = "".join(f"{k}={v}" for k, v in sorted(config.items()))
    else:
        hash_input = "".join(f"{k}={v}" for k, v in sorted(config.items()) if not (k == "init"))
    return hashlib.md5(hash_input.encode()).hexdigest()

def has_been_run(hash):
    hash_file = "config_hashes.txt"
    if not os.path.exists(hash_file):
        return False
    with open(hash_file, "r") as file:
        existing_hashes = file.read().split()
    return hash in existing_hashes

def store_hash(hash):
    with open("config_hashes.txt", "a") as file:
        file.write(hash + "\n")