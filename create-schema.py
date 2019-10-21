import inspect
import os

from foolbox import attacks
from foolbox.attacks.base import Attack

from models import ALLOWED_MODELS


def _get_signature(attack_class):
  parameters = list()

  sig = inspect.signature(attack_class.__call__)
  for key, parameter in sig.parameters.items():
    if key not in ['self', 'input_or_adv', 'label', 'unpack']:
      parameters.append((key, type(parameter.default), parameter.default))

  return parameters


def main():
  input_schema = [{'functions': []}]
  output_schema = [{'functions': []}]

  for name, item in inspect.getmembers(attacks):
    if (inspect.isclass(item) 
        and item is not Attack 
        and issubclass(item, Attack) 
        and len(item.__abstractmethods__) == 0):
      fn_output_schema = {
        'name': name,
        'output_tags': [
          {'name': 'mlsploit-visualize', 'type': 'str'},
          {'name': 'label', 'type': 'str'}],
        'has_modified_files': True,
        'has_extra_files': False}

      fn_input_schema = { 'name': name }
      
      print(name)
      print(get_signature(item))
      print('---')

