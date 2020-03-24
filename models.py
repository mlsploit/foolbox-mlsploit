from foolbox import zoo
import torchvision.models as models


ALLOWED_MODELS = ["vgg16", "resnet18"]
GIT_EXTENSION = ".git"
CUSTOM_MODEL = "custom"


def load_pretrained_model(model_name):
    # https://pytorch.org/docs/stable/torchvision/models.html
    assert model_name in ALLOWED_MODELS
    model_fn = getattr(models, model_name)
    model = model_fn(pretrained=True)

    return model


def load_foolbox_zoo_model(git_url):
    # https://foolbox.readthedocs.io/en/latest/modules/zoo.html
    assert git_url.endswith(GIT_EXTENSION)
    fmodel = zoo.get_model(git_url)

    return fmodel


if __name__ == "__main__":
    for model_name in ALLOWED_MODELS:
        load_pretrained_model(model_name)
