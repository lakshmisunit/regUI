# from test_regCodeGen import regs
# module header common inserts
REGWIDTH = 32
ADRWIDTH = 10
N = 'NAME'

T = 'TYPE'
I = 'input'
O = 'output'
X = 'inout'
Y = 'wire'
G = 'reg'

A = 'ASSIGN'
C = 'CONCAT'
L = 'SPLIT'
Z = 'NONE'
M = 'MUXIN'

W = 'WIDTH'
S = 'SIGNAL'
R = 'ISREG'
COMMON_PINS = {
  'APB': [
    {T: I, W: 1,          N: 'clock',   },
    {T: I, W: 1,          N: 'reset',   },
    {T: I, W: ADRWIDTH,   N: 'addr',    },
    # {T: I, W: 1,          N: 'PSEL',  },
    {T: I, W: 1,          N: 'enable',  },
    {T: I, W: 1,          N: 'wr',      },
    {T: I, W: REGWIDTH,   N: 'wdata',   },
    {T: I, W: 1,          N: 'rd',      },
    {T: O, W: 1,          N: 'ready',   },
    {T: O, W: REGWIDTH,   N: 'rdata',   }
  ],
  'TYPE-1': [ 
    {T: Z, W: '1 ', N: 'clock', S: 'clock'},
    {T: Z, W: '1 ', N: 'reset', S: 'reset'},
  ]
}

CLOCK = {
  'APB': 'APBSlaveClock'
}

RESET = {
  'APB': 'APBSlaveReset'
}

CELL_PINS = {
  'WR': [
    { R: 0, T: Y, W: 1, N: 'enable__',    A: Z},
    { R: 1, T: G, W: REGWIDTH, N: 'D__fromSW__', A: C},
    { R: 0, T: O, W: REGWIDTH, N: 'Q__toHW__',   A: L}
  ],
  'RO': [
    { R: 0, T: Y, W: 1, N: 'enable__',    A: Z},
    { R: 0, T: I, W: REGWIDTH, N: 'D__fromHW__', A: C},
    { R: 1, T: Y, W: REGWIDTH, N: 'Q__toSW__',   A: Z}
  ],
  'WR12C': [
    { R: 0, T: Y, W: 1, N: 'enable__',      A: Z},
    { R: 0, T: I, W: REGWIDTH, N: 'D__fromHW__',   A: C},
    { R: 0, T: Y, W: REGWIDTH, N: 'Q__toSW__',     A: Z},
    { R: 1, T: G, W: REGWIDTH, N: 'WR1__fromSW__', A: C},
    { R: 0, T: O, W: REGWIDTH, N: 'CLEAR__toHW__', A: L}
  ],
  'HWC': [
    { R: 0, T: Y, W: 1, N: 'enable__',        A: Z},
    { R: 0, T: G, W: REGWIDTH, N: 'D__fromSW__',     A: C},
    { R: 0, T: O, W: REGWIDTH, N: 'Q__toHW__',       A: L},
    { R: 0, T: I, W: REGWIDTH, N: 'CLEAR__fromHW__', A: C}
  ],
  'HWCI': [
    { R: 0, T: Y, W: 1, N: 'enable__',        A: Z},
    { R: 0, T: G, W: REGWIDTH, N: 'D__fromSW__',     A: C},
    { R: 0, T: O, W: REGWIDTH, N: 'Q__toHW__',       A: L},
    { R: 0, T: I, W: REGWIDTH, N: 'CLEAR__fromHW__', A: C}
  ],
  'RSVD': [] 
}

def search(collection, item, property, value):
  if (item not in collection):
    return None
  x = collection[item]
  r = []
  for y in x:
    if (y[property] == value):
      r.append(y)
  return r

def collect(collection, property, suffix):
  x = []
  for y in collection:
    if (property in y):
      x.append(y[property] + suffix)
  return x 

def getCmnIOList(t):
  return collect(COMMON_PINS[t], N, '')

def getCmnIODecls(t):
  ioListRaw = COMMON_PINS[t]
  ioList = []
  for i in ioListRaw:
    d = '  {0} '.format(i[T])
    if (i[W] > 1):
      d = d + '[{0}:0] '.format(i[W]-1)
    d = d + i[N] + ';'
    ioList.append(d)
    if(i[T] == O):
      d = '  reg '
      if (i[W] > 1):
        d = d + '[{0}:0] '.format(i[W]-1)
      d = d + i[N] + ';'
      ioList.append(d)
  return ioList

# collection, type, reg-name, field-array
def getIOList(c, t, r, f):
  if(t == "read-only"):
    t = 'RO'
  if(t == "read-write" or t == "write-only"):
    t = 'WR'
  ioList = []
  for field in f:
    ioList = ioList + getIOList_internal(c,t,r+'__'+field.fldName)
  return ioList

def getIOList_internal(c, t, s):
  ioListRaw = search(c,t,T,I) + search(c,t,T,O)
  ioList = collect(ioListRaw, N, s)
  return ioList

def getIODecls(c, t, r, f):
  decls = []
  for field in f:
    decls = decls + getIODecls_internal (c,t,r+'__'+field.fldName,field.fldWidth)
  return decls

def getIODecls_internal(c, t, s, z):
  decls = []
  print(f"t value inside the regcode gen is {t}")
  if(t == "read-only"):
    t = 'RO'
  if(t == "read-write" or t == "write-only"):
    t = 'WR'

  ioList = search(c,t,T,I) + search(c,t,T,O)
  for i in ioList:
    d = '  ' + i[T] + ' '
    print(z)
    if (z > 1): 
      d = d + ' [{0}:0] '.format(z-1)
    d = d + i[N] + s + ';'
    decls.append(d)
    if (i[R]):
      d = '  reg '
    else:
      d = '  wire '
    if (z > 1): 
      d = d + ' [{0}:0] '.format(z-1)
    d = d + i[N] + s + ';'
    decls.append(d)
  return decls

def getLocalVars(r):
  localVars = []
  for reg in r:
    localVars.append(getLocalVars_internal(CELL_PINS, reg.regType, reg.regName, reg.regWidth))
  return localVars

# type, reg, size
def getLocalVars_internal(c, t, s, z):
  print('Working {0}'.format(s))
  if(t == "read-only"):
    t = 'RO'
  if(t == "read-write" or t == "write-only"):
    t = 'WR'
  varList = search(c,t,T,Y) + search(c,t,T,G)
  varDecls = []
  for i in varList:
    v = '  ' + i[T]
    if (i[W] > 1):
      v = v + ' [{0}:0] '.format(i[W]-1)
    v = v + ' ' + i[N] + s + ';'
    varDecls.append(v)
    if (t == 'WR' or t == 'HWC' or t == 'HWCI'):
      v = '  wire [{0}:0] Q__toHW__{1};'.format(z-1, s)
      if not (v in varDecls):
        varDecls.append(v)
    if (t == 'HWC' or t == 'HWCI'):
      v = '  wire [{0}:0] CLEAR__fromHW__{1};'.format(z-1, s)
      if not (v in varDecls):
        varDecls.append(v)
    if (t == 'RO'):
      v = '  wire [{0}:0] D__fromHW__{1};'.format(z-1, s)
      if not (v in varDecls):
        varDecls.append(v)
    # print(varDecls)
  return varDecls

def getInstStr(r):
  instStr = []
  for reg in r:
    x = '{32\'d0'
    for f in reg.fields:
      x = x + ', ' + f.resetVal
      # print(f.resetVal)
    x = x + '}'
    instStr.append(getInstStr_internal(CELL_PINS, reg.regType, reg.regName, x))
  return instStr
  
def getInstStr_internal(c, t, r, v):
  if(t == "read-only"):
    t = 'RO'
  if(t == "read-write" or t == "write-only"):
    t = 'WR'
  instStr = t + ' #({0},{1}) '.format(REGWIDTH, v) + r + '('
  cmnSigList = COMMON_PINS['TYPE-1']
  n = collect(cmnSigList, N, '')
  q = collect(cmnSigList, S, '')
  for i in range(len(n)):
    instStr = instStr + '.{0}({1}), '.format(n[i], q[i])
  n = collect(c[t], N, '')
  for i in range(len(n)):
    instStr = instStr + '.{0}({1}{2})'.format(n[i], n[i], r)
    if (i < len(n)-1):
      instStr = instStr + ', '
  instStr = instStr + ');\n' 
  return instStr

# reg name, signal array
def getAssignStr(r):
  str = []
  for reg in r:
    t = reg.regType
    n = reg.regName
    s = reg.fields
    if (t == 'WR'):
      str.append(getAssignStr_WR(n, s))
    elif (t == 'RO'):
      str.append(getAssignStr_RO(n, s))
    elif (t == 'WR12C'):
      return getAssignStr_WR12C(n, s)
    elif (t == 'HWC' or t == 'HWCI'):
      str.append(getAssignStr_HWC(n, s))
  return str

def getAssignStr_WR(n, s):
  s.reverse()
  assignStr = 'assign {'
  for i in range(len(s)):
    assignStr = assignStr + 'Q__toHW__{0}__{1}'.format(n,s[i].fldName)
    if (i < len(s)-1):
      assignStr = assignStr + ', '
  assignStr = assignStr + '} = '+ 'Q__toHW__{0};'.format(n)
  return assignStr

def getAssignStr_RO(n, s):
  s.reverse()
  assignStr = 'assign D__fromHW__{0} = '.format(n)
  assignStr = assignStr + '{32\'d0, '
  for i in range(len(s)):
    assignStr = assignStr + 'D__fromHW__{0}__{1}'.format(n,s[i].fldName)
    if (i < len(s)-1):
      assignStr = assignStr + ', '
  assignStr = assignStr + '};'
  return assignStr

def getAssignStr_WR12C(n, s):
  s.reverse()
  assignStr = 'assign D__fromHW__{0} = '.format(n)
  assignStr = assignStr + '{32\'d0, '
  for i in range(len(s)):
    assignStr = assignStr + 'Q__toSW__{0}__{1}'.format(n,s[i].fldName)
    if (i < len(s)-1):
      assignStr = assignStr + ', '
  assignStr = assignStr + '};\n'
  assignStr = assignStr + 'assign Q__toSW__{0} = D__fromHW__{0};\n'.format(n)
  assignStr = assignStr + 'assign CLEAR__toHW__{0} = D__fromSW__{0};'.format(n)
  return assignStr

def getAssignStr_HWC(n, s):
  s.reverse()
  a1 = 'assign {'
  a2 = 'assign CLEAR__fromHW__{0} = '.format(n) + '{32\'d0, '
  for i in range(len(s)):
    a1 = a1 + 'Q__toHW__{0}__{1}'.format(n,s[i].fldName)
    a2 = a2 + 'CLEAR__fromHW__{0}__{1}'.format(n,s[i].fldName)
    if (i < len(s)-1):
      a1 = a1 + ', '
      a2 = a2 + ', '
  a1 = a1 + '} = ' + 'Q__toHW__{0};\n'.format(n)
  a2 = a2 + '};'
  assignStr = a1 + a2
  return assignStr

##########################################################################
################ PRINT ROUTINES ##########################################
##########################################################################

# output file handle, block name, common-collection, type, reg-array
def printModuleStatement(o, n, c, r):
  o.write('/* *************************************************\n')
  o.write('// auto-generated by RegMagic software.  Do not edit\n')
  o.write('************************************************* */\n')
  o.write('module {0} (\n'.format(n))
  s = getCmnIOList('APB')
  for sigs in s:
    o.write('{0}, '.format(sigs))
  for i in range(len(r)):
    x = getIOList(c,r[i].regType,r[i].regName,r[i].fields)
    o.write(', '.join(x))
    if (i < len(r)-1):
      o.write(', ')
  o.write(');\n')

def printIODecls(o,c,r):
  o.write('///////////////////////////////// IO DECLARAIONS  //////////////////////////////////////////\n')
  for s in getCmnIODecls('APB'):
    o.write(s+'\n')
  for reg in r:
    for s in getIODecls(c,reg.regType, reg.regName, reg.fields):
      o.write(s+'\n')

def printLocalVars(o, r):
  o.write('///////////////////////////////// LOCAL VARIABLES  //////////////////////////////////////////\n')
  for s in getLocalVars(r):
    o.write('\n'.join(s))
    o.write('\n')

# def printRdWrControllers(o, c, t):
#   o.write('///////////////////////////////// LOCAL WR/RD ENs  //////////////////////////////////////////\n')
#   o.write('  wire doWrite, doRead;\n')
#   o.write('  assign doWrite = PWRITE & PENABLE;\n')
#   o.write('  assign doRead = !PWRITE & PENABLE;\n')

def printInstStr(o, r):
  o.write('///////////////////////////////// REG INSTANTIATION //////////////////////////////////////////\n')
  for s in getInstStr(r):
    o.write(s)

def printAssignStr(o, r):
  o.write('///////////////////////////////// ASSIGN STATEMENTS //////////////////////////////////////////\n')
  for s in getAssignStr(r):
    o.write(s + '\n')
  o.write('\n')

def printEnables(o, r):
  o.write('////////////////////////////////// REG WR ROUTING ///////////////////////////////////////////\n')
  o.write('// ENABLES\n')
  n = []
  b = []
  for reg in r:
    n.append(reg.regName)
    b.append(reg.regOffset)
  printEnables_internal(o, n, b)

def printEnables_internal(o, n, b): # n and b are arrays
  for i in range(len(n)):
    o.write('assign enable__{0} = (wr && enable && {1} == addr);\n'.format(n[i], b[i]))

def printInputDataRouting(o, r):
  o.write('// DATA ROUTING\n')
  printReadFunction(o, r)
  for reg in r:
    printWriting(o, reg.regName, reg.regType)
  # printReading (o, reg.regName, reg.regType)
  printReading (o)

def getRegOutputName(r):
  if(r.regType == 'WR'):
    return ('Q__toHW__{0}'.format(r.regName))
  if(r.regType == 'RO' or r.regType == 'WR12C'):
    return ('Q__toSW__{0}'.format(r.regName))
  if(r.regType == 'HWC' or r.regType == 'HWCI'):
    return ('Q__toHW__{0}'.format(r.regName))

def printReadFunction(o, r):
  o.write('function [31:0] readData(input [9:0] A);\n')
  o.write('  case (A)\n')
  for reg in r:
    regOutput = getRegOutputName(reg)
    o.write('    {0}: readData = {1};\n'.format(reg.regOffset, regOutput))
  o.write('    default: readData = 32\'d0;')
  o.write('  endcase\n')
  o.write('endfunction\n')

def printRWLogic(o,t):
  o.write('// logic for read-write operation //')

def printWriting(o, n, t):
  if(t == 'WR' or t == 'HWC' or t == 'HWCI'):
    o.write('always @(*) begin\n'.format(n))  
    o.write('  if(enable__{0} && wr) D__fromSW__{0} = wdata;\n'.format(n))
    o.write('  else D__fromSW__{0} = 0;\n'.format(n))
    o.write('end\n')  
  # elif(t == 'RO' or t == 'WR12C'):

def printReading(o):
  o.write('reg callRead;\n')
  o.write('always @(posedge clock or negedge reset) begin\n')
  o.write('  if (reset == 1\'b0) begin\n')
  o.write('    rdata <= 0;\n')
  o.write('    ready <= 0;\n')
  o.write('    callRead <= 0;\n')
  o.write('  end\n')
  o.write('  else begin\n')
  o.write('    if (callRead) begin\n')
  o.write('      rdata <= readData(addr);\n')
  o.write('      ready <= 1;\n')
  o.write('      callRead <= 0;\n')
  o.write('    end\n')
  o.write('    else begin\n')
  o.write('      ready <= 0;\n')
  o.write('    end\n')
  o.write('    if (rd && enable) begin\n')
  o.write('      callRead <= 1;\n')
  o.write('    end\n')
  o.write('    if (wr && enable) begin\n')
  o.write('      ready <= 1;\n')
  o.write('    end\n')
  o.write('  end\n')
  o.write('end\n')

def printEndModule(o):
  o.write('endmodule\n')

def processRegBlock (a, m, regs):
  printModuleStatement(a, m, CELL_PINS, regs)
  printIODecls(a, CELL_PINS, regs)
  printLocalVars(a, regs)
  # printRdWrControllers(a, COMMON_PINS, 'APB')
  printAssignStr(a, regs)
  printEnables(a, regs)
  printInputDataRouting(a, regs)
  printInstStr(a, regs)
  printEndModule(a)

def processRegMacros(a, regs):
  a.write('//////////////////////////////////////////////////////////////\n')
  a.write('// Auto-generated by RegMagic software.  Do not edit this file\n')
  a.write('//////////////////////////////////////////////////////////////\n')
  for r in regs:
    for m in r.macros:
      a.write(m)

def processRegMacros_D(a, regs):
  a.write('//////////////////////////////////////////////////////////////\n')
  a.write('// Auto-generated by RegMagic software.  Do not edit this file\n')
  a.write('//////////////////////////////////////////////////////////////\n')
  for r in regs:
    print(regs)
    print(r.cmacros)
    for m in r.cmacros:
      print(m)
      a.write(m)
# with open('out.v', 'w') as a:
#   processRegBlock (a, regs)
# a.close()
