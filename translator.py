from googletrans import Translator
sen = str(input("Enter a sentence: "))
k = Translator()
lang = str(input("Enter the language: "))
convert = str(input(" To which language should the input be converted to? "))
output = k.translate(sen,src=lang,dest=convert)
print(output.text)
