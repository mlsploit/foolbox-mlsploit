from pathlib import Path
from tempfile import mkdtemp
from typing import Iterable, Tuple

import numpy as np
from PIL import Image

from mlsploit.dataset.datasets import ImageClassificationDataset
from mlsploit.paths import FilepathType


IMG_WIDTH = 224
IMG_HEIGHT = 224
IMG_DTYPE = np.double


def process_image(image: Image) -> np.ndarray:
    image = image.resize((IMG_WIDTH, IMG_HEIGHT))
    image = np.array(image, dtype=IMG_DTYPE)
    image = image.transpose([2, 0, 1])
    image = image / 255.0
    return image


def load_and_process_image(image_path: FilepathType) -> np.ndarray:
    image = Image.open(image_path)
    image = process_image(image)
    return image


def recreate_image(data: np.ndarray) -> Image:
    image = np.uint8(data * 255.0)
    image = image.transpose([1, 2, 0])
    image = Image.fromarray(image)
    return image


def get_or_create_dataset(
    input_file_paths: Iterable[FilepathType],
) -> Tuple[ImageClassificationDataset, bool]:

    dataset_filename = ImageClassificationDataset.recommended_filename

    # return dataset if found in given input files
    for input_file_path in map(Path, input_file_paths):
        if input_file_path.name == dataset_filename:
            return ImageClassificationDataset(input_file_path), False

    # no dataset found, create a new dataset which contains the given input files
    dataset = ImageClassificationDataset.initialize(
        Path(mkdtemp(prefix="foolbox-")) / dataset_filename, module="foolbox",
    )

    for input_file_path in map(Path, input_file_paths):
        image = load_and_process_image(input_file_path)
        dataset.add_item(filename=input_file_path.name, image=image, label=-1)

    return dataset, True
