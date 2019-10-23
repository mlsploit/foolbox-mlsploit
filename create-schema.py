import inspect
import os
import json

from foolbox import attacks
from foolbox.attacks.base import Attack

import torchvision.models as models
from models import ALLOWED_MODELS

ALLOWED_OPTION_TYPES = ['str', 'float', 'int', 'bool']
ALLOWED_ATTACKS = [
  'BasicIterativeMethod',
  'CarliniWagnerL2Attack',
  'DeepFoolL2Attack',
  'DeepFoolLinfinityAttack',
  'FGSM',
  'IterativeGradientSignAttack',
  'LBFGSAttack',
  'ProjectedGradientDescent',
  'RandomProjectedGradientDescent',
  'SaltAndPepperNoiseAttack',
  'SinglePixelAttack']

def _get_signature(attack_class):
  parameters = list()

  sig = inspect.signature(attack_class.__call__)
  for key, parameter in sig.parameters.items():
    if key not in ['self', 'input_or_adv', 'label', 'unpack']:
      parameters.append((key, type(parameter.default), parameter.default))

  return parameters


def main():
  input_schema = {'functions': []}
  output_schema = {'functions': []}
  
  for name, item in inspect.getmembers(attacks):
    if (inspect.isclass(item)
        and item is not Attack
        and issubclass(item, Attack)
        and len(item.__abstractmethods__) == 0
        and name in ALLOWED_ATTACKS):
      
      fn_input_schema = {
        'name': name,
        'extensions': [
          {'extension': 'jpg'}]}
      
      fn_output_schema = {
        'name': name,
        'output_tags': [
          {'name': 'mlsploit-visualize', 'type': 'str'},
          {'name': 'label', 'type': 'str'}],
        'has_modified_files': True,
        'has_extra_files': False}
      
      options = []
      options.append({
        'name': 'model', 
        'type': 'enum',
        'values': ALLOWED_MODELS,
        'required': True})
      
      for (option_name, 
           option_type, 
           option_default) in _get_signature(item):

        option_type = option_type.__name__
        if option_type in ALLOWED_OPTION_TYPES:
          options.append({
            'name': option_name, 
            'type': option_type,
            'default': option_default,
            'required': True})
      fn_input_schema['options'] = options

      input_schema['functions'].append(fn_input_schema)
      output_schema['functions'].append(fn_output_schema)
  
  with open('input.schema', 'w') as f:
    json.dump(input_schema, f, indent=2)

  with open('output.schema', 'w') as f:
    json.dump(output_schema, f, indent=2)

if __name__ == "__main__":
    main()
