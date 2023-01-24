from QueryExpansion import QueryExpansion

if __name__ == "__main__":
    qe = QueryExpansion()
    resultQE = qe.getWhatFromText("apa sebenarnya kejadian kecelakaan yang terjadi diberita tersebut")
    
    # 3 NER when, who, where, jika hasil qe success
    if (resultQE == "success"):
        print('Query Expansion Success')