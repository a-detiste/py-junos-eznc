from . import RunstatMaker as RSM

##### -------------------------------------------------------------------------
##### illustrates the use of field groups; optimization around collecting
##### from XML child node-sets
##### -------------------------------------------------------------------------

EthPortView = RSM.View(RSM.Fields()
  .str('oper', 'oper-status')
  .str('admin','admin-status')
  .int('mtu')
  .str('link_mode','link-mode')
  .str('speed')
  .str('macaddr','current-physical-address')
  .int('rx_bytes', 'input-bytes', group='mac_stats')
  .int('rx_packets', 'input-packets', group='mac_stats')
  .int('tx_bytes', 'output-bytes', group='mac_stats')
  .int('tx_packets', 'output-packets', group='mac_stats')
  .end,
  groups = {
    'mac_stats':'ethernet-mac-statistics'
  }
)

EthPortTable = RSM.GetTable('get-interface-information',
  args =  {'media': True, 'interface_name': '[fgx]e*' },
  item = 'physical-interface',
  view = EthPortView
)

##### this shows example of two things:
##### (1) extending an existing view at runtime
##### (2) using a 'flag' field to return True/False if the
#####     xpath/element exists

class EthPortView2(EthPortView):  
  """ extend the EthPortView at runtime """

  def __init__(self,**kvargs):    
    with self.updater() as more:
      more.groups = {'flags':'if-device-flags'}
      more.fields.flag('present', 'ifdf-present', group='flags')
      more.fields.flag('running', 'ifdf-running', group='flags')

    # call parent __init__ **after** the udpates
    EthPortView.__init__(self, **kvargs)

##### The following shows how to declare a new class that
##### extends from another class.  Most of the time you
##### will want to do this, and not the runtime way ...
##### but it's good to have options, yo!

EthPortView4 = RSM.View( extends=EthPortView, 
  fields = RSM.Fields()
    .flag('present', 'ifdf-present', group='flags')
    .flag('running', 'ifdf-running', group='flags')
    .astype('loopback', astype=lambda x: True if x == 'enabled' else False)
    .end,
  groups = {'flags':'if-device-flags'})