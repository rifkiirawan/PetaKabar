from NER import NER

if __name__ == "__main__":
    ner = NER()
    resultNER = ner.getValueNER()

    if (resultNER == "success"):
        print('NER Success')