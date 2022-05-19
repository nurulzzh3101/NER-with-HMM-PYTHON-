import nltk
import string
import re
from nltk import word_tokenize
import numpy as np


# fungsi punctuation teks
def remove_punc(string):
    punc = """():","""
    for ele in string:
        if ele in punc:
            string = string.replace(ele, "")
    return string


#DATA LATIH
# pre-processing (baca file data latih)
print("PREPROCESSING DATA LATIH :")
filename = "latih.txt"
file = open(filename, "r")
text_latih = file.readlines()  # membaca isi data latih
print("Data Latih :")
print(text_latih)
file.close()

# pre-processing (hilangkan punctuation dari teks data latih )
punctuation_latih = [remove_punc(i) for i in text_latih]  # menggunakan fungsi remove_punc
print("\nHasil Hilangkan tanda baca Data Latih :")
for i in punctuation_latih:
    print(i)

# pre-processing (mengubah huruf teks data latih menjadi lowecase)
lower_case_latih = [i.casefold() for i in punctuation_latih]
print("\nHasil Case Folding ke lower Case Data Latih :")
for i in lower_case_latih:
    print(i)

# pre-processing (tokenisasi teks data latih menjadi bentuk list)
print("\nHasil Tokenisasi Data Latih :")
list_token = []
for i in lower_case_latih:
    token_latih = word_tokenize(i)
    token_erase_latih = [
        word for word in token_latih if word not in ("", ".")  # hapus token isinya titik
    ]
    # menambahkan hasil tokenisasi menjadi list
    list_token.append(token_erase_latih)
# mengubah list hasil tokenisasi menjadi array
list_token = np.array(list_token, dtype=list)
print(list_token)


# pemisahan label tag NER dengan kata dalam data latih hasil tokenisasi 
print("\nPisahkan Kata dengan Label NER :")
print("Label NER data latih: (emisi)")
# tag NER untuk emisi
label = []
i = 0
while i < len(list_token):
    j = 0
    while j < len(list_token[i]):
        # pemisahan label tag NER (untuk emisi)
        token_label = re.sub(".*[/]", "", list_token[i][j])
        # menambahkan data dalam list
        label.append(token_label)
        j = j + 1
    i = i + 1
print(label)
print("\n")

print("Kata data latih: (emisi)")
# kata untuk emisi
word = []
i = 0
while i < len(list_token):
    j = 0
    while j < len(list_token[i]):
        # pemisahan kata (untuk emisi)
        token_word = re.sub("[/].*", "", list_token[i][j])
        # menambahkan data dalam list
        word.append(token_word)
        j = j + 1
    i = i + 1
print(word)
print("\n")

print("Label NER data latih: (transisi)")
# tag NER untuk transisi
label2 = []
i = 0
while i < len(list_token):
    j = 0
    tag = []
    while j < len(list_token[i]):
        # pemisahan label tag NER (untuk transisi)
        token_label2 = re.sub(".*[/]", "", list_token[i][j])
        # menambahkan data dalam list
        tag.append(token_label2)
        j = j + 1
    # menambahkan data dalam list
    label2.append(tag)
    i = i + 1
print(label2)
print("\n")


# tag NER unik (loc, org, oth, per, time)
print("\nTag NER Unik data latih:")
tag_ner = []
i = 0
for i in label:
    if i not in tag_ner:
        # menambahkan data dalam list
        tag_ner.append(i)
# mengurutkan tag_ner sesuai abjad
tag_ner.sort()
tag_ner.insert(0, "loc") #menambahkan label NER loc karena di data latih tidak ada kata dg label loc
print(tag_ner, "\n")

# kata unik
print("\nKata Unik data latih:")
kata = []
i = 0
for i in word:
    if i not in kata:
        # menambahkan data dalam list
        kata.append(i)
# mengurutkan kata sesuai abjad
kata.sort()
print(kata, "\n")


# perhitungan EMISI (nilai pasangan kata dengan tag_NER)
print("\nEMISI : (nilai pasangan kata data latih)")  #
emisi1 = []
i = 0
for i in range(len(kata)):  # baris emisi (kata unik)
    j = 0
    kolom = []
    for j in range(len(tag_ner)):  # kolom emisi (tag ner unik)
        hitung = 0
        for k in range(len(word)):  # mengecek untuk tiap kata dari hasil pemisahan
            if kata[i] == word[k]:  # jika kata unik = kata hasil pemisahan
                if tag_ner[j] == label[k]:  # jika tag ner unik = tag hasil pemisahan
                    hitung = hitung + 1  # mengitung jumlah tag dalam suatu kata
        # menambahkan data dalam list
        kolom.append(hitung)
    # menambahkan data dalam list
    emisi1.append(kolom)
# print emisi1 / pasangan kata dan tag_ner
for i in range(len(kata)):
    print(emisi1[i])


# perhitungan EMISI (mencari nilai probabilitas emisi)
print("\nEMISI :")
print("EMISI : (nilai probabilitas emisi data latih)")
i = 0
j = 0
k = 0
# menghitung totalnya perkolom tag
for j in range(len(tag_ner)):  # kolom emisi
    count = 0
    for i in range(len(kata)):  # baris emisi
        count = count + emisi1[i][j]  # mengitung jumlah total per tag ner (perkolom)
    for k in range(len(emisi1)):
        if count != 0:
            emisi1[k][j] = emisi1[k][j] / count  # menghitung nilai probabilitas emisi tiap tag ner
        if count == 0:
            emisi1[k][j] = count
# print emisi1 / hasil probabilitas emisi per tag ner
for i in range(len(kata)):
    print(emisi1[i])


# perhitungan TRANSISI (nilai kejadian bersama)
print("\nTRANSISI : ")
tag_nerbaru = tag_ner.copy()  # membuat variabel baru dg menyalin data dari tag_ner
tag_nerbaru.insert(0, "<S>")
tag_nerbaru2 = tag_ner.copy()  # membuat variabel baru dg menyalin data dari tag_ner
tag_nerbaru2.append("<E>")  # menambahkan data <E> di akhir list
print("Tag NER baru :")
print(tag_nerbaru)
print(tag_nerbaru2)


# menghitung nilai kejadian bersama
print("\nTRANSISI : (nilai kejadian bersama data latih)")
transisi1 = []
i = 0
for i in range(len(tag_nerbaru)):  # baris transisi (<S> + tag_ner)
    kol = []
    for j in range(len(tag_nerbaru2)):  # kolom transisi (tag_ner + <E>)
        jumlah = 0
        for x in range(len(label2)):  # mengecek untuk tiap tag ner dari hasil pemisahan (baris)
            for y in range(len(label2[x])):  # mengecek untuk tiap tag ner dari hasil pemisahan (kolom)

                # mencari menghitung jumlah tag yang ada di awal kalimat / <S>
                if (i == 0):  # hanya mengecek pada baris dengan indeks 0 pada list
                    if (y == 0):  # hanya mengecek pada kolom dengan indeks 0 pada tiap baris list
                        if (tag_nerbaru2[j] == label2[x][y]):
                            jumlah = jumlah + 1

                # mencari dan menghitung jumlah tag yang ada di akhir kalimat / <E>
                if (j == len(tag_nerbaru2) - 1):  # hanya mengecek pada kolom dengan indeks akhir pada list
                    if y == len(label2[x]) - 1:  # hanya mengecek pada kolom dengan indeks akhir pada tiap baris list
                        if (tag_nerbaru[i] == label2[x][y]):
                            jumlah = jumlah + 1

                # mencari dan menghitung jumlah tag yang bertemu dengan tag lain
                if (y < len(label2[x]) - 1):  # mengecek kolom dengan indeks 0 sampai (len-1) pada tiap baris list
                    if tag_nerbaru[i] == label2[x][y]:
                        if tag_nerbaru2[j] == label2[x][y + 1]:  # mengecek tag apa yang dimiliki pada indeks setelahnya
                            jumlah = jumlah + 1
        # menambahkan data pada list
        kol.append(jumlah)
    # menambahkan data pada list
    transisi1.append(kol)
# print transisi1 / kejadian bersama
for i in range(len(transisi1[i])):
    print(transisi1[i])


# perhitungan TRANSISI (mencari nilai probabilitas transisi)
print("\nTRANSISI : (nilai probabilitas transisi data latih)")
i = 0
j = 0
x = 0
# menghitung totalnya perbaris tag
for i in range(len(transisi1)):  # baris transisi
    jumlah = 0
    for j in range(len(transisi1[i])):  # kolom transisi
        jumlah = jumlah + transisi1[i][j]  # mengitung jumlah total per tag ner baru (perbaris)
    for x in range(len(transisi1[i])):
        if jumlah != 0:
            transisi1[i][x] = transisi1[i][x] / jumlah  # menghitung nilai probabilitas transisi tiap tag ner baru
        if jumlah == 0:
            transisi1[i][x] = 0
# print transisi1 / hasil probabilitas transisi per tag ner
for i in range(len(transisi1[i])):
    print(transisi1[i])
print("\n\n")




# DATA UJI
print("PREPROCESSING DATA UJI :")
# pre-processing (baca file data uji)
filename = "uji.txt"
file = open(filename, "r")
text_uji = file.readlines()  # membaca isi data uji
print("Data uji :")
print(text_uji)
file.close()

# pre-processing (hilangkan punctuation dari teks data uji )
punctuation_uji = [remove_punc(i) for i in text_uji]  # menggunakan fungsi remove_punc
# print("\nHasil Hilangkan tanda baca Data uji :\n")
# for i in punctuation_uji:
#    print(i)

# pre-processing (mengubah huruf teks data uji menjadi lowecase)
lower_case_uji = [i.casefold() for i in punctuation_uji]
# print("\nHasil Case Folding ke lower Case Data uji :\n")
# for i in lower_case_uji:
#    print(i)

# pre-processing (tokenisasi teks data latih menjadi bentuk list)
# print("\nHasil Tokenisasi Data uji :")
list_token_uji = []
for i in lower_case_uji:
    token_uji = word_tokenize(i)
    token_erase_uji = [
        word for word in token_uji if word not in ("", ".")  # hapus token isinya titik
    ]
    # menambahkan hasil tokenisasi menjadi list
    list_token_uji.append(token_erase_uji)
# mengubah list hasil tokenisasi menjadi array
list_token_uji = np.array(list_token_uji, dtype=list)
# print(list_token_uji)


print("\nPemisahan Tag  NER dan kata data uji:")
# pemisahan label tag NER dengan kata dalam data uji hasil tokenisasi
word_uji = []
label2_uji = []
i =0
while i < len(list_token_uji):
    j = 0
    tag=[]
    kata_token =[]
    while j < len(list_token_uji[i]):
        #pemisahan kata data uji
        uji_word = re.sub("[/].*", "", list_token_uji[i][j])
        #pemisahan label tag ner data uji
        uji_label2 = re.sub(".*[/]", "", list_token_uji[i][j])
        #tambah data dalam list
        kata_token.append(uji_word)
        tag.append(uji_label2)
        j = j + 1
    #tambah data dalam list
    label2_uji.append(tag)
    word_uji.append(kata_token)
    i = i + 1
print("label tag ner data uji :")
print(label2_uji)
print("\nkata data uji :")
print(word_uji)


# perhitungan emisi (mencari nilai probabilitas emisi data uji)
print("\nhasil probabilitas emisi data uji : ")
emisi_uji = []
#mencari nilai probabilitas emisi data uji dari probabilitas emisi data latih
for i in range (len(word_uji)) : #baris emisi (kata hasil pemisahan)
    kol = []
    for j in range (len(word_uji[i])) : #kolom emisi (kata hasil pemisahan)
        hitung = 0
        for x in range (len(emisi1)) : #mengecek  baris pada tabel emisi data latih
            for y in range (len(emisi1[x])) : #mengecek pada kolom emisi data latih
                if word_uji[i][j] == kata[x] : #jika kata hasil pemisahan = kata unik data latih
                    if label2_uji[i][j] == label[y] : #jika label NER hasil pemisahan = label NER hasil pemisahan data latih
                        hitung = emisi1[x][y] #get data probabilitas emisi data latih dengan kata dan label yg sesuai
        #tambah data ke list
        kol.append(hitung)
    #tambah data ke list
    emisi_uji.append(kol)
# print emisi_uji data uji
for i in range (len(emisi_uji)):
    print(emisi_uji[i])


# perhitungan transisi (mencari nilai probabilitas transisi data uji)
print("\nhasil probabilitas transisi data uji : ")
transisi_uji = []
#mencari nilai probabilitas transisi data uji dari probabilitas transisi data latih
for i in range (len(label2_uji)) :
    label2_uji[i].append("<E>") #menambahkan data <E> pada tiap akhir baris
    label2_uji[i].insert(0, "<S>")  #menambahkan data <S> pada tiap awal baris
print(label2_uji)

for i in range (len(label2_uji)) : #baris transisi (label NER hasil pemisahan)
    kol = []
    for j in range (len(label2_uji[i])): #kolom transisi (label NER hasil pemisahan)
        hitung = 0
        for x in range (len(transisi1)): #mengecek baris pada tabel transisi data latih
            for y in range (len(transisi1[x])): #mengecek kolom pada tabel transisi data latih
                if label2_uji[i][j] == tag_nerbaru[x] : #jika label hasil pemisahan = <S>+label NER unik data latih
                    if label2_uji[i][j+1] == tag_nerbaru2[y] : #jika label hasil pemisahan = label NER unik+<E> data latih
                        hitung = transisi1[x][y] #get data probabilitas transisi data latih dengan label yang sesuai
        #tambah data ke list
        kol.append(hitung)
    #tambah data ke list
    transisi_uji.append(kol)
# print transisi_uji data uji
for i in range (len(transisi_uji)) :
    print(transisi_uji[i])
  
    
#probabilitas akhir 
print("\nnilai probabilitas : ")
print("nilai probabilitas emisi : ")
probabilitas_emisi = []
for i in range(len(emisi_uji)) : #baris prob emisi (emisi data uji)
    kol = []
    hitung = 1
    for j in range(len(emisi_uji[i])) : #kolom prob emisi (emisi data uji)
        hitung = emisi_uji[i][j] * hitung #menghitung total emisi untuk tiap barisnya
    #tambah data ke list
    probabilitas_emisi.append(hitung)
#print prob emisi 
for i in range (len(probabilitas_emisi)) :
    print(probabilitas_emisi[i])

print("\nnilai probabilitas transisi: ")
probabilitas_transisi = []
for i in range(len(emisi_uji)) : #baris prob transisi (transisi data uji)
    kol = []
    hitung = 1
    for j in range(len(emisi_uji[i])) : #kolom prob transisi (transisi data uji)
        hitung = transisi_uji[i][j] * hitung  #menghitung total transisi untuk tiap barisnya
     #tambah data ke list
    probabilitas_transisi.append(hitung)
#print prob transisi 
for i in range (len(probabilitas_transisi)) :
    print(probabilitas_transisi[i])
    
print("\nnilai probabilitas total: ")   
probabilitas_total = []
#karena panjang index prob emisi dan prob transisi sama, maka kita gunakan salah satu
for i in range (len(probabilitas_emisi)) : 
    hitung = probabilitas_emisi[i] * probabilitas_transisi[i] #menghitung total probabilitas untuk tiap barisnya
    #tambah data ke list
    probabilitas_total.append(hitung)
print(probabilitas_total)