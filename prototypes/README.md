Note: Make sure mock is enabled to run prototype modules in development/your system

mqttcontrol_ON_BOARD.py: starts connection with MQTT and controls motor.
  dependencies:
    - MQTT broker for messages and instructions
    - MQTT client (like phone app or web app) to controll/send instructions

ultrasonicsensor_ON_BOARD.py: prototype to get ultrasonic values and control motor based on those values.
  dependencies:
    - to try on actual device - ultrasonic sensors are required and pins to be configured in pins.json file.
    - for mock testing, enable mock and run the module.

mockdatageneration\
  psut.py: this module generates simple information about system - like process, cpu usage, etc.
    dependencies:
      - telemetry server must be running to centralize data (or can be configured to save locally on board).