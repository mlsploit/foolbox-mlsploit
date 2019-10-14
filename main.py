from mlsploit import Job
from Pillow import Image

# Initialize the job, which will
# load and verify all input parameters
Job.initialize()

Job.input_json = {
  "name": "ADefAttack",
  "options": {
    "max_iter": 100,
    "max_norm": "inf",
    "smooth": 1.0,
    "sumsample": 10
  },
  "num_files": 1,
  "files": ["example.jpg"],
  "tags": [{}]
}

Job.function = "ADefAttack"

Job.options = {
    "max_iter": 100,
    "max_norm": "inf",
    "smooth": 1.0,
    "sumsample": 10
}

Job.input_files = ["/mnt/input/example.jpg"]

input_file_path = Job.input_files[0] # /mnt/input/image123.jpg
image = Image.open(input_file_path)


for name, item in inspect.getmembers(attacks):
  if (inspect.isclass(item)
      and item is not Attack
      and issubclass(item, Attack)
      and len(item.__abstractmethods__) == 0):
    print(name) # ADefAttack, AdditiveGaussianNoiseAttack ...

    if name == Job.function:
        # perform attack here
        attack_class = item
        #attack = attack_class(**Job.options)
        attack = ADefAttack(max_iter=100, max_norm=np.inf, smooth=1.0, sumsample=10)
        attacked_image = attack.attack(image)

        output_image_filename = os.path.basename(input_file_path) # "image123.jpg"
        output_file_path = Job.make_output_filepath(output_image_filename) # /mnt/output/image123.jpg
        save(attacked_image, output_file_path)
        Job.add_output_file(
            output_file_path, tags=None,
            is_modified=True, is_extra=False)

        Job.commit_output()
    else:
        continue
