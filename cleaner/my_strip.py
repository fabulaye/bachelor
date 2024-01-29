import regex as re

def my_rstrip(string,stripped):
    pattern=re.compile(stripped)
    search=pattern.findall(string)
    if len(search)>=1:
        string=string[:-len(search[0])]
        return string
    else:
        return string

test=my_rstrip("Invaliden test"," test")
print(test)