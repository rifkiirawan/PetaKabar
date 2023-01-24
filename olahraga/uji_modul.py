from submodule.NER import NER
from submodule.QueryExpansion import QueryExpansion
from submodule.Severity import Severity
from submodule.Classification import Classification

if __name__ == "__main__":
    # ner = NER()
    # resultNER = ner.getValueNER()
    classification = Classification()
    resultClassification=classification.getClassificationValue()