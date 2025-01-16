from reg_pkg_consts import CELL_PINS, COMMON_PINS, getIODecls, getIOList, getLocalDecl
from reg_pkg_consts import genLogic_WR, genLogic_RO, genLogic_HWC
import re
class Field:
  """This is a class which holds field properties"""
  parent = ''
  fldName = ""
  fldPos = ""
  fldWidth = ""
  resetVal = ""
  descr = ""
  ioNames = []
  ioDecls = []
  def __init__(self,parent,f,w,p,t,r,d):
    self.parent = parent
    self.fldName = f
    self.fldWidth = w
    self.fldPos = p
    self.fldType = t
    if(t == "read-only"):
        t = 'RO'
    if(t == "read-write" or t == "write-only"):
        t = 'WR'
    self.resetVal = r
    self.descr = d
    print(f"t value is = {t}")
    self.ioNames = getIOList (CELL_PINS, t, 'PROP', 1, parent+'__'+f)
    self.ioDecls = getIODecls(CELL_PINS, t, 'PROP', 1, w, parent+'__'+f)
  def show(self):
    print(self.fldType, self.fldPos, self.fldName)

class Reg:
  """This is a class which holds individual reg properties"""
  regName = ""
  regOffset = ""
  regType = ""
  regWidth = ""
  descr = ""
  fields = []
  instSigs = []
  started = 0
  fldNames = []
  fldWidths = []
  fldTypes = []
  localVars = []
  macros = []
  cmacros = []
  def __init__(self, b, n, t, o, z, d):
    self.baseAddr = b
    #print(self.baseAddr)
    self.regName = n
    self.regType = t
    self.regOffset = o
    #print(self.regOffset)
    self.regWidth = z
    self.descr = d
    self.macros.append('`define {0}__REG_OFFSET {1}\n'.format(n,o))
    o_ = int(re.sub("32\'h", '', o), 32) + self.baseAddr
    self.cmacros.append('`define {0} 0x{1}\n'.format(n,o_))
  def insertFld(self, f,w,p,t,r,d):
    if (t == 'RSVD'):
      return
    x = Field(self.regName, f,w,p,t,r,d)
    self.macros.append('`define {0}__{1} {2}\n'.format(self.regName,f,p))
    self.fields.append(x)
    x = None

  def start(self):
    if (self.started):
      return
    self.fldNames = []
    self.fldWidths = []
    self.fldTypes = []
    # collect all signal names and widths in arrays
    for y in self.fields:
        self.fldNames.append(y.fldName)
        self.fldWidths.append(y.fldWidth)
        self.fldTypes.append(y.fldType)
    self.fldNames.reverse()
    self.fldWidths.reverse()
    self.fldTypes.reverse()
    self.localVars = getLocalDecl(CELL_PINS, self.regType, 'reg', self.regName)
    print(len(self.localVars))
    self.started = 1

  def getInstSigs(self):
    self.start()
    self.instSigs = []
    if (self.regType == 'WR'):
      self.instSigs.append('wire [{0}:0] Q__toHW__{1};'.format((self.regWidth)-1, self.regName))
    elif (self.regType == 'RO'):
      self.instSigs.append('wire [{0}:0] D__fromHW__{1};'.format((self.regWidth)-1, self.regName))
      self.instSigs.append('wire [{0}:0] Q__toSW__{1};'.format((self.regWidth)-1, self.regName))
    elif (self.regType == 'WR12C'):
      # D_fromHW__, CLEAR_toHW__
      self.instSigs.append('wire [{0}:0] D__fromHW__{1};'.format((self.regWidth)-1, self.regName))
      self.instSigs.append('wire [{0}:0] CLEAR__toHW__{1};'.format((self.regWidth)-1, self.regName))
    elif (self.regType == 'HWC' or self.regType == 'HWCI'):
      # Q_toHW__, CLEAR_fromHW__
      print('returning signals for HWC')
      self.instSigs.append('wire [{0}:0] Q__toHW__{1};'.format((self.regWidth)-1, self.regName))
      self.instSigs.append('wire [{0}:0] CLEAR__fromHW__{1};'.format((self.regWidth)-1, self.regName))
      print(self.instSigs)
    return self.instSigs

  def getInstStr(self):
    if (self.regType == 'WR'):
      return '(.clock(clock), .reset(reset), .enable(enable__{0}), .D__fromSW(D__fromSW__{0}), .Q__toHW('.format(self.regName) + 'Q__toHW__{0}'.format(self.regName) + '));'
    elif (self.regType == 'RO'):
      return '(.clock(clock), .reset(reset), .enable(enable__{0}), .D__fromHW(D__fromHW__{1}), .Q__toSW(Q__toSW__{2}));'.format(self.regName, self.regName, self.regName)
    elif (self.regType == 'WR12C'):
      return '(.clock(clock), .reset(reset),' + '.enable(enable__{0}), '.format(self.regName) + '.D__fromHW(D__fromHW__{0}), '.format(self.regName) +'.Q__toSW(Q__toSW__{0}), '.format(self.regName), '.WR1__fromSW(WR1_fromSW__{0}), '.format(self.regName) + '.CLEAR__toHW(CLEAR_toHW__{0}));'.format(self.regName)
    elif (self.regType == 'HWC' or self.regType == 'HWCI'):
      return '(.clock(clock), .reset(reset),' + '.enable(enable__{0}), '.format(self.regName) + '.D__fromSW(D__fromSW__{0}), '.format(self.regName) + '.Q__toHW(Q__toHW__{0}), '.format(self.regName) + '.CLEAR__fromHW(CLEAR__fromHW__{0}));'.format(self.regName)
    return ''

  def getAssignStr(self):
    self.start()
    assign = ''
    if (self.regType == 'WR'):
      assign = 'assign { '
      x = []
      for f in self.fldNames:
        x.append('Q__toHW__'+self.regName+'__'+f)
      if (self.fldNames[-1] == 'reserved' and self.fldWidth[-1] > 0):
        assign = assign + '{' + '{0}'.format(self.fldWidth[-1]) + '{1\'b0}}, '
      assign = assign + ', '.join(x) + ' }'
      assign = assign + ' = Q__toHW__{0};'.format(self.regName)
    elif (self.regType == 'RO'):
      x = []
      assign = 'assign D__fromHW__{0} = '.format(self.regName)
      assign = assign + '{'
      for f in self.fldNames:
        x.append('D__fromHW__'+self.regName+'__'+f)
      assign = assign + ', '.join(x) + '};'
    elif (self.regType == 'WR12C'):
      x = []
      assign = 'assign Q__toSW__{0} = '.format(self.regName)
      assign = assign + '{'
      for f in self.fldNames:
        x.append('D__fromHW__'+self.regName+'__'+f)
      assign = assign + ', '.join(x) + '};\n'
      x = []
      tmp = 'assign {'
      for f in self.fldNames:
        x.append('CLEAR__toHW__{0}_{1}'.format(self.regName, f))
      tmp = tmp + ', '.join(x) + '} = CLEAR__toHW__{0};'.format(self.regName)
      assign = assign + tmp
    elif (self.regType == 'HWC' or self.regType == 'HWCI'):
      assign = 'assign { '
      x = []
      for f in self.fldNames:
        x.append('Q__toHW__'+self.regName+'__'+f)
      if (self.fldNames[-1] == 'reserved' and self.fldWidth[-1] > 0):
        assign = assign + '{' + '{0}'.format(self.fldWidth[-1]) + '{1\'b0}}, '
      assign = assign + ', '.join(x) + ' }'
      assign = assign + ' = Q__toHW__{0};'.format(self.regName)
      x = []
      tmp = 'assign CLEAR__fromHW__{0} '.format(self.regName) + '= {'
      for f in self.fldNames:
        x.append('CLEAR__fromHW__{0}__{1}'.format(self.regName, f))
      tmp = tmp + ', '.join(x) + '};'
      assign = assign + tmp

    return assign

class RegBlock:
  """This is a class which holds the reg-block properties"""
  blockName = ""
  blockAddrBase = 0
  descr = ""
  macros = []
  def __init__(self, n, a, d):
    self.regArray = []
    self.blockName = n
    self.blockAddrBase = a
    self.descr = d
  def insertReg(self, r):
    self.regArray.append(r)
  def setMacros(self, m):
    self.macros = m
  def printBlock(self, fname):
    print('in Block')
    mfile = 'MACROS_'+fname
    with open(mfile, 'w') as macfile:
      macfile.write('//////////////////////////////////////////////////////////////\n')
      macfile.write('// Auto-generated by RegMagic software.  Do not edit this file\n')
      macfile.write('//////////////////////////////////////////////////////////////\n')
      for r in self.regArray:
        # take one reg at a time
        print(r)
        for m in r.macros:
          print(m)
    macfile.close()
    with open(fname, 'w') as outfile:
      outfile.write('//////////////////////////////////////////////////////////////\n')
      outfile.write('// Auto-generated by RegMagic software.  Do not edit this file\n')
      outfile.write('//////////////////////////////////////////////////////////////\n')
      for m in self.macros:
        outfile.write('{0}\n'.format(m))
      # ###################### CREATE the cells ########################
      # for r in self.regArray:
      #   r.start()
      #   printModule(outfile, r.regType, r.regName)

      # ################################################################
      # ###################### CREATE the block ########################
      outfile.write("module {0} (\n".format(self.blockName))

      # ###################### PRINT io signals ########################
      s = ', '.join(getIOList(COMMON_PINS, 'APB', 'PROP', 1, '')) + ', '
      for l in range(len(self.regArray)):
        # take one reg at a time
        r = self.regArray[l]
        length = len(r.fields)
        # complete all fields in that reg
        for i in range(length):
          s = s + ', '.join(r.fields[i].ioNames)
          if (i<length-1):
            s = s + ', '
        if(l<len(self.regArray)-1):
          s = s + ','
      outfile.write('  {0}\n'.format(s))
      outfile.write(");\n")
      outfile.write('parameter W = 32;\n')
      
      # ###################### DEFINE io signals ########################
      s = getIODecls(COMMON_PINS, 'APB', 'PROP', 1, 0, '')
      for x in s:
        outfile.write('{0}\n'.format(x))
      for r in self.regArray:
        r.start()
        print('Processing {0} -- {1}'.format(r.regName, len(r.localVars)))
        for q in r.localVars:
          print(q)
          outfile.write('{0}\n'.format(q))
        for f in r.fields:
          for i in f.ioDecls:
            outfile.write('{0}\n'.format(i))
      
      # ###################### CREATE   instSigs  ########################
      for r in self.regArray:
        y = r.getInstSigs()
        for z in y: 
          outfile.write(z + '\n')
      
      # ###################### CREATE   assigns   ########################
      for r in self.regArray:
        outfile.write(r.getAssignStr())
        outfile.write('\n')
      
      # ###################### CREATE   instances ########################
      for r in self.regArray:
        outfile.write(r.regType)
        outfile.write(' #({0}) '.format(r.regWidth))
        outfile.write(r.regName)
        outfile.write(r.getInstStr() + '\n')
      
      # ###################### GENERATE logic code #######################
      for r in self.regArray:
        if (r.regType == 'WR'):
          genLogic_WR (outfile, r.regName, r.regOffset)
        elif (r.regType == 'RO'):
          genLogic_RO (outfile, r.regName, r.regOffset)
        elif (r.regType == 'HWC' or r.regType == 'HWCI'):
          genLogic_HWC (outfile, r.regName, r.regOffset)

      # ###################### CLOSE the module   ########################
      outfile.write("endmodule // {0} \n".format(self.blockName))
      # ##################################################################

    outfile.close()
