import string

class TextModifier:

    def ladder(sentence):
        palavras = ""
        for i in range((len(sentence)*2-1)):
            if (i>=len(sentence)):
                word = sentence[0:(len(sentence)-(i-len(sentence)+1))]
                if (word[len(word)-1] != " "):
                    palavras+=word
                    palavras+="\n"
            else:
                word = sentence[0:(i+1)]
                if (word[len(word)-1] != " "):
                    palavras+=word
                    palavras+="\n"
        return palavras

    def emojify(sentence):
        alfabeto = string.ascii_lowercase[:27]
        with open("textmodifier/emoji_letters.txt", 'r', encoding="utf-8") as arquivo:
            lines = arquivo.readlines()

        indice_alfabeto = 0

        emojis = {}

        emoji = ""
        for line in lines:
            if(len(line) > 1):
                emoji+=line
            else:
                emojis[alfabeto[indice_alfabeto]] = emoji
                emoji = ""
                indice_alfabeto+=1
                
        emojis[alfabeto[indice_alfabeto]] = emoji


        word = sentence
        word = word.lower()

        emojified = ""

        for letter in word:
            if(letter in emojis.keys()):
                emojified+=emojis[letter]+"\n"
            else:
                emojified+="\n\n"

        return emojified