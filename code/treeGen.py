import json
import re

subGraphID = 0
anyLabelN = 0
newWritten = []
notWritten = []

dataFile = r"D:\IITD\CoS-data\processed_data\parsed_combined.json" 
oldData = data = courses = abbr = None
with open(dataFile, encoding='utf-8') as f:
    data = json.load(f)
with open(r"D:\IITD\CoS-data\processed_data\courses_combined.json", encoding='utf-8') as f:
    courses = json.load(f)
with open(r"D:\IITD\CoS-data\raw\abbr.json") as f:
    abbr = json.load(f)
with open(r'D:\IITD\CoS-data\processed_data\parsed_pre.json', encoding='utf-8') as f:
    oldData = json.load(f)
    

def doGenTree(course) -> bool:
    pre = data[course]
    if not pre:
        return False
    return True

def gen(course) -> str:
    id = newID()
    pre = data[course]
    head = f'{course}-{id}'
    
    str = "flowchart TD\n"
    str += f'{head}[{course}]\n'
    if 'COURSE' in pre:
        str += "".join(genCourseTree(head, pre['COURSE'], id))
    elif 'AND' in pre:
        str += "".join(genAndTree(head, pre['AND'], id))
    elif 'OR' in pre:
        str += genOrTree(head, pre['OR'])
    
    str += '''\nclassDef empty height:17px, fill:transparent, stroke:transparent;
classDef trueEmpty height:0px, width:0px;'''  
    return str
    
def newID() -> int:
    global subGraphID
    subGraphID += 1
    return subGraphID  

def genAndTree(head, ands, id) -> set[str]:
    graph = set()
    
    for dict in ands:
        found = 0
        if 'COURSE' in dict:
            course = dict['COURSE']
            graph.update(genCourseTree(head, course, id))
            found += 1
        elif 'OR' in dict:
            graph.add(genOrTree(head, dict['OR']))
            found += 1
        elif 'AND' in dict:
            raise ValueError(f'Nested AND not allowed. head: {head}, ands: {ands}')
        else:
            raise ValueError('Empty And. head: {head}')
        if found != 1:
            raise ValueError(f'Invalid data for and: {ands} with head: {head}\n'
                             'Multiple Parameters found' + str(dict))
    return graph
            
def genOrTree(head, ors) -> str:
    '''uses given subgraph ID'''
    thisId = newID()
    orHead = f'Or{thisId}'
    str = f'{head} --- {orHead}[Any one of]:::empty\n'
    
    for dict in ors:
        found = 0
        pathID = newID()
        if 'COURSE' in dict:
            course = dict['COURSE']
            str += "".join(genCourseTree(orHead, course, pathID, dotted = True))
            found += 1
        elif 'AND' in dict:
            andHead = f'and{pathID}'
            str += f'{orHead} -.- {andHead}[ ]:::trueEmpty\n'
            str += "".join(genAndTree(andHead, dict['AND'], pathID))
            found += 1
        elif 'OR' in dict:
            raise ValueError(f'Nested OR not allowed. head: {head}, ors: {ors}')
        else:
            raise ValueError('Empty Or. head: {head}')
        if found != 1:
            raise ValueError(f'Invalid data for or: {ors} with head: {head}\n'
                             'Multiple Parameters found' + str(dict))
    return str
             
def genCourseTree(head, course, subID, dotted = False) -> set[str]:
    newHead = f'{course}-{subID}'
    graph = {f"{head} --> {newHead}[{course}]\n"} if not dotted else {f"{head} -.-> {newHead}[{course}]\n"}
    
    ecRegex = re.compile(r'EC\s?\d{2,3}')
    if ecRegex.match(course) or course == "NLN100" or course == "NLN101":
        return graph
    
    if course not in data:
        raise ZeroDivisionError(f'Course not found: {course}')
    pre = data[course]
    
    found = 0
    
    if 'COURSE' in pre:
        graph.update(genCourseTree(newHead, pre['COURSE'], subID))
        found += 1
    elif 'AND' in pre:
        graph.update(genAndTree(newHead, pre['AND'], subID))
        found += 1
    elif 'OR' in pre:
        graph.add(genOrTree(newHead, pre['OR']))
        found += 1
    elif not pre:
        found += 1
    else:
        raise ValueError('Invalid data for course: ' + course + ' with head: ' + head + "\n"
                         'No valid parameter found' + str(pre))
    
    if found != 1:
        raise ValueError('Invalid data for course: ' + course + ' with head: ' + head + '\n'
                         'Multiple Parameters found' + str(pre))
    return graph
      
def main():
    for course in data:
        if not doGenTree(course):
            continue
        try:
            graph = gen(course)
            path = getFilePath(course)
            with open(path, 'r', encoding="utf-8") as f:
                content = f.read()
                if '### Prerequisite Tree' in content:
                    continue
            
            with open(path, 'a') as f:
                f.write('\n\n### Prerequisite Tree\n')
                f.write('\n```mermaid\n' + graph + '\n```')
            newWritten.append(course)
        except ZeroDivisionError as e:
            notWritten.append(course)
            
    print('Newly Written:', newWritten)
    print('Not Written:', notWritten)

def getFilePath(course):
    c = courses[course]
    dep = c['department']
    dir = abbr[dep]
    return f"D:\Code\Website\quartz\content\{dir}\{course}.md"


if __name__ == '__main__':
    main()