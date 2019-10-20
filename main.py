from mlsploit import Job
from PIL import Image
import foolbox
import inspectO
import tensorflow as tf

# Initialize the job, which will
# load and verify all input parameters
Job.initialize()

Job.input_json = {
  "name": "FGSM",
  "options": {
    "label": 0,
    "unpack": false,
    "epsilon": 1.0,
    "stepsize": 1.0,
    "iterations": 10,
    "random_start": true,
    "return_early": false
  },
  "num_files": 1,
  "files": ["example.jpg"],
  "tags": [{}]
}

Job.function = "FGSM"

Job.options = {
    "label": 0,
    "unpack": false,
    "epsilon": 1.0,
    "stepsize": 1.0,
    "iterations": 10,
    "random_start": true,
    "return_early": false
}

Job.input_files = ["/mnt/input/example.jpg"]

input_file_path = Job.input_files[0] # /mnt/input/image123.jpg
image = Image.open(input_file_path)


for name, item in inspect.getmembers(foolbox.attacks):
    if name == Job.function:
        print (name)
        # perform attack here
        #attack = attack_class(**Job.options)
        #attack = ADefAttack(max_iter=100, max_norm=np.inf, smooth=1.0, sumsample=10)
        attacked_image = attack.attack(image)
        attack  = foolbox.attacks.ADefAttack(item)
        label = "hello"
        adversarial = attack(image, label)

        output_image_filename = os.path.basename(input_file_path) # "image123.jpg"
        output_file_path = Job.make_output_filepath(output_image_filename) # /mnt/output/image123.jpg
        save(attacked_image, output_file_path)
        Job.add_output_file(
            output_file_path, tags=None,
            is_modified=True, is_extra=False)

        Job.commit_output()
    else:
        continue
