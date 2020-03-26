from pathlib import Path
from tempfile import mkdtemp
from typing import Iterable, Tuple

import numpy as np
from PIL import Image

from mlsploit.dataset import Dataset
from mlsploit.paths import FilepathType


IMG_WIDTH = 224
IMG_HEIGHT = 224
IMG_DTYPE = np.float32


def build_image_dataset(dataset_path: FilepathType) -> Dataset:
    img_shape = (3, IMG_HEIGHT, IMG_WIDTH)

    return (
        Dataset.build(dataset_path)
        .with_metadata(
            bounds=[0, 1],
            color_mode="RGB",
            channels_first=True,
            img_width=IMG_WIDTH,
            img_height=IMG_HEIGHT,
            preprocessing=[0, 1],
        )
        .add_item_attr(name="name", shape=None, dtype="str",)
        .add_item_attr(name="data", shape=img_shape, dtype=IMG_DTYPE)
        .add_item_attr(name="label", shape=None, dtype=int)
        .add_item_attr(name="prediction", shape=None, dtype=int)
        .conclude_build()
    )


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
) -> Tuple[Dataset, bool]:

    # return dataset if found in given input files
    for input_file_path in map(Path, input_file_paths):
        if input_file_path.name == Dataset.recommended_filename:
            return Dataset(input_file_path), False

    # no dataset found, create a new dataset which contains the given input files
    dataset = build_image_dataset(
        Path(mkdtemp(prefix="foolbox-")) / Dataset.recommended_filename
    )

    for input_file_path in map(Path, input_file_paths):
        image = load_and_process_image(input_file_path)
        dataset.add_item(name=input_file_path.name, data=image, label=-1, prediction=-1)

    return dataset, True
