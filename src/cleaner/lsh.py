import hashlib
from hashlib import 
import os
def get_relevent(folder_path):
    seen_hashes = {}
    duplicate_remoal = 0
    if not os.path.exists(folder_path):
        raise ValueError("file koni")
    
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)

        if os.path.isfile(full_path):

            sha_256 = hashlib.sha256()
            

            with open(full_path, "rb") as f:
                while chr:= f.read(8169):
                    sha_256.update(chr)

                file_hash = sha_256.hexdigest()

                if file_hash in seen_hashes:
                    print(f" Duplicate found {file_name} is identical to {os.path.basename(seen_hashes[seen_hashes])}")

                    os.remove(full_path)
                    duplicate_remoal  += 1
                    print(f"Total duplicate{duplicate_remoal}")

                else:
                    seen_hashes[file_name] = full_path
                    print("Duplicate not found")


            print(f" file name {file_name}")
           
target_folder = "/Users/niteshv1520/NexaSearch/data/raw/markdown"
get_relevent(target_folder)



        

            

        



