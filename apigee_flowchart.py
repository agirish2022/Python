import  flowgiston as flg

import ast
flowjson="""output of apigee_flow.py"""
flowdict = ast.literal_eval(flowjson)

Base = flg.flowgiston_base(fillcolor= "lightblue")

charcoal= '#264653ff'
persGreen=  '#2a9d8fff'
orYellCray =  '#e9c46aff'
sandyBrown= '#f4a261ff'
burntSienna= '#e76f51ff'

class Note(Base):
    fillcolor= "lightyellow"
    style = "filled, dashed"
    shape = "box"
    fontname = "courier"

class Intro(Base):
    fillcolor= '#264653'
    fontcolor = "white"
    style = "filled, solid"
    shape = "box"
    fontname = "courier"

class EstArte(Base):
    fillcolor= '#2a9d8f55'
    style = "filled, solid"
    shape = "box"
    fontname = "courier"

class Metodo(Base):
    fillcolor= '#e9c46aff'
    style = "filled, solid"
    shape = "box"
    fontname = "courier"

class Ana(Base):
    fillcolor= "#f4a261ff"
    style = "filled, solid"
    shape = "box"
    fontname = "courier"

class Conc(Base):
    fillcolor= '#e76f51ff'
    style = "filled, solid"
    shape = "box"
    fontname = "courier"
tex_intro_req = """Beggining of Request"""
tex_intro_res = """Beggining of Response"""
#text_conc = """Conclusão"""
chart = flg.FlowgistonChart(Base)

diag1 = chart.Intro.node(tex_intro_req)

#Request
diag1 = diag1.edge(chart.Intro.node("Proxy PreFlow")) 

for proxyPreReq in flowdict["Proxy"]["PreFlow"]["Request"]:
    if list(proxyPreReq.values())[0] == None:
        diag1 = diag1.edge(chart.EstArte.node(list(proxyPreReq.keys())[0]))
    else :
        diag1 = diag1.edge(chart.Note.node(list(proxyPreReq.keys())[0]),  label=list(proxyPreReq.values())[0])

diag1 = diag1.edge(chart.Intro.node("Proxy PostFlow"))        
for proxyPreReq in flowdict["Proxy"]["PostFlow"]["Request"]:
    if list(proxyPreReq.values())[0] == None:
        diag1 = diag1.edge(chart.EstArte.node(list(proxyPreReq.keys())[0]))
    else :
        diag1 = diag1.edge(chart.Note.node(list(proxyPreReq.keys())[0]),  label=list(proxyPreReq.values())[0])

#Flows

diag1 = diag1.edge(chart.Intro.node("Conditional Flows"))

for proxyPreReq in flowdict["Proxy"]["Flows"]:
    diag1 = diag1.edge(chart.Note.node(proxyPreReq),  label=flowdict["Proxy"]["Flows"][proxyPreReq]["Condition"])


diag1 = diag1.edge(chart.Intro.node("Target PreFlow"))        
for proxyPreReq in flowdict["Target"]["PreFlow"]["Request"]:
    if list(proxyPreReq.values())[0] == None:
        diag1 = diag1.edge(chart.EstArte.node(list(proxyPreReq.keys())[0]))
    else :
        diag1 = diag1.edge(chart.Note.node(list(proxyPreReq.keys())[0]),  label=list(proxyPreReq.values())[0])

diag1 = diag1.edge(chart.Intro.node("Target PostFlow"))
for proxyPreReq in flowdict["Target"]["PostFlow"]["Request"]:
    if list(proxyPreReq.values())[0] == None:
        diag1 = diag1.edge(chart.EstArte.node(list(proxyPreReq.keys())[0]))
    else :
        diag1 = diag1.edge(chart.Note.node(list(proxyPreReq.keys())[0]),  label=list(proxyPreReq.values())[0])
        

#Response
diag1 = diag1.edge(chart.Intro.node(tex_intro_res)) 

diag1 = diag1.edge(chart.Intro.node("Proxy PreFlow"))
for proxyPreReq in flowdict["Proxy"]["PreFlow"]["Response"]:
    if list(proxyPreReq.values())[0] == None:
        diag1 = diag1.edge(chart.EstArte.node(list(proxyPreReq.keys())[0]))
    else :
        diag1 = diag1.edge(chart.Note.node(list(proxyPreReq.keys())[0]),  label=list(proxyPreReq.values())[0])

diag1 = diag1.edge(chart.Intro.node("Proxy PostFlow"))        
for proxyPreReq in flowdict["Proxy"]["PostFlow"]["Response"]:
    if list(proxyPreReq.values())[0] == None:
        diag1 = diag1.edge(chart.EstArte.node(list(proxyPreReq.keys())[0]))
    else :
        diag1 = diag1.edge(chart.Note.node(list(proxyPreReq.keys())[0]),  label=list(proxyPreReq.values())[0])
        
#Flows

diag1 = diag1.edge(chart.Intro.node("Conditional Flows"))

for proxyPreReq in flowdict["Target"]["Flows"]:
    diag1 = diag1.edge(chart.Note.node(proxyPreReq))
        
        
diag1 = diag1.edge(chart.Intro.node("Target PreFlow"))         
for proxyPreReq in flowdict["Target"]["PreFlow"]["Response"]:
    if list(proxyPreReq.values())[0] == None:
        diag1 = diag1.edge(chart.EstArte.node(list(proxyPreReq.keys())[0]))
    else :
        diag1 = diag1.edge(chart.Note.node(list(proxyPreReq.keys())[0]),  label=list(proxyPreReq.values())[0])

diag1 = diag1.edge(chart.Intro.node("Target PostFlow"))        
for proxyPreReq in flowdict["Target"]["PostFlow"]["Response"]:
    if list(proxyPreReq.values())[0] == None:
        diag1 = diag1.edge(chart.EstArte.node(list(proxyPreReq.keys())[0]))
    else :
        diag1 = diag1.edge(chart.Note.node(list(proxyPreReq.keys())[0]),  label=list(proxyPreReq.values())[0])
       
chart        
