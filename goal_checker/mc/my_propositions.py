"""
------------------------------------------------------------------
File:   my_propositions.py
Author: Joaquín Ezpeleta (Univ. of Zaragoza, Spain)
Date:   June 2025
        Model checker based on the DLTL and algorithm in the following reference:
        J. M. Couvreur, J. Ezpeleta
        "A Linear Temporal Logic Model Checking Method over Finite Words with Correlated Transition Attributes" 
        Procs. of the 7th International Symposium on Data-driven Process Discovery and Analysis (SIMPDA 2017),
        Neuchâtel, Switzerland, December 6-8, 2017, ISSN: 1613-0073, Lecture Notes in Business Information Processing,
        Vol. 340, Springer, Paolo Ceravolo, Maurice van Keulen and Kilian Stoffel (Eds.), 2019 
Coms:   Prototype for TACAS artifacts
        This file is imported by default. Users can write here all the propositions
        (functions evaluated over one or more sates and return a true or false)
------------------------------------------------------------------
"""

import log_handling
atribNames = log_handling.mapIndexNonAtomic


def doble(x):
    return x * 2
# ---------------------------------------
def suma(x, y):
    return x + y
# ---------------------------------------
def quote(s):
    return '"' + s + '"'
# ---------------------------------------
#x.("(x)PROP.IN_DIC(x[p],'b',3)")
def IN_DIC(dicc, k, v):
    if k in dicc:
        return dicc[k] == v
    else:
        return False


#x.("(x)PROP.IN_DIC_2(x,p,'b',22)")
def IN_DIC_2(event, posDir, k, v):
    if k in event[posDir]:
        return event[posDir][k] == v
    else:
        return False
# ---------------------------------------
#x.(F y.("(x,y)PROP.TS_IG(x,y)"))
#x.(X y.("(x,y)PROP.TS_IG(x,y)"))
def TS_IG(x, y):
    V = atribNames['mess']
    return x[V] == y[V]
# ---------------------------------------
# F x.(true & "(x)PROP.SPARQL_old(x['Details_g'])")
def SPARQL_old(g):
    # for s, p, o in g:
    #     print(f"{s} -- {p} --> {o}")

    query = """
        ASK
            WHERE {
               ?s <http://snomed.info/sct/duration> "Ongoing".
            }
            """
    print(f"query: '{query}'")
    return g.query(query).askAnswer
# ---------------------------------------
def SP_HAS_VALUE(g, predicado, objeto):
    # for s, p, o in g:
    #     print(f"{s} -- {p} --> {o}")
    query = """
                ASK
                    WHERE {
                       ?s <http://snomed.info/sct/%s> "%s".
                    }
            """%(predicado, objeto)
    # print(f"query: '{query}'")
    return g.query(query).askAnswer
# ---------------------------------------
# S1=?s snomed:duration "Ongoing" .
#   ?s ex:hasSeverity ?severityValue .
#   FILTER (STRSTARTS(?severityValue, 'H')) . 


# duration --> "Ongoing".
# F x.(true & "(x)FN.SP_HAS_VALUE(x['Details_g'],'duration','Ongoing')")

# closureReason --> "Condition_resolved"
# ac_Patient_Login & F x.("(x)FN.SP_HAS_VALUE(x['Details_g'],'closureReason','Condition_resolved')")

# _SET$ ?objs 'Condition_resolved','Ongoing'

# ac_Patient_Login & F x.("(x)FN.SP_HAS_VALUE(x['Details_g'],'closureReason',?objs)")

