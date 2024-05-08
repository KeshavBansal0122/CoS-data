import pprint
import json

def parse_expression(expr, i):
    if expr == "FAIL":
        return {"FAIL": "FAIL"}, i
    op_index = 0
    expressions = ["", ""]
    operator = "COURSE"
    new_expression = ""
    nesting = False
    while i < len(expr):
        if nesting:
            if expr[i] != ')':
                new_expression += expr[i]
            else:
                expressions[op_index] = new_expression
                new_expression = ""
                nesting = False
        elif expr[i] == '[' or expr[i] == ' ' or expr[i] == ']':
            pass
        elif expr[i] == '|' and op_index == 0:
            op_index = 1
            operator = "OR"
        elif expr[i] == '&' and op_index == 0:
            op_index = 1
            operator = "AND"
        elif expr[i] == '(':
            nesting = True
        else:
            expressions[op_index] += expr[i]
        i += 1
    if operator == "COURSE":
        return {operator: expressions[0]}, i
    else:
        if operator == "OR":
            parsed_1, _ = parse_expression(expressions[0], 0)
            parsed_2, _ = parse_expression(expressions[1], 0)
            if list(parsed_1.keys())[0] == "OR" and list(parsed_2.keys())[0] == "OR":
                return {operator: parsed_1[operator] + parsed_2[operator]}, i
            elif list(parsed_1.keys())[0] == "OR" and list(parsed_2.keys())[0] == "COURSE":
                return {operator: parsed_1[operator] + [{"COURSE": parsed_2["COURSE"]}]}, i
            elif list(parsed_1.keys())[0] == "COURSE" and list(parsed_2.keys())[0] == "OR":
                return {operator: [{"COURSE": parsed_1["COURSE"]}] + parsed_2[operator]}, i
        elif operator == "AND":
            parsed_1, _ = parse_expression(expressions[0], 0)
            parsed_2, _ = parse_expression(expressions[1], 0)
            if list(parsed_1.keys())[0] == "AND" and list(parsed_2.keys())[0] == "AND":
                return {operator: parsed_1[operator] + parsed_2[operator]}, i
            elif list(parsed_1.keys())[0] == "AND" and list(parsed_2.keys())[0] == "COURSE":
                return {operator: parsed_1[operator] + [{"COURSE": parsed_2["COURSE"]}]}, i
            elif list(parsed_1.keys())[0] == "COURSE" and list(parsed_2.keys())[0] == "AND":
                return {operator: [{"COURSE": parsed_1["COURSE"]}] + parsed_2[operator]}, i
        return {operator: [parse_expression(expressions[0], 0)[0], parse_expression(expressions[1], 0)[0]]}, i


course_code = None
result = {}

fails = []
def parse_line(input_string):
    global course_code
    global result
    lines = input_string.split('\n')
    for line in lines:
        if line.startswith("Course:"):
            course_code = line.split(":")[1].strip()
        elif line.startswith("Pre:") and "FAIL" not in line:
            expr, _ = parse_expression(line.split(":")[1].strip(), 0)
            result[course_code] = expr
            course_code = None
        elif line.startswith("Pre:") and "FAIL" in line:
            fails.append(course_code)
            course_code = None

"""
flowchart TD
    %% A[Start] -->|COL778| B(Any One Of)
    %% B -->|COL333| C[.]
    %% C -->|COL106| D[.]
    %% D -->|COL100| E[.]
    %% B -->|COL774| F[.]
    %% F -->|MTL106| G[.]
    %% B -->|ELL784| F
    %% B -->|ELL409| H[All Of]
    %% H -->|MTL106| G[.]
    %% H -->|COL106| I[.]
    A[COL778] --- B[any one of]:::empty
    B <-.- C[COL333]
    B <-.- D[COL774]
    B -.-> E[ELL784]
    B -.-> F[ELL409]
    C --> G[COL106]
    G --> H[COL100]
    D --> I[MTL106]
    E --> I[MTL106]
    F --- J[ ]:::trueEmpty
    J --> I
    J --> G
    classDef empty height:17px, fill:transparent, stroke:transparent;
    classDef trueEmpty height:0px, width:0px;
"""


connections = []
courses = []


def gen_graph(course, prereq):
    ret_str = f"flowchart TD\n    {course}"
    '''Returns the mermaid graph for the course prereq tree.
    Returns empty string if the given course or any one of its prereq is not in the data.'''
    def graph_nodes(course):
        global connections
        global courses




with open(r"D:\IITD\CoS-data\llmParsing\parsedDataUnbracketed.txt", 'r') as f:
    for line in f.readlines():
        parse_line(line)
with open(r"D:\IITD\CoS-data\processed_data\parsed_unbracket.json", 'w') as f:
    json.dump(result, f, indent=4)
    
print(len(fails))
print(fails)