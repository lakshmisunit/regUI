
def printModule(o, t, n):
  if (t == 'WR'):
    printWR (o, n)
  if (t == 'HWC'):
    printHWC (o, n)

def printWR(o, n):
  o.write('module {0} (clock, reset, enable, D, Q);\n'.format(n))
  o.write('  parameter W = 32;\n')
  o.write('  input clock, reset, enable;\n')
  o.write('  input [W-1:0] D;\n')
  o.write('  output [W-1:0] Q;\n')
  o.write('  reg [W-1:0] Q;\n')
  o.write('  always @(posedge clock or negedge reset) begin\n')
  o.write('    if (reset == 1\'b0) begin\n')
  o.write('      Q <= 32\'b0;\n')
  o.write('    end\n')
  o.write('    else if (enable) begin\n')
  o.write('      Q <= D;\n')
  o.write('    end\n')
  o.write('  end\n')
  o.write('endmodule // {0}\n'.format(n))

# printModule(outfile, 'HWC', r.regName, [1,2,3, 26], ['a', 'b', 'c', 'reserved'], ['HWC', 'HWC', 'HWCI', 'RSVD'])
def printHWC(o, n):
  o.write('module {0} (clock, reset, enable, D, Q, clear);\n'.format(n))
  o.write('  parameter W = 32;\n')
  o.write('  input clock, reset, enable;\n')
  o.write('  input [W-1:0] D;\n')
  o.write('  output [W-1:0] Q;\n')
  o.write('  reg [W-1:0] Q;\n')
  o.write('  input [W-1:0] clear;\n')
  o.write('  always @(posedge clock or negedge reset) begin\n')
  o.write('    if (reset == 1\'b0) begin\n')
  o.write('      Q <= 32\'b0;\n')
  o.write('    end\n')
  o.write('    else if (enable) begin\n')
  o.write('      Q <= D;\n')
  o.write('      for(i=0; i<W; i=i+1) if(clear[i]) Q[i] <= 1\'b0;\n')
  o.write('    end\n')
  o.write('  end\n')
  o.write('endmodule // {0}\n'.format(n))