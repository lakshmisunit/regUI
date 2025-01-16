# module header common inserts
PARAM = "parameter W = 1;"
I = 'input'
O = 'output'
X = 'inout'
D = 'DIR'
W = 'WID'
N = 'NAME'
P = 'PROP' 
L = 'LINK'
C = 'LOCAL_WIRE'

COMMON_PINS = {
  'APB': [
    {D: I, W: '1 ', N: 'APBSlaveClock', P: 1, C: 0},
    {D: I, W: '1 ', N: 'APBSlaveReset', P: 1, C: 0},
    {D: I, W: '16', N: 'PADDR', P: 1, C: 0},
    {D: I, W: '1 ', N: 'PSEL', P: 1, C: 0},
    {D: I, W: '1 ', N: 'PENABLE', P: 1, C: 0},
    {D: I, W: '1 ', N: 'PWRITE', P: 1, C: 0},
    {D: I, W: '32', N: 'PWDATA', P: 1, C: 0},
    {D: O, W: '1 ', N: 'PREADY', P: 1, C: 0},
    {D: O, W: '32', N: 'PRDATA', P: 1, C: 0}
  ],
  'TYPE-1': [ 
    {D: I, W: '1 ', N: 'clock', P: 0, L: 'APBSlaveClock'},
    {D: I, W: '1 ', N: 'reset', P: 0, L: 'APBSlaveReset'},
  ]
}

CELL_PINS = {
  'WR': [
    { D: I, W: '1', N: 'enable__', P: 0, C: 1 },
    { D: I, W: 'W', N: 'D__fromSW__', P: 0, C: 1 },
    { D: O, W: 'W', N: 'Q__toHW__', P: 1, C: 0 }
  ],
  'RO': [
    { D: I, W: '1', N: 'enable__', P: 0, C: 1 },
    { D: I, W: 'W', N: 'D__fromHW__', P: 1, C: 0 },
    { D: O, W: 'W', N: 'Q__toSW__', P: 0, C: 0 }
  ],
  'WR12C': [
    { D: I, W: '1', N: 'enable__', P: 0, C: 1 },
    { D: I, W: 'W', N: 'D__fromHW__', P: 1, C: 0 },
    { D: O, W: 'W', N: 'Q__toSW__', P: 0, C: 0 },
    { D: I, W: 'W', N: 'WR1__fromSW__', P: 0, C: 0 },
    { D: O, W: 'W', N: 'CLEAR__toHW__', P: 1, C: 0 }
  ],
  'HWC': [
    { D: I, W: '1', N: 'enable__', P: 0, C: 1 },
    { D: I, W: 'W', N: 'D__fromSW__', P: 0, C: 1 },
    { D: O, W: 'W', N: 'Q__toHW__', P: 1, C: 0 },
    { D: I, W: 'W', N: 'CLEAR__fromHW__', P: 1, C: 0 },
  ],
  'HWCI': [
    { D: I, W: '1', N: 'enable__', P: 0, C: 1 },
    { D: I, W: 'W', N: 'D__fromSW__', P: 0, C: 1 },
    { D: O, W: 'W', N: 'Q_toHW__', P: 1, C: 0 },
    { D: I, W: 'W', N: 'CLEAR__fromHW__', P: 1, C: 0 },
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

# returns propagated IO list for a specified type 't' from a given collection 'c',  
# the master-list elements with given name 'n', after appending 's' to each element
def getIOList(c, t, n, v, s):
  ioListRaw = search(c,t,n,v)
  ioList = collect(ioListRaw, N, s)
  return ioList

def getIODecls(c, t, n, v, z, s):
  ioListRaw = search(c,t,n,v)
  d = collect(ioListRaw, D, '')
  if (z == 0):
    w = collect(ioListRaw, W, '')
  else:
    w = []
    for x in d:
      w.append(str(z)) 
  m = collect(ioListRaw, N, '')
  ioDecls = []
  length = len(d)
  for i in range(length):
    x = '  ' + d[i] + ' [' + w[i] + '-1:0] ' + m[i] + s + ';'
    ioDecls.append(x)
  return ioDecls

def getLocalDecl(c, t, d, s):
  ioListRaw = search(c,t,'LOCAL_WIRE',1)
  localWires = []
  length = len(ioListRaw)
  for i in range(length):
    width = ''
    if (ioListRaw[i][W] != 1):
      width = '[' + ioListRaw[i][W] + '-1:0]'
    localWires.append('  {0} {1} {2}{3};'.format(d, width, ioListRaw[i][N], s))
  return localWires

# outfile, regName, regBaseAddr
def genLogic_WR(o, n, b):
  print(n, b)
  o.write('always @(posedge clock) begin\n')
  o.write('  if (PADDR == {0}) begin\n'.format(b))
  o.write('    enable__{0} <= 1;\n'.format(n))  
  o.write('    D__fromSW__{0} <= PWDATA;\n'.format(n))  
  o.write('  end\n')
  o.write('  else begin\n'.format(b))
  o.write('    enable__{0} <= 0;\n'.format(n))  
  o.write('  end\n')
  o.write('end\n')

def genLogic_RO(o, n, b):
  print(n, b)
  o.write('always @(posedge clock) begin\n')
  o.write('  if (PADDR == {0}) begin\n'.format(b))
  o.write('    enable__{0} <= 1;\n'.format(n))  
  o.write('    PRDATA <= Q__toSW__{0};\n'.format(n))  
  o.write('  end\n')
  o.write('  else begin\n'.format(b))
  o.write('    enable__{0} <= 0;\n'.format(n))  
  o.write('  end\n')
  o.write('end\n')

def genLogic_HWC(o, n, b):
  print(n, b)
  o.write('always @(posedge clock) begin\n')
  o.write('  if (PADDR == {0}) begin\n'.format(b))
  o.write('    enable__{0} <= 1;\n'.format(n))  
  o.write('    D__fromSW__{0} <= PWDATA;\n'.format(n))  
  o.write('  end\n')
  o.write('  else begin\n'.format(b))
  o.write('    enable__{0} <= 0;\n'.format(n))  
  o.write('  end\n')
  o.write('end\n')
# print (getIOList(CELL_PINS, 'WR12C', P, 1, 'CHECK_'))
# print (getIODecls(CELL_PINS, 'WR12C', P, 1, 'CHECK_'))
# print (getInstStr(CELL_PINS, 'WR12C', 'CHECK_'))
