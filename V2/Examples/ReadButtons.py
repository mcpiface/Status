import smbus
import time
 
# Use I2C Bus 1
bus = smbus.SMBus(1)

# MCP23017 Data Sheet: http://ww1.microchip.com/downloads/en/devicedoc/20001952c.pdf

# Example derived from:
# https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-2/

# Addresses with IOCON.BANK = 0 (default)
DEVICE = 0x20 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
IODIRB = 0x01 # Port B direction register
GPIOA  = 0x12 # Register for LEDs
GPIOB  = 0x13 # Register for Buttons
IOCONA = 0x0A # Bank A IOCON CONFIGURATION REGISTER
IOCONB = 0x0B
GPPUA  = 0x0C # Bank A GPIO Pullups.
GPPUB  = 0x0D
INTFA  = 0x0E # Bank A Interrupt flats.
INTFB  = 0x0F
OLATA  = 0x14 # Bank A output latch
OLATB  = 0x15

# Set all GPA pins as output.
bus.write_byte_data(DEVICE,IODIRA,0x00)
 
# Set all GPB pins as input.
# Only GPB0..4 are actually used.
bus.write_byte_data(DEVICE,IODIRB,0xFF)

# Configure GPB0..3 as pullup
bus.write_byte_data(DEVICE,GPPUB,0x0F)

# Interrupt config.
# ODR: 1 (Open-drain output (overrides the INTPOL bit.))
# INTPOL: 0 (Active-low)
bus.write_byte_data(DEVICE,IOCONB,0x04)

# Interrupt on GPB0..4
bus.write_byte_data(DEVICE,INTFB,0x0F)
 
# Loop until user presses CTRL-C
while True:
  # Set LEDs to Green
  bus.write_byte_data(DEVICE,OLATA,0x55)
 
  # Read state of GPIOB register
  button = bus.read_byte_data(DEVICE,GPIOB)
 
  # GPB0..3 should be high if not pressed.
  # active low on button press.
  # GPB4..7 are tied low.
  if button != 0x0F:
   print "Switch was pressed! %x" % button

   # Make all LEDs red to indicate a button press
   bus.write_byte_data(DEVICE,OLATA,0xAA)
   time.sleep(2)