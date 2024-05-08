llmData = r"D:\IITD\CoS-data\llmParsing"
unparsedData = ""
parsedData = open(f"{llmData}\\parsedDataUnbracketed.txt", 'r').read()

def readUnparsedData():
    global unparsedData
    for i in range(1, 6):
        file = f"{llmData}\\{i}.txt"
        with open(file, "r") as f:
            unparsedData += f.read()
            unparsedData += "\n"
