def test_long_phrase():
    phrase = input("Set a phrase: ")
    long_phrase = len(phrase)
    assert long_phrase < 15, f" phrase is longer 15 characters"
