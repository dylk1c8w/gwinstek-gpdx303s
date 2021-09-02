import time
from GWInstekGPDx303S.GWInstekGPDx303S import GWInstekGPDx303S


port = "COM3"  # serial port of GWInstek GPDx303S
gwinstek_gpdx303s = GWInstekGPDx303S(
    port=port
)  # establishe communication with the GWInstek GPDx303S
gwinstek_gpdx303s.on()  # set output status ON
time.sleep(5.0)  # wait 5 seconds
gwinstek_gpdx303s.off()  # set output status OFF
gwinstek_gpdx303s.close()  # close communication with theGWInstek GPDx303S
del gwinstek_gpdx303s
