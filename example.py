from font2png import font2png

font_file = "data/fontscn_3jqwe90k.ttf"


def main():
    font_mapping = font2png(font_file)
    for character, data in font_mapping.items():
        print(character, data)


if __name__ == "__main__":
    main()
