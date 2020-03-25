import inspect
import os
import json

from foolbox import attacks
from foolbox.attacks.base import Attack

from foolboxdocs import docs
from models import ALLOWED_MODELS, CUSTOM_MODEL

ALLOWED_OPTION_TYPES = ["str", "float", "int", "bool"]
ALLOWED_ATTACKS = [
    "BasicIterativeMethod",
    "CarliniWagnerL2Attack",
    "DeepFoolL2Attack",
    "FGSM",
    "IterativeGradientSignAttack",
    "ProjectedGradientDescent",
    "SaltAndPepperNoiseAttack",
    "SinglePixelAttack",
]

DOCTXT = "doctxt"
TAGLINE = "tagline"


def _get_signature(attack_class):
    parameters = list()

    sig = inspect.signature(attack_class.__call__)
    for key, parameter in sig.parameters.items():
        if key not in ["self", "input_or_adv", "label", "unpack"]:
            parameters.append((key, type(parameter.default), parameter.default))

    return parameters


def _process_doctxt(doctxt):
    for _ in range(4):
        doctxt = doctxt.strip()
        doctxt = doctxt.strip("\n")
    return doctxt


def _get_custom_model_option():
    return {
        "name": "custom_model_url",
        "type": "str",
        "required": False,
        "doctxt": (
            "Git URL for a foolbox-zoo compatible repository. "
            "Image will be of size 224x224 normalized to [0, 1]. "
            'This option is used when "model" is set to "%s".' % CUSTOM_MODEL
        ),
    }


def _get_classify_schema():
    name = "Classify"

    fn_input_schema = {
        "name": name,
        "extensions": [{"extension": "jpg"}, {"extension": "db"}],
        "doctxt": "This simply classifies the image using the specified model, no attack here.",
        "options": [
            {
                "name": "model",
                "type": "enum",
                "values": ALLOWED_MODELS + [CUSTOM_MODEL],
                "required": True,
                "doctxt": "Pre-trained model to use for classification.",
            },
            _get_custom_model_option(),
        ],
    }

    fn_output_schema = {
        "name": name,
        "output_tags": [
            {"name": "mlsploit-visualize", "type": "str"},
            {"name": "label", "type": "str"},
        ],
        "has_modified_files": True,
        "has_extra_files": True,
    }

    return fn_input_schema, fn_output_schema


def main():

    input_schema = {"functions": []}
    output_schema = {"functions": []}

    clf_ism, clf_osm = _get_classify_schema()
    input_schema["functions"].append(clf_ism)
    output_schema["functions"].append(clf_osm)

    if DOCTXT in docs:
        input_schema[DOCTXT] = _process_doctxt(docs[DOCTXT])
    if TAGLINE in docs:
        input_schema[TAGLINE] = docs[TAGLINE]
    adocs = docs["attacks"]

    for name, item in inspect.getmembers(attacks):
        if (
            inspect.isclass(item)
            and item is not Attack
            and issubclass(item, Attack)
            and len(item.__abstractmethods__) == 0
            and name in ALLOWED_ATTACKS
        ):

            fn_input_schema = {
                "name": name,
                "extensions": [{"extension": "jpg"}, {"extension": "db"}],
            }

            fn_output_schema = {
                "name": name,
                "output_tags": [
                    {"name": "mlsploit-visualize", "type": "str"},
                    {"name": "label", "type": "str"},
                ],
                "has_modified_files": True,
                "has_extra_files": True,
            }

            if name in adocs and DOCTXT in adocs[name]:
                fn_input_schema[DOCTXT] = _process_doctxt(adocs[name][DOCTXT])

            options = []
            options.append(
                {
                    "name": "model",
                    "type": "enum",
                    "values": ALLOWED_MODELS + [CUSTOM_MODEL],
                    "required": True,
                    "doctxt": "Pre-trained model to be attacked.",
                }
            )
            options.append(_get_custom_model_option())

            for (option_name, option_type, option_default) in _get_signature(item):

                option_type = option_type.__name__
                if option_type in ALLOWED_OPTION_TYPES:
                    opt = {
                        "name": option_name,
                        "type": option_type,
                        "default": option_default,
                        "required": True,
                    }

                    if name in adocs and option_name in adocs[name]["parameters"]:
                        opt[DOCTXT] = _process_doctxt(
                            adocs[name]["parameters"][option_name][DOCTXT]
                        )

                    options.append(opt)

            fn_input_schema["options"] = options
            input_schema["functions"].append(fn_input_schema)
            output_schema["functions"].append(fn_output_schema)

    with open("input.schema", "w") as f:
        json.dump(input_schema, f, indent=2)

    with open("output.schema", "w") as f:
        json.dump(output_schema, f, indent=2)


if __name__ == "__main__":
    main()
