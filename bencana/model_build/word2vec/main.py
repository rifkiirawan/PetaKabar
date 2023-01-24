import gensim
# import pandas as pd
import csv

path = './idwiki_word2vec_200_new_lower.model'
id_w2v = gensim.models.word2vec.Word2Vec.load(path)

# maximal value dari cosine similarity dalah 1

def similar(kata, proseske):
    most_similars = id_w2v.wv.most_similar(kata)
    arr = []

    # proses masukin ke csv
    f = open('bow_bencana.csv', 'a', encoding='UTF8', newline='')

    f1 = open("<=62.csv", "a", encoding='UTF8', newline='')
    f2 = open(">62.csv", "a", encoding='UTF8', newline='')

    for x in range(len(most_similars)):
        words = most_similars[x][0]
        similarity = most_similars[x][1]
        # print(words)
        # print(similarity)
        result = [words, similarity]
        # if similarity > maxDistance:
        #     maxDistance = similarity
        # elif similarity < minDistance:
        #     minDistance = similarity

        if round(similarity, 2) <= 0.62:
            f1writer = csv.writer(f1)
            f1writer.writerow(result)
        else:
            f2writer = csv.writer(f2)
            f2writer.writerow(result)
        
        arr.append((words, similarity))

    writer = csv.writer(f)
    writer.writerow([str(proseske), kata, most_similars])

    f.close()
    f1.close()
    f2.close()

    return(arr)


def tree(arr, proseske):
    hasil = []
    for x in range(len(arr)):
        for y in range(10):
            words = arr[x][y][0]
            similarity = arr[x][y][1]
            # if round(similarity, 2) <= 0.62:
            tes = similar(words, proseske)
            hasil.append(tes)
    return(hasil)


if __name__ == "__main__":
    path = './idwiki_word2vec_200_new_lower.model'
    id_w2v = gensim.models.word2vec.Word2Vec.load(path)

    f = open('bow_bencana.csv', 'w', encoding='UTF8')
    writer = csv.writer(f)
    writer.writerow(['tingkat setelah parent', 'parent', 'similarity'])

    f1 = open("<=62.csv", "w", encoding='UTF8', newline='')
    writer = csv.writer(f1)
    writer.writerow(['Word', 'Similarity'])
    f1.close()

    f2 = open(">62.csv", "w", encoding='UTF8', newline='')
    writer = csv.writer(f2)
    writer.writerow(['Word', 'Similarity'])
    f2.close()

    f.close()
    x = 0

    tes = similar('bencana', x)
    data = []
    data.append(tes)

    while(True):
        if(x <= 2):
            x = x+1
            coba = tree(data, x)
            data = coba
            continue
        else:
            # print('maxDistance ' + str(maxDistance) + '\n')
            # print('minDistance ' + str(minDistance) + '\n')
            break
