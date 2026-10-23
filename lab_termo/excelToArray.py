import pyperclip

excel = excel = pyperclip.paste()


result = "["
for line in excel.split():
    line = line.replace(".", "")
    chunks = line.split(",")
    if len(chunks) == 2:
        result += f"{chunks[0]}.{chunks[1]}, "
    else:
        result += f"{chunks[0]}, "
result = result[:-2] + "]"

pyperclip.copy(result)
print(result)