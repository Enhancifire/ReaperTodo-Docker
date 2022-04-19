import hasher
import uuid

key, salt = hasher.hash("fs144")

print(salt)
print(key)

print(hasher.dehash(key, salt, "fs144"))
