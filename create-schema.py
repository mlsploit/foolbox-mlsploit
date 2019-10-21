import inspect
import os
import json

from foolbox import attacks
from foolbox.attacks.base import Attack

import torchvision.models as models
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
      options = [{'options': []}]
      for tuple in _get_signature(item):
          nextElement = []
          nextElement.append(('name', tuple[0]))
          nextElement.append(('type', tuple[1]))
          nextElement.append(('default', tuple[2]))
          nextElement.append(('required', "true"))
          options.append(nextElement)
      extension = {"extension": ".jpg"}
      nextAttack = []
      nextAttack.append(('name', name))
      nextAttack.append(('options', options))
      nextAttack.append(('extensions', extension))
      input_schema.append(nextAttack)
    with open("tester.json", 'w') as finishedSchema:
        json.dump(input_schema, finishedSchema)
      #print(name)
      #print(_get_signature(item))
      #print('---')

if __name__ == "__main__":
    main()
