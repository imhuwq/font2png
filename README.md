# font2png
---

Convert characters in a font file to png pictures.

This project is inited from [fontforge](https://github.com/fontforge/fontforge), and simply does the two modifications:
- delete code unrelated to font-image conversion
- make it installable by `python3 setup.py install`

Great thanks to [fontforge](https://github.com/fontforge/fontforge) and all it's [authors](https://github.com/fontforge/fontforge/blob/master/AUTHORS).


## 1. How to install
1.1 first prepare system dependencies:
```shell script
sudo apt install libjpeg-dev && \
  libtiff5-dev && \
  libpng-dev && \
  libfreetype6-dev && \
  libgif-dev && \
  libxml2-dev && \
  libpango1.0-dev  && \
  python3-dev && \
  cmake && \
  build-essential
```

1.2 then install this package by python3:
```shell script
python3 setup.py install
```

## 2. How to use it
```python
# example.py
from font2png import font2png

font_file = "data/fontscn_3jqwe90k.ttf"


def main():
    font_mapping = font2png(font_file)
    for character, data in font_mapping.items():
        print(character, data)

if __name__ == "__main__":
    main()

```
