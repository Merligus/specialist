import os

# path to the input file
input_file = "dracula.txt"

# path to the out directory
path = "./dracula_segmented"

# create the folder and ignores if it alrerady exists
os.makedirs(path, exist_ok=True)

# word to segment the file
# dracula
words_list = [
    "SUMÁRIO",
    "INTRODUÇÃO",
    "CAPÍTULO I",
    "CAPÍTULO II",
    "CAPÍTULO III",
    "CAPÍTULO IV",
    "CAPÍTULO V",
    "CAPÍTULO VI",
    "CAPÍTULO VII",
    "CAPÍTULO VIII",
    "CAPÍTULO IX",
    "CAPÍTULO X",
    "CAPÍTULO XI",
    "CAPÍTULO XII",
    "CAPÍTULO XIII",
    "CAPÍTULO XIV",
    "CAPÍTULO XV",
    "CAPÍTULO XVI",
    "CAPÍTULO XVII",
    "CAPÍTULO XVIII",
    "CAPÍTULO XIX",
    "CAPÍTULO XX",
    "CAPÍTULO XXI",
    "CAPÍTULO XXII",
    "CAPÍTULO XXIII",
    "CAPÍTULO XXIV",
    "CAPÍTULO XXV",
    "CAPÍTULO XXVI",
    "CAPÍTULO XXVII",
    "CONTO: O HÓSPEDE DE DRÁCULA",
    "A NOVA HISTÓRIA DO",
    "RESENHA",
    "LEITURA",
    "HAMPSHIRE ADVERTISER",
    "Romances Recentes",
    "ENTREVISTA DA",
    "William Gladstone",
    "MARY ELIZABETH BRADDON",
    "SIR ARTHUR CONAN DOYLE",
    "OSCAR WILDE",
    "POSFÁCIO",
    "A SOMBRA DO VAMPIRO",
    "VAMPIRO Enciclopédia Britannica",
    "O Vampiro",
    "Fragmento*",
    "Carmilla",
    "Charles Baudelaire: O Vampiro",
]
# alice
# words_list = [
#     "PRE",
#     "CHAPTER I",
#     "CHAPTER II",
#     "CHAPTER III",
#     "CHAPTER IV",
#     "CHAPTER V",
#     "CHAPTER VI",
#     "CHAPTER VII",
#     "CHAPTER VIII",
#     "CHAPTER IX",
#     "CHAPTER X",
#     "CHAPTER XI",
#     "CHAPTER XII",
# ]

# open the file
with open(
    input_file,
    "r",
) as file:
    # current word to look for
    current_word_idx = 1
    # create the file with the name of the current word
    current_word = words_list[current_word_idx]
    # first file to write the lines
    current_file = open(f"{path}/{words_list[0]}.txt", "w")

    # iterate over the file
    for raw_line in file:
        # filter characters
        line = raw_line # .replace("\xad", "").replace("\n", " ")
        # if the word is in the line...
        if words_list[current_word_idx] in raw_line:
            # close the actual file
            current_file.close()

            # open a new file to write the incoming lines
            current_file = open(f"{path}/{current_word}.txt", "w")
            if current_word_idx + 1 < len(words_list):
                # update the current word to look for in the line
                current_word_idx += 1
                # update the current word
                current_word = words_list[current_word_idx]

        # copy the line
        current_file.write(line)
    # close the last file
    current_file.close()
