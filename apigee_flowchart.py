import  flowgiston as flg

import ast
flowjson="""{
  'Proxy': {
    'PreFlow': {
      'Request': [
        {
          'AM-OverrideConfig': None
        },
        {
          'KVM-Api-Config': None
        },
        {
          'FC-VerifyApikey-or-OAuth-LimitTraffic': None
        },
        {
          'AM-SetContentType-JSON': '(request.content!=null) and (request.content!="")'
        },
        {
          'JTP-JSONThreatChecks': '(request.content!=null) and (request.content!="")'
        },
        {
          'EV-ExtractNonQueryRequestVars': '(request.content!=null) and (request.content!="")'
        },
        {
          'EV-ExtractQueryRequestVars': '(request.content=null) or (request.content="")'
        }
      ],
      'Response': [
        
      ]
    },
    'PostFlow': {
      'Request': [
        
      ],
      'Response': [
        {
          'FC-Post-Log-Message': None
        }
      ]
    },
    'Flows': {
      'update-account-id-quote-id-details': {
        'Condition': '(proxy.pathsuffix MatchesPath "/quotes/*") and (request.verb = "PATCH")',
        'Request': [
          {
            'AM-400-InvalidQuoteUpdate': '(api.request.quoteupdate = null) or (api.request.quoteupdate = "")'
          },
          {
            'RF-400-BadRequest': '(api.request.quoteupdate = null) or (api.request.quoteupdate = "")'
          }
        ],
        'Response': [
          
        ]
      },
      'create-account-id-quote-id-action': {
        'Condition': '(proxy.pathsuffix MatchesPath "/quotes/*/actions") and (request.verb = "POST")',
        'Request': [
          {
            'JS-ValidateActionName': None
          },
          {
            'AM-400-InvalidActionError': '(api.quote.action.isvalid != "true")'
          },
          {
            'RF-400-BadRequest': '(api.quote.action.isvalid != "true")'
          }
        ],
        'Response': [
          
        ]
      },
      'get-accounts-account-id-quotes-quote-id-field-service-execution-details': {
        'Condition': '(proxy.pathsuffix MatchesPath "/quotes/*/work-orders") and (request.verb = "GET")',
        'Request': [
          {
            'AM-400-MissingQuoteItemId': '(request.queryparam.quote-item-ids = null) or (request.queryparam.quote-item-ids  = "")'
          },
          {
            'RF-400-BadRequest': '(request.queryparam.quote-item-ids = null) or (request.queryparam.quote-item-ids  = "")'
          }
        ],
        'Response': [
          
        ]
      },
      'Options': {
        'Condition': '(request.verb = "OPTIONS")',
        'Request': [
          
        ],
        'Response': [
          {
            'AM-AddCORS': None
          }
        ]
      }
    }
  },
  'Target': {
    'PreFlow': {
      'Request': [
        {
          'KVM-ESB-QuoteConfig': None
        },
        {
          'AM-400-UnknownBackend': '(api.request.targetinfo.quotation.system != null) and (api.request.targetinfo.quotation.system != "")'
        },
        {
          'RF-400-BadRequest': '(api.request.targetinfo.quotation.system != null) and (api.request.targetinfo.quotation.system != "")'
        },
        {
          'AM-401-Token-Required-For-App': '(api.isApikeyVerified = "true")'
        },
        {
          'RF-401-MissingAuthHeader': '(api.isApikeyVerified = "true")'
        }
      ],
      'Response': [
        {
          'AM-AddCORS': None
        }
      ]
    },
    'PostFlow': {
      'Request': [
        
      ],
      'Response': [
        
      ]
    },
    'Flows': {
      'create-quote': {
        'Condition': '(proxy.pathsuffix MatchesPath "/quotes") and (request.verb = "POST")',
        'Request': [
          
        ],
        'Response': [
          
        ]
      },
      'unsupportedFlow': {
        'Request': [
          {
            'AM-403-Forbidden': None
          },
          {
            'RF-403-Forbidden': None
          }
        ],
        'Response': [
          
        ]
      }
    }
  }
}"""
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
    diag1 = diag1.edge(chart.Note.node(proxyPreReq),  label=flowdict["Target"]["Flows"][proxyPreReq]["Condition"])
        
        
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
