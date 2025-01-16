// Code your design here
// Code your design here


/*
  Write-able cells have the following characteristics:
    * accept input data from software (through APB)
    * provide the registered data (written from APB) towards HW side
 **/
module WR (
  clock,
  reset,
  enable__,
  D__fromSW__,
  Q__toHW__
);
  parameter W = 1;
  parameter RESETVAL = 32'h0;

  input   clock;
  input   reset;
  input   enable__;
  input   [W-1:0] D__fromSW__;
  output  [W-1:0] Q__toHW__;
  
  reg     [W-1:0] Q__toHW__;
  always @(posedge clock or negedge reset) begin
    if (!reset) begin
      Q__toHW__     <= RESETVAL;
    end
    else begin
      if (enable__) begin
        Q__toHW__   <= D__fromSW__;
      end
    end
  end
endmodule

/*
  Read-only cells have the following characteristics:
    * accept input data from HW side
    * provide the registered data (written from HW) towards SW side (APB side)
 **/
module RO (
  clock,
  reset,
  enable__,
  D__fromHW__,
  Q__toSW__
);
  parameter W = 1;
  parameter RESETVAL = 32'h0;
  input   clock;
  input   reset;
  input   enable__;
  input   [W-1:0] D__fromHW__;
  output  [W-1:0] Q__toSW__;
  reg     [W-1:0] Q__toSW__;
  always @(posedge clock or negedge reset) begin
    if (!reset) begin
      Q__toSW__     <= RESETVAL;
    end
    else begin
      if (enable__) begin
        Q__toSW__   <= D__fromHW__;
      end
    end
  end
endmodule

/*
  HW-clear cells have the following characteristics:
    * accept input data from SW side
    * provide the registered data (written from SW) towards HW side
    * accept and respond to CLEAR signal from HW side and clear the output
**/
module HWC (
  clock,
  reset,
  enable__,
  D__fromSW__,
  Q__toHW__,
  CLEAR__fromHW__
);
  parameter W = 1;
  parameter RESETVAL = 32'h0;

  input   clock;
  input   reset;
  input   enable__;
  input   [W-1:0] D__fromSW__;
  output  [W-1:0] Q__toHW__;
  input   [W-1:0] CLEAR__fromHW__;
  
  reg     [W-1:0] Q__toHW__;
  always @(posedge clock or negedge reset) begin
    if (!reset) begin
      Q__toHW__       <= RESETVAL;
    end
    else begin
      if (enable__) begin
        Q__toHW__     <= D__fromSW__ & CLEAR__fromHW__;
      end
    end
  end
endmodule

/*
  HW-clear-inverted cells have the following characteristics:
    * accept input data from SW side
    * provide the inverted value of the registered data (written from SW) towards HW side
    * accept and respond to CLEAR signal from HW side and clear the output
 **/
module HWCI (
  clock,
  reset,
  enable__,
  D__fromSW__,
  Q__toHW__,
  CLEAR__fromHW__
);
  parameter W = 1;
  input   clock;
  input   reset;
  input   enable__;
  input   [W-1:0] D__fromSW__;
  output  [W-1:0] Q__toHW__;
  input   [W-1:0] CLEAR__fromHW__;
  reg     [W-1:0] Q__toHW__;
  
  reg     [W-1:0] Q_toHW__;
  always @(posedge clock or negedge reset) begin
    if (!reset) begin
      Q__toHW__       <= 32'hFFFF_FFFF;
    end
    else begin
      if (enable__) begin
        Q__toHW__     <= ~D__fromSW__ & CLEAR__fromHW__;
      end
    end
  end
endmodule