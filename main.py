import os

from mlsploit import Job
import numpy as np
from PIL import Image
import foolbox
import inspect

from models import load_pretrained_model
from utils.imagenet import get_label_for_imagenet_class

# Initialize the job, which will
# load and verify all input parameters
Job.initialize()

attack_name = Job.function
attack_options = dict(Job.options)

model_name = attack_options.pop('model')
model = load_pretrained_model(model_name).eval()

input_file_paths = list(map(lambda f: f.path, Job.input_files))
input_file_path = input_file_paths[0]
input_file_name = os.path.basename(input_file_path)

mean = np.array([0.485, 0.456, 0.406]).reshape((3, 1, 1))
std = np.array([0.229, 0.224, 0.225]).reshape((3, 1, 1))
fmodel = foolbox.models.PyTorchModel(
  model,
  bounds=(0, 1),
  num_classes=1000,
  preprocessing=(mean, std))

image_size = 224
original_image = Image.open(input_file_path)
image = original_image.resize((image_size, image_size))
image = np.array(image, dtype=np.float32)
image = image.transpose([2, 0, 1])
image = image / 255.

label = np.argmax(fmodel.predictions(image))
print('Original prediction:', get_label_for_imagenet_class(label))

if attack_name == 'classify':
    output_image = original_image
    output_file_path = Job.make_output_filepath(input_file_name)
    output_image.save(output_file_path)
    Job.add_output_file(
        output_file_path,
        tags={
        'label': label,
        'mlsploit-visualize': 'image'})
    Job.commit_output()

else:
    for name, item in inspect.getmembers(foolbox.attacks):
        if name == Job.function:
            attack_init = item
            attack = attack_init(fmodel)
            adversarial = attack(image, label, **attack_options)

            label_attack = np.argmax(fmodel.predictions(adversarial))
            label_attack = get_label_for_imagenet_class(label_attack)
            print('Prediction after attack:', label_attack)

            output_image = np.uint8(adversarial * 255.)
            output_image = output_image.transpose([1, 2, 0])
            output_image = Image.fromarray(output_image)

            output_file_path = Job.make_output_filepath(input_file_name)
            output_image.save(output_file_path)
            Job.add_output_file(
            output_file_path, is_modified=True,
            tags={
                'label': label_attack,
                'mlsploit-visualize': 'image'})
            Job.commit_output()

        else:
            continue
