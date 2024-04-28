import pandas as pd
import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language

@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)


def lang_detect(text):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('language_detector')
    doc = nlp(text)
    result = doc._.language['language']
    return result

if __name__ == "__main__":
    testing_txt = "প্রকল্পের কর্মরত বিল এন্ট্রি দেওয়ার সময় Economic Code পাওয়া যাচ্ছে না।"
    detected_language = lang_detect(testing_txt)

    print(f"The detected language is: {detected_language}")
