import torchvision.models as models


ALLOWED_MODELS = {'vgg16', 'resnet18'}


def load_pretrained_model(model_name):
    assert model_name in ALLOWED_MODELS
    model_fn = getattr(models, model_name)
    model = model_fn(pretrained=True)

    return model


if __name__ == "__main__":
    for model_name in ALLOWED_MODELS:
        load_pretrained_model(model_name)
