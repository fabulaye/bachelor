import chardet


def change_encoding(input_csv,output_csv):
# Detect the encoding
    with open(input_csv, 'rb') as f:
        result = chardet.detect(f.read())

    current_encoding = result['encoding']

    # Convert the file
    with open(input_csv, 'r', encoding=current_encoding) as f:
        content = f.read()

    with open(output_csv, 'w', encoding='utf-8') as f:
        f.write(content)

change_encoding("C:/Users/lukas/Desktop/bachelor/data/suchliste.csv","C:/Users/lukas/Desktop/bachelor/data/suchliste_utf8.csv")
