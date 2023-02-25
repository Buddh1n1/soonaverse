from iota_client import IotaClient
import time
import matplotlib.pyplot as plt

inWeeks = True

#region statics
client = IotaClient({'nodes': ['https://api.shimmer.network']})
soonid = "0x0884298fe9b82504d26ddb873dbd234a344c120da3a4317d8063dbcf96d356aa9d0100000000"
scale = 1+6*int(inWeeks)
indices = 52*7//scale
expires_in = []
for i in range(indices):
    expires_in.append(0)
#endregion

output_ids = client.basic_output_ids([{"hasTimelock": True},{"hasNativeTokens": True}])
soon_outputs = [o['output'] for o in client.get_outputs(output_ids) if o['output']['nativeTokens'][0]['id']==soonid]

for o in soon_outputs:
    ind = int(o['unlockConditions'][1]['unixTime'] - time.time()) // (24*60*60*scale)
    if ind < indices:
        expires_in[ind]+=(int(o['nativeTokens'][0]['amount'], 16))//1000000

plt.bar(range(indices), expires_in)
plt.title(f'soon tokens locked in {"weeks" if inWeeks else "days"}')
plt.show()
