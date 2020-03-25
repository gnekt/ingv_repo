from obspy.clients.nrl import NRL
from obspy.core.inventory.response import Response
from obspy.io.xseed.parser import  Parser
from obspy.clients.nrl.client import NRLDict
from obspy.core.inventory.response import PolesZerosResponseStage
nrl = NRL()

nrl_dic = NRLDict(nrl)
for man in nrl.sensors:
    print(man)
    print("->")
    for product in nrl.sensors[man]:
        print(product)
        print("->")
        period_freq = nrl.sensors[man][product]
        


sensor =  nrl.get_sensor_response(sensor_keys=['Guralp','CMG-40T','40s - 100Hz','800'])
print(sensor._get_overall_sensitivity_and_gain())
for stage in sensor.response_stages:
    if isinstance(stage,PolesZerosResponseStage):
        print( 'Input ' + stage.input_units)
        print( 'Output '+ stage.output_units)
        print(' Transfer Function Type ' + stage.pz_transfer_function_type)
        print(' Normalization Factor : {norm_factor:g}'.format(norm_factor=stage.normalization_factor))
        print(' Normalization Frequency : {norm_frequency:.2f}'.format(norm_frequency=stage.normalization_frequency))
        print(' Gain : {gain:.5f}'.format(gain=stage.stage_gain))
        print(stage.zeros.__str__())
        print(stage.poles.__str__())


# resp=nrl.get_response( sensor_keys=['Guralp','CMG-40T','40s - 100Hz','800'],
#                datalogger_keys=['REF TEK', 'RT 130 & 130-SMA', '1', '200'])

# print(resp.get_sacpz())
# my_parser = Parser(data=resp)


