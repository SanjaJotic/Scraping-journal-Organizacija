import PyPDF2
import sys
import re
from os import listdir
import os

dir = os.getcwd()
path = dir + "\\radovi\\"
sys.path.append(path)
pdf_files = [f for f in listdir(path) if f.endswith(".pdf")]


kljucne_rijeci = []
naslov_autor = []
autor_rijeci = []

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# open pdf, find keywords and append pair pdf_tittle|keywords to list kljucne_rijeci
for pdf in pdf_files:
    pdfFileObj = open(path+pdf, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=True)
    pageObj = pdfReader.getPage(0)
    sadrzaj = pageObj.extractText()
    sadrzaj = sadrzaj.strip("\t")
    kljucne_rijeci.append([str(pdf).strip(".pdf"), re.findall(r'(Keywords:|Key words:|Ključne besede:.*\n)(\s*.*\n)?', sadrzaj)])
    pdfFileObj.close()

# append pairs pdf_tittle|authors to list naslov_autor
with open(dir + "\\autori.txt", "r", encoding="utf8") as f:
    for line in f:
        naslov_autor.append(line.strip())

# check if pdf tittles are matching and save pair authors|keywords to list
for i in naslov_autor:
    naslov, autor = i.split("|")
    for rijec in kljucne_rijeci:
        rijec[1] = str(rijec[1]).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace("\n","").replace("Keywords:","").replace("Key words:","").replace("Keywords","")
        if rijec[0] == naslov:
            autor_rijeci.append((autor, rijec[1]))

# save pairs authors|keywords to file
for par in autor_rijeci:
    with open(dir + "\\autori_kljucnerijeci.txt", "a+", encoding="utf8") as f:
        f.write(str(par[0]) + "|" + str(par[1]).replace("\\n","") + "\n")