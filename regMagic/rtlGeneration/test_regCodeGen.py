regs = []
class Reg:
  regName = ''
  regWidth = 32
  regType = ''
  regOffset = ''
  fields = []
  def __init__(self, n, w, t, o, f):
    self.regName = n
    self.regWidth = w 
    self.regType = t 
    self.regOffset = o 
    self.fields = f 

wr_reg = 'Cfg_Rx_BaseControl'
wr_fields = [
  {'fldName': 'enableRxPHY', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'enableOffsetCalib', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'enableEyeCalib', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'enableDLLCalib', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'enableEyeScan', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'enableDeskew', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'enableRXterm', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'resetRx', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'selectTerminationType', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'selectRxClock', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'selectPDControls', 'fldWidth': 1, 'fldType': 'WR'},
  {'fldName': 'setImpedance', 'fldWidth': 1, 'fldType': 'WR'}
]
r = Reg (wr_reg, 32, 'WR', '10\'h000', wr_fields)
regs.append(r)


ro_reg = 'Sts_Rx_AggregatedStatus'
ro_fields = [
  {'fldName': 'RXReady', 'fldWidth': 1, 'fldType': 'RO'},
  {'fldName': 'offsetCalibDone', 'fldWidth': 1, 'fldType': 'RO'},
  {'fldName': 'eyeCalibDone', 'fldWidth': 1, 'fldType': 'RO'},
  {'fldName': 'DLLCalibDone', 'fldWidth': 1, 'fldType': 'RO'},
  {'fldName': 'eyeScanDone', 'fldWidth': 1, 'fldType': 'RO'},
  {'fldName': 'deskewDone', 'fldWidth': 1, 'fldType': 'RO'}
]
r = Reg (ro_reg, 32, 'RO', '10\'h004', ro_fields)
regs.append(r)

hwc_reg = 'Cfg_PHY_OperationalControl'
hwc_fields = [
  {'fldName': 'resetPHY', 'fldType': 'HWC', 'fldWidth': 1},
  {'fldName': 'startPVTCalib', 'fldType': 'HWC', 'fldWidth': 1},
  {'fldName': 'resetPVTCalib', 'fldType': 'HWC', 'fldWidth': 1},
  {'fldName': 'startImpedanceCalib', 'fldType': 'HWC', 'fldWidth': 1},
  {'fldName': 'resetImpedanceCalib', 'fldType': 'HWC', 'fldWidth': 1},
  {'fldName': 'powerDownPHY', 'fldType': 'HWC', 'fldWidth': 1}
]
r = Reg (hwc_reg, 32, 'HWC', '10\'h008', hwc_fields)
regs.append(r)

# print(getIOList(CELL_PINS, 'HWC', hwc_reg, hwc_fields))
# print(getIODecls(CELL_PINS, 'HWC', hwc_reg, hwc_fields))
# print(getLocalVars(CELL_PINS, 'HWC', hwc_reg, 32))
# print(getAssignStr('HWC', hwc_reg, hwc_fields))
# print(getInstStr(CELL_PINS, 'HWC', hwc_reg))
# print(getIOList(CELL_PINS, 'RO', ro_reg, ro_fields))
# print(getIODecls(CELL_PINS, 'RO', ro_reg, ro_fields))
# print(getLocalVars(CELL_PINS, 'RO', ro_reg, 32))
# print(getAssignStr('RO', ro_reg, ro_fields))
# print(getInstStr(CELL_PINS, 'RO', ro_reg))
# print(getIOList(CELL_PINS, 'WR', wr_reg, wr_fields))
# print(getIODecls(CELL_PINS, 'WR', wr_reg, wr_fields))
# print(getLocalVars(CELL_PINS, 'WR', wr_reg, 32))
# print(getAssignStr('WR', wr_reg, wr_fields))
# print(getInstStr(CELL_PINS, 'WR', wr_reg))

# with open('out.ttx', 'w') as a:
#   genEnables(a, ['adfadf', 'fgdgfdg', 'iaueoirueiou', 'areadj'], [100, 200, 300, 400])
# a.close()

# with open('out.ttx', 'w') as a:
#   genInputDataRouting(a, ['adfadf', 'fgdgfdg', 'iaueoirueiou', 'areadj'], 'WR')
# a.close()
