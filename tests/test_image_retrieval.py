
from dont_scroll.core.image_retrieval import ImageRetrieval

from dont_scroll.core.utils import cos_sim

def test_hedgehog_similarity():
    """
    hedgehog (hedgehog and hedgehog)
    """

    image_retrieval = ImageRetrieval()
    a = image_retrieval.image_to_vector("./tests/images/hedgehog1.jpg")
    b = image_retrieval.image_to_vector("./tests/images/hedgehog2.jpg")

    ret = cos_sim(a, b)
    print(f"ret : {ret}")

def test_hedgehog_cat_similarity():
    """
    hedgehog (hedgehog and cat)
    """

    image_retrieval = ImageRetrieval()
    a = image_retrieval.image_to_vector("./tests/images/hedgehog1.jpg")
    b = image_retrieval.image_to_vector("./tests/images/cat.png")

    ret = cos_sim(a, b)
    print(f"ret : {ret}")

if __name__ == "__main__":
    assert 0.75 < test_hedgehog_similarity()
    assert test_hedgehog_cat_similarity() < 0.75
