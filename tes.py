import csv

dic={}
with open("ラノベPOP v2__77lines_converter.csv","r",encoding="UTF") as f:
    data=f.readlines()

i=0
for char in data:
    char=char.strip("\n")
    dic[char]=i
    i=i+1

sentence="Kuretan Avatar Text　任意文字の入力・翻訳可能・64文字まで対応可能　Boothでダウンロードできます。"
# print(dic["詰"])
for char in sentence:
    print(dic[char])