# This file contains all the function required to cut(crop) the images
from os import write

# Author: Prakash Sahu <github.com/prakash4844> <pk484442@gmail.com>

import typer
from PIL import Image
from typing import Tuple
from .deserialize_image_cut_block_data import deserialize
from .serialize_image_cut_block_data import serialize

# Define the 720p resolution threshold
THRESHOLD_RES = (1280, 720)

app = typer.Typer(
    name="Image Cut",
    no_args_is_help=True,
    invoke_without_command=True,
    help="Cut(crop) images.",
    context_settings={"help_option_names": ["-h", "--help"]},
)

def is_above_threshold(res: Tuple[int, int]) -> bool:
    """Check if the resolution is above the 720p threshold."""
    return res[0] > THRESHOLD_RES[0] or res[1] > THRESHOLD_RES[1]

def divide_into_grid(res: Tuple[int, int]) -> Tuple[int, int]:
    """Divide the resolution into a 3x3 grid."""
    width, height = res
    return width // 3, height // 3

def process_image_blocks(image: Image, res: Tuple[int, int], depth: int = 0, filename: str = None) -> None:
    """Recursively process the 3x3 blocks of the image."""
    if depth == 0:
        deserialize(f"{'  ' * depth}Processing resolution: {res}", filename)

    if not is_above_threshold(res):
        deserialize(f"{'  ' * depth}Resolution {res} is within the threshold.", filename)
        return

    block_res = divide_into_grid(res)
    for row in range(3):
        for col in range(3):
            deserialize(f"{'  ' * (depth + 1)}Block ({row + 1}, {col + 1})"
                                           f" with resolution {block_res}", filename)
            process_image_blocks(image, block_res, depth + 1, filename)

@app.command()
def calculate_resolution(image_path: str, threshold: tuple[int, int] = THRESHOLD_RES) -> tuple[int, int]:
    """Calculate and process the resolution of an image."""
    try:
        filename = image_path.split("/")[-1]
        # Open the image
        with Image.open(image_path) as img:
            res = img.size  # (width, height)
            original_res = f"Original resolution: {res}"
            deserialize(original_res, filename)

            # Process the image
            process_image_blocks(img, res, filename=filename)

    # Serialize the image cut resolution data
    #     serialize(filename)

    except Exception as e:
        typer.echo(f"Error processing the image: {e}")
