import inspect

from foolbox import attacks
from foolbox.attacks.base import Attack

from mlsploit import Module

from _foolboxdocs import docs
from models import ALLOWED_MODELS, CUSTOM_MODEL

DOCTXT_KEY = "doctxt"
PARAMETERS_KEY = "parameters"

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

ATTACK_FN_ARGS = {
    "creates_new_files": True,
    "modifies_input_files": True,
    "expected_filetype": "zip",
    "optional_filetypes": ["jpg", "jpeg", "png"],
}

ATTACK_FN_INPUT_MODEL_OPTION = {
    "name": "model",
    "type": "enum",
    "doctxt": "Pre-trained model to be attacked.",
    "enum_values": ALLOWED_MODELS + [CUSTOM_MODEL],
    "default": ALLOWED_MODELS[0],
    "required": True,
}

CLASSIFY_FN_ARGS = dict(ATTACK_FN_ARGS.items())
CLASSIFY_FN_ARGS.update(modifies_input_files=False)
CLASSIFY_FN_DOCTXT = (
    "This simply classifies the image using the specified model, no attack here."
)

CLASSIFY_FN_INPUT_MODEL_OPTION = dict(ATTACK_FN_INPUT_MODEL_OPTION.items())
CLASSIFY_FN_INPUT_MODEL_OPTION.update(
    doctxt="Pre-trained model to use for classification."
)

CUSTOM_MODEL_OPTION = {
    "name": "custom_model_url",
    "type": "str",
    "doctxt": (
        "Git URL for a foolbox-zoo compatible repository. "
        "Image will be of size 224x224 normalized to [0, 1]. "
        'This option is used when "model" is set to "%s".' % CUSTOM_MODEL
    ),
    "default": "",
    "required": False,
}


def _get_signature(attack_class):
    parameters = list()

    sig = inspect.signature(attack_class.__call__)
    for key, parameter in sig.parameters.items():
        if key not in ["self", "input_or_adv", "label", "unpack"]:
            param_name = key
            param_default = parameter.default
            param_type = type(param_default) if param_default != 1 else float
            param_default = param_type(param_default)
            parameters.append((param_name, param_type, param_default))

    return parameters


def _process_doctxt(doctxt):
    doctxt = doctxt.strip(" \n")
    return doctxt


def _add_output_tags(module_fn):
    module_fn.add_output_tag(name="visualize", type="str")
    module_fn.add_output_tag(name="label", type="str")


def main():
    module = Module.build(
        display_name="Foolbox",
        tagline=docs["tagline"],
        doctxt=_process_doctxt(docs[DOCTXT_KEY]),
        icon_url=docs["icon_url"],
    )

    classify_fn = module.build_function(
        name="Classify", doctxt=CLASSIFY_FN_DOCTXT, **CLASSIFY_FN_ARGS
    )

    classify_fn.add_option(**CLASSIFY_FN_INPUT_MODEL_OPTION)
    classify_fn.add_option(**CUSTOM_MODEL_OPTION)

    _add_output_tags(classify_fn)

    adocs = docs["attacks"]
    for name, item in inspect.getmembers(attacks):
        if (
            inspect.isclass(item)
            and item is not Attack
            and issubclass(item, Attack)
            and len(item.__abstractmethods__) == 0
            and name in ALLOWED_ATTACKS
        ):
            attack_fn = module.build_function(
                name=name,
                doctxt=_process_doctxt(adocs[name][DOCTXT_KEY]),
                **ATTACK_FN_ARGS
            )

            attack_fn.add_option(**ATTACK_FN_INPUT_MODEL_OPTION)
            attack_fn.add_option(**CUSTOM_MODEL_OPTION)

            for (option_name, option_type, option_default) in _get_signature(item):
                option_type = option_type.__name__
                if option_type in ALLOWED_OPTION_TYPES:
                    attack_fn.add_option(
                        name=option_name,
                        type=option_type,
                        doctxt=_process_doctxt(
                            adocs[name][PARAMETERS_KEY][option_name][DOCTXT_KEY]
                        ),
                        default=option_default,
                        required=True,
                    )

            _add_output_tags(attack_fn)

    module.save()


if __name__ == "__main__":
    main()
