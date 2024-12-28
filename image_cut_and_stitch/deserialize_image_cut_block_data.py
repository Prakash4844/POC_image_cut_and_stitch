# Author: Prakash Sahu <github.com/prakash4844> <pk484442@gmail.com>

# This file contains code for deserializing the image cut resolution data.

import datetime

def deserialize(data: str, filename) -> list:
    """Deserialize the image cut resolution data."""
    try:
        file_name = filename
        with open(f"/tmp/{file_name}.tree", "a") as file:
            file.write(data)
            file.write("\n")
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error deserializing image cut resolution data: {e}")