import regex as re

def my_rstrip(string,stripped):
    #pattern=re.compile(stripped)
    #search=pattern.findall(string)
    if isinstance(stripped,str) and string.endswith(stripped):
        string=string[:-len(stripped)]
    return string

test=my_rstrip("Invaliden test"," test")
print(test)



    