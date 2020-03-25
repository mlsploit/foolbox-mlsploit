import os

import numpy as np
from PIL import Image
import foolbox
import inspect

from mlsploit_local import Job

from data import build_image_dataset, get_or_create_dataset, recreate_image
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

    attack_name = Job.function
    attack_options = dict(Job.options)

    fmodel = get_fmodel(attack_options)

    input_file_paths = list(map(lambda f: f.path, Job.input_files))
    input_dataset, is_temp_dataset = get_or_create_dataset(input_file_paths)

    output_dataset = build_image_dataset(
        Job.make_output_filepath(input_dataset.path.name)
    )

    original_predictions = dict()
    for item in input_dataset:
        original_predictions[item.name] = np.argmax(fmodel.predictions(item.data))

        print(
            "Original prediction for %s: %s"
            % (item.name, get_label_for_imagenet_class(original_predictions[item.name]))
        )

    if attack_name == "Classify":
        for item in input_dataset:
            output_dataset.add_item(
                name=item.name,
                data=item.data,
                label=item.label,
                prediction=original_predictions[item.name],
            )

    else:
        attack_class = ATTACK_CLASSES[attack_name]
        attack = attack_class(fmodel)

        for item in input_dataset:
            adversarial_image = attack(
                item.data, original_predictions[item.name], **attack_options
            )

            attack_prediction = np.argmax(fmodel.predictions(adversarial_image))

            output_dataset.add_item(
                name=item.name,
                data=adversarial_image,
                label=item.label,
                prediction=attack_prediction,
            )

            print(
                "Prediction after attack for %s: %s"
                % (item.name, get_label_for_imagenet_class(attack_prediction))
            )

    output_item = output_dataset[0]
    output_image = recreate_image(output_item.data)
    output_image_label = get_label_for_imagenet_class(output_item.prediction)
    output_image_path = Job.make_output_filepath(output_item.name)
    output_image.save(output_image_path)

    Job.add_output_file(str(output_dataset.path), is_extra=True)
    Job.add_output_file(
        output_image_path,
        is_modified=True,
        tags={"label": output_image_label, "mlsploit-visualize": "image"},
    )

    Job.commit_output()

    if is_temp_dataset:
        os.remove(input_dataset.path)


if __name__ == "__main__":
    main()
