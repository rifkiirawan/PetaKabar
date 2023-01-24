import gensim
import pandas as pd
import csv

path = './model/idwiki_word2vec_200_new_lower.model'
id_w2v = gensim.models.word2vec.Word2Vec.load(path)


def nextproses(kata):
    tes = id_w2v.wv.most_similar(kata)
    arr = []

    for x in range(len(tes)):
        arr.append(tes[x][0])

    return(arr)


def similar(kata, proseske):
    tes = id_w2v.wv.most_similar(kata)
    arr = []

    # proses masukin ke csv

    f = open('bow_kesehatan.csv', 'a', encoding='UTF8', newline='')

    for x in range(len(tes)):
        arr.append(tes[x][0])

    writer = csv.writer(f)
    writer.writerow([str(proseske), kata, tes])

    f.close()

    return(arr)


def tree(arr, proseske):
    hasil = []
    for x in range(len(arr)):
        for y in range(10):
            tes = similar(arr[x][y], proseske)
            hasil.append(tes)
    return(hasil)


if __name__ == "__main__":

    path = './model/idwiki_word2vec_200_new_lower.model'
    id_w2v = gensim.models.word2vec.Word2Vec.load(path)

    # setelah proses pertama ini di comen sampe
    # f = open('bow_kesehatan.csv', 'w', encoding='UTF8',)

    # writer = csv.writer(f)
    # writer.writerow(['tingkat setelah parent', 'parent', 'similarity'])

    # f.close()
    # sini
    x = 6

    # ini buat tes pertaman
    # tes = similar('kanker', x)

    # ini tes kedua dan seterusnya
    tes = nextproses('stroke')

    data = []
    data.append(tes)

    # ini ingin mulai proses dari angka brp

    while(True):

        # ini mau sampe proses ke berapa di looping
        if(x < 10):

            # setelah proses pertama ini pindah ke bawah coba = tree .....
            
            
            # ini setelah proses satu pindah ke atas x=x+1
            coba = tree(data, x)
            x = x+1
            data = coba
            print(x)
            continue
        else:
            break