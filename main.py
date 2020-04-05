import os

import numpy as np
from PIL import Image
import foolbox
import inspect

from mlsploit import Job
from mlsploit.dataset.datasets import ImageClassificationDatasetWithPrediction

from data import get_or_create_dataset, recreate_image
from models import CUSTOM_MODEL, load_foolbox_zoo_model, load_pretrained_model
from utils.imagenet import get_label_for_imagenet_class


ATTACK_CLASSES = {
    name: attack_class for name, attack_class in inspect.getmembers(foolbox.attacks)
}


def get_fmodel(attack_options):
    model_name = attack_options.pop("model")
    custom_model_url = attack_options.pop("custom_model_url", None)

    if model_name == CUSTOM_MODEL:
        return load_foolbox_zoo_model(custom_model_url)

    model = load_pretrained_model(model_name).eval()
    mean = np.array([0.485, 0.456, 0.406]).reshape((3, 1, 1))
    std = np.array([0.229, 0.224, 0.225]).reshape((3, 1, 1))
    return foolbox.models.PyTorchModel(
        model, bounds=(0, 1), num_classes=1000, preprocessing=(mean, std)
    )


def main():
    # Initialize the job, which will
    # load and verify all input parameters
    Job.initialize()

    fn_name = Job.function_name
    fn_options = Job.options._asdict()

    fmodel = get_fmodel(fn_options)

    input_file_paths = list(map(lambda f: f.path, Job.input_file_items))
    input_dataset, is_temp_dataset = get_or_create_dataset(input_file_paths)

    output_dataset_file_item = Job.reserve_output_file_item(
        input_dataset.path.name, is_new_file=True
    )
    output_dataset = ImageClassificationDatasetWithPrediction.initialize(
        output_dataset_file_item.path, module="foolbox"
    )

    original_predictions = dict()
    for item in input_dataset:
        image = np.array(item.image, dtype=np.float32)
        original_predictions[item.filename] = np.argmax(fmodel.predictions(image))

        print(
            "Original prediction for %s: %s"
            % (
                item.filename,
                get_label_for_imagenet_class(original_predictions[item.filename]),
            )
        )

    if fn_name == "Classify":
        for item in input_dataset:
            output_dataset.add_item(
                filename=item.filename,
                image=item.image,
                label=item.label,
                prediction=original_predictions[item.filename],
            )

    else:
        attack_class = ATTACK_CLASSES[fn_name]
        attack = attack_class(fmodel)

        for item in input_dataset:
            image = np.array(item.image, dtype=np.float32)
            adversarial_image = attack(
                image, original_predictions[item.filename], **fn_options
            )

            attack_prediction = np.argmax(fmodel.predictions(adversarial_image))

            output_dataset.add_item(
                filename=item.filename,
                image=adversarial_image,
                label=item.label,
                prediction=attack_prediction,
            )

            print(
                "Prediction after attack for %s: %s"
                % (item.filename, get_label_for_imagenet_class(attack_prediction))
            )

    output_item = output_dataset[0]
    output_image = recreate_image(output_item.image)
    output_image_label = get_label_for_imagenet_class(output_item.prediction)

    output_image_file_item = Job.reserve_output_file_item(
        output_item.filename, is_modified_file=True,
    )
    output_image.save(output_image_file_item.path)
    output_image_file_item.add_tag(name="visualize", value="image")
    output_image_file_item.add_tag(name="label", value=output_image_label)

    Job.commit_output()

    if is_temp_dataset:
        os.remove(input_dataset.path)


if __name__ == "__main__":
    main()
