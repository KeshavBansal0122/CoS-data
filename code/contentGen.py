import json, re
import os

courses: dict[str, dict] = None
abbr: dict[str, dict] = None
with open(r"D:\IITD\CoS-data\processed_data\courses_combined.json", encoding='utf-8') as f:
    courses = json.load(f)
with open(r"D:\IITD\CoS-data\raw\abbr.json", encoding='utf=8') as f:
    abbr = json.load(f)
outDir = r"D:\Code\Website\quartz\content"
courseRegex = re.compile("[A-Z]{3}\d{3}")

def getWikilink(courseNo):
    global courses, abbr
    if courseNo in courses:
        dep = courses[courseNo]['department']
        dirName = abbr[dep]
        return f"[[/{dirName}/{courseNo}|{courseNo}]]"
    else:
        print(f"Course {courseNo} not found")
        return f'[[/{courseNo}|{courseNo}]]'

def writeFile(f, course):
    global courseRegex
    out = f'''---
title: \"{course['name']}\"
---
**Credits:** {course['credits']}

'''
    pre: str = course['pre']
    if pre:
        pre = courseRegex.sub(lambda x: getWikilink(x.group(0)), pre)
        out += f"**Prerequisites:** {pre}\n\n"
    
    overlap = course['overlap']
    if overlap:
        out += f"**Overlaps with:** {overlap}\n\n"
    
    allocPref = course['allocPref']
    if allocPref:
        out += f"**Allocation Preference:** {allocPref}\n\n"
    
    if "note" in course and course['note']:
        out += f"**Note:** {course['note']}\n\n"
        
    out += "#### Description\n"
    des = course['description']
    if des:
        out += des
    else:
        out += "No description available."
    
    f.write(out)

def writeDepIndex(dep, courses):
    global abbr
    courses.sort(key=lambda x: x['code'])
    out = f'''---
title: {dep}
---'''
    oldName = ""
    for course in courses:
        code = course['code']
        c_name = code[:3]
        if c_name != oldName:
            out += f"\n\n## {c_name}  \n"
            oldName = c_name
        out += f"[[{code} |{course['name']}]]  \n"
        
    index_file_path = f"{outDir}/{abbr[dep]}/index.md"
    directory = os.path.dirname(index_file_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(index_file_path, 'w+', encoding='utf-8') as f:
        f.write(out)
        
def getFilePath(course):
    global abbr
    dep = course['department']
    dir = abbr[dep]
    return f"{outDir}\{dir}\{course['code']}.md"

def main():
    global courses
    depFile = {}
    i = 0
    for courseNo, course in courses.items():
        dep = course['department']
        depFile.setdefault(dep, []).append(course)
        
        file_path = getFilePath(course)
        directory = os.path.dirname(file_path)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(file_path, 'w+', encoding='utf-8') as f:
            writeFile(f, course)
        i += 1
    
    print(f"Written {i} files")
    i = 0
    for dep, courses in depFile.items():
        writeDepIndex(dep, courses)
        i += 1
    print(f"Written {i} department index files")
    
if __name__ == "__main__":
    main()