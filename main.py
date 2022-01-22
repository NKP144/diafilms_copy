import xml.etree.ElementTree as ET
#from xml.etree import ElementTree
import requests
import os

url = 'https://diafilmy.su/dia-list-androidgz.php'

response = requests.get(url)
with open('diafilm.xml', 'wb') as file:
   file.write(response.content)
#parser = ET.XMLParser(encoding="utf-8")
#tree = ET.parse("diafilm.xml", parser=parser)
tree = ET.parse("diafilm.xml")

#tree = ElementTree.parse("students.xml")

root = tree.getroot()
print(root)

with open('main/urls.csv', 'w') as file:
    file.write("id; Имя; Путь к фильму; Путь к постеру; \n")
    for child in root:
        print(child[1].text, child[3].text, child[4].text, child[5].text, sep='\n')
        write_str = f"{child[1].text}; {child[3].text}; {child[4].text}; {child[5].text}; \n"
        file.write(write_str)

#count = 0;
#for i in root:
#    print(count)
#    count += 1

print(len(root))
for i in range(len(root)):
    url = f"https://www.diafilmy.su/dia-android.php?id={root[i][1].text}"
    response = requests.get(url)

    path = f"films/{root[i][3].text}"
    print(path)
    try:
        os.mkdir(path)
    except OSError:
        print("Создать директорию %s не удалось" % path)
    else:
        print("Успешно создана директория %s " % path)

    try:
        open(f"{path}/db.xml", 'wb')
    except OSError:
        print("%s - слишком длинное имя" % path)
        continue
    else:
        print("Файл открыт")

    with open(f"{path}/db.xml", 'wb') as file:
        file.write(response.content)

    slides_tree = ET.parse(f"{path}/db.xml")
    slides_root = slides_tree.getroot()
    print(slides_root)
    element = slides_root[2]
    print(element[0].text)

    with open(f"{path}/slides_urls.txt", 'w') as file:
        for slides_child in element:
            print(slides_child.text)
            if slides_child.text:
                file.write(slides_child.text + "\n")








