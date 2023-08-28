import ssl
from typing import Union

import clip
import torch
from PIL import Image

from dont_scroll.core.utils import cos_sim
from dont_scroll.logger import applogger

ssl._create_default_https_context = ssl._create_unverified_context


class ImageRetrieval:
    def __init__(self, model: str = None, device: str = None):
        """
        :param model: Model version. HINT) ViT-B/32
        :param device: Device HINT) cuda:0, cpu
        """

        if device == None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device

        if model == None:
            model = "ViT-B/32"

        self.model, self.preprocess = clip.load(model, device=device)

    def image_text(self, image_path: str):
        """
        Correlation between Images and Text
        :param image_path: image path
        """
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        text = clip.tokenize(["a hedgehog", "a dog", "a cat"]).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_features = self.model.encode_text(text)

            logits_per_image, logits_per_text = self.model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        print("Label probs:", probs)
        return probs

    def image_to_vector(self, image: Union[Image.Image, str]):
        """
        Image to vector
        :param image: image path or Image.Image
        """

        if isinstance(image, Image.Image):
            # TODO
            pass
        elif isinstance(image, str):
            image = Image.open(image)
        else:
            # TODO
            print("Error type error.")

        image = self.preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)

        if __debug__:
            applogger.debug(f"image_features : {image_features[0, :3]}")
            applogger.debug(f"image_features : {image_features.shape}")

        image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features[0]

    def text_to_vector(self, text: str):
        """
        Image to vector
        :param text: text
        """
        text = clip.tokenize([text]).to(self.device)

        with torch.no_grad():
            text_features = self.model.encode_text(text)

        if __debug__:
            applogger.debug(f"text_features : {text_features[0, :3]}")
            applogger.debug(f"text_features : {text_features.shape}")

        text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features[0]

    def vectorization(self, image: str, text: str):
        """Vectorization
        :param str image: image path
        :param str text: text
        :return: vectorized vector
        """

        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        text = clip.tokenize([text]).to(device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_features = self.model.encode_text(text)

        logits_per_image, logits_per_text = self.model(image, text)

        return logits_per_image, logits_per_text


if __name__ == "__main__":
    image_retrieval = ImageRetrieval()
    image_retrieval.image_text("./tests/images/hedgehog1.jpg")

    a = image_retrieval.image_to_vector("./tests/images/hedgehog1.jpg")
    b = image_retrieval.image_to_vector("./tests/images/hedgehog2.jpg")

    ret = cos_sim(a, b)
    print(f"ret : {ret}")
