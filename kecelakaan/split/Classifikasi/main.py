from Classification import Classification

if __name__ == "__main__":
    classification = Classification()
    resultClassification=classification.getClassificationValue()

    if (resultClassification == "success"):
        print('Classification Success')