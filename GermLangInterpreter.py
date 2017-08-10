#!/usr/bin/env python

#############################################################
# GermLangInterpreter.py - A basic DIY programming language #
# (c) gdifiore 2017                                         #
#############################################################

from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data

def lex(filecontents):
    tok = ""
    state = 0
    isexpr = 0
    varStarted = 0
    var = ""
    string = ""
    expr = ""
    n = ""
    filecontents = list(filecontents)
    for char in filecontents:
        tok += char
        if tok == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""    
                varStarted = 0            
            tok = ""
        elif tok == "=" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""    
                varStarted = 0    
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
            else:
                tokens.append("EQUALS")
            tok = ""
        elif tok == "$" and state == 0:
            varStarted = 1
            var += tok
            tok = ""
        elif varStarted == 1:
            if tok == "<" or tok == ">":
                if var != "":
                    tokens.append("VAR:" + var)
                    var = ""    
                    varStarted = 0   
            tok = ""
            var += tok
            tok = ""
        elif tok == "print" or tok == "PRINT":
            tokens.append("PRINT")
            tok = ""
        elif tok == "input" or tok == "INPUT":
            tokens.append("INPUT")
            tok = ""
        elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\t":
            tok = ""
        elif tok == "\"" or tok == " \"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0    
                tok = ""    
        elif state == 1:
            string += tok
            tok = ""
    #print(tokens)
    #return ''
    return tokens
    

def evalExpression(expr):
    return eval(expr) 

def doPRINT(toPRINT):
    if(toPRINT[0:6] == "STRING"):
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif(toPRINT[0:3] == "NUM"):
        toPRINT = toPRINT[4:]
    elif(toPRINT[0:4] == "EXPR"):
        toPRINT = evalExpression(toPRINT[5:])       
    print(toPRINT)

def doAssign(varName, varValue):
        symbols[varName[4:]] = varValue

def getVariable(varName):
    varName = varName[4:]
    if varName in symbols:
        return symbols[varName]
    else:
        return "Variable Error: UNDEFINED VARIABLE"
        exit()

def getInput(STRING, varname):
    i = input(STRING[1:-1] + " ")
    symbols[varname] = "STRING:\"" + i + "\""

def parse(toks):
    i = 0
    while(i < len(toks)):
        if toks[i] == "ENDIF":
            i+=1
        elif toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
            if toks[i+1][0:6] == "STRING":
                doPRINT(toks[i+1])
            elif toks[i+1][0:3] == "NUM":
                doPRINT(toks[i+1])
            elif toks[i+1][0:4] == "EXPR":
                doPRINT(toks[i+1])          
            elif toks[i+1][0:3] == "VAR":
                doPRINT(getVariable(toks[i+1]))      
            i+=2
        elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            if toks[i+2][0:6] == "STRING":
                doAssign(toks[i],toks[i+2])
            elif toks[i+2][0:3] == "NUM":
                doAssign(toks[i],toks[i+2])
            elif toks[i+2][0:4] == "EXPR":
                doAssign(toks[i],"NUM:" + str(evalExpression(toks[i+2][5:])))  
            elif toks[i+2][0:3] == "VAR":
                doAssign(toks[i],getVariable(toks[i+2]))
            i+=3
        elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
            getInput(toks[i+1][7:], toks[i+2][4:])
            i+=3

    #print(symbols)
            
def run():
    data = open_file(argv[1])
    toks = lex(data)
    parse(toks)
            
run()
