##Function to overwrite the config file of the touch screen's backlight with a brand new value.
#
# arg: value: the value of the screen's backlight intensity.
#The value must be in 0 and 255.
#
# return: none
def setBackLight(value):
    filepath="/sys/class/backlight/rpi_backlight/brightness"
    configFile=open(filepath, "w")
    configFile.write(str(value))
    configFile.close()
