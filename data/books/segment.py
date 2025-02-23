import os

# path to the directory with the files
path = "./alice_segmented"

# create the folder and ignores if it alrerady exists
os.makedirs(path, exist_ok=True)

# word to segment the file
# words_list = [
#     "SUMÁRIO",
#     "INTRODUÇÃO",
#     "CA­PÍ­TU­LO I",
#     "CA­PÍ­TU­LO II",
#     "CA­PÍ­TU­LO III",
#     "CA­PÍ­TU­LO IV",
#     "CA­PÍ­TU­LO V",
#     "CA­PÍ­TU­LO VI",
#     "CA­PÍ­TU­LO VII",
#     "CA­PÍ­TU­LO VI­II",
#     "CA­PÍ­TU­LO IX",
#     "CA­PÍ­TU­LO X",
#     "CA­PÍ­TU­LO XI",
#     "CA­PÍ­TU­LO XII",
#     "CA­PÍ­TU­LO XI­II",
#     "CA­PÍ­TU­LO XIV",
#     "CA­PÍ­TU­LO XV",
#     "CA­PÍ­TU­LO XVI",
#     "CA­PÍ­TU­LO XVII",
#     "CA­PÍ­TU­LO XVI­II",
#     "CA­PÍ­TU­LO XIX",
#     "CA­PÍ­TU­LO XX",
#     "CA­PÍ­TU­LO XXI",
#     "CA­PÍ­TU­LO XXII",
#     "CA­PÍ­TU­LO XXI­II",
#     "CA­PÍ­TU­LO XXIV",
#     "CA­PÍ­TU­LO XXV",
#     "CA­PÍ­TU­LO XX­VI",
#     "CA­PÍ­TU­LO XX­VII",
#     "CON­TO: O HÓS­PE­DE DE DRÁ­CU­LA",
#     "A NO­VA HIS­TÓ­RIA DO",
#     "RE­SE­NHA",
#     "LEI­TU­RA",
#     "HAMPSHI­RE AD­VER­TI­SER",
#     "Ro­man­ces Re­cen­tes",
#     "EN­TRE­VIS­TA DA",
#     "Wil­li­am Glads­to­ne",
#     "MARY ELI­ZA­BE­TH BRAD­DON",
#     "SIR AR­THUR CO­NAN DOY­LE",
#     "OS­CAR WIL­DE",
#     "POS­FÁ­CIO",
#     "A SOM­BRA DO VAM­PI­RO",
#     "VAMPIRO En­ci­clo­pé­dia Bri­tan­ni­ca",
#     "O Vam­pi­ro",
#     "Frag­men­to*",
#     "Car­mil­la",
#     "Char­les Bau­de­lai­re: O Vam­pi­ro",
# ]
words_list = [
    "PRE",
    "CHAPTER I",
    "CHAPTER II",
    "CHAPTER III",
    "CHAPTER IV",
    "CHAPTER V",
    "CHAPTER VI",
    "CHAPTER VII",
    "CHAPTER VIII",
    "CHAPTER IX",
    "CHAPTER X",
    "CHAPTER XI",
    "CHAPTER XII",
]

# open the file
with open(
    "alice_in_wonderland.md",
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
