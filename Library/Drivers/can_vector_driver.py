'''
:Author: *Jim Nilsson*  
:Version: *0.9 Beta*
:Status: *Released*

------------------------------------------------------------------------------- 
'''

#IMPORTS
import os
import ctypes

#MODULE CONSTANTS
XL_CONFIG_MAX_CHANNELS      =       64
XL_MAX_LENGTH               =       31
XL_INTERFACE_VERSION        =       3
XL_ACTIVATE_RESET_CLOCK     =       8
XL_INVALID_PORTHANDLE       =       -1
MAX_MSG_LEN                 =       8

XL_TRANSCEIVER_STATUS_PRESENT                     =       ctypes.c_uint(0x0001)
XL_TRANSCEIVER_STATUS_POWER                       =       ctypes.c_uint(0x0002)
XL_TRANSCEIVER_STATUS_MEMBLANK                    =       ctypes.c_uint(0x0004)
XL_TRANSCEIVER_STATUS_MEMCORRUPT                  =       ctypes.c_uint(0x0008)
XL_TRANSCEIVER_STATUS_POWER_GOOD                  =       ctypes.c_uint(0x0010)
XL_TRANSCEIVER_STATUS_EXT_POWER_GOOD              =       ctypes.c_uint(0x0020)
XL_TRANSCEIVER_STATUS_NOT_SUPPORTED               =       ctypes.c_uint(0x0040)

XLuint64                    =       ctypes.c_longlong
XLaccess                    =       XLuint64
XLportHandle                =       ctypes.c_long
XLeventTag                  =       ctypes.c_ubyte

class s_xl_can_msg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ulong),
                ("flags", ctypes.c_ushort),
                ("dlc", ctypes.c_ushort),
                ("res1", XLuint64),
                ("data", ctypes.c_ubyte*MAX_MSG_LEN)]

class s_xl_chip_state(ctypes.Structure):
    _fields_ = [("busStatus", ctypes.c_ubyte),
                ("txErrorCounter", ctypes.c_ubyte),
                ("rxErrorCounter", ctypes.c_ubyte),
                ("chipStatte", ctypes.c_ubyte),
                ("flags", ctypes.c_uint)]

class s_xl_lin_crc_info(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte),
                ("flags", ctypes.c_ubyte)]

class s_xl_lin_wake_up(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]

class s_xl_lin_no_ans(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte)]

class s_xl_lin_sleep(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]

class s_xl_lin_msg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte),
                ("dlc", ctypes.c_ubyte),
                ("flags", ctypes.c_ushort),
                ("data", ctypes.c_ubyte*8),
                ("crc", ctypes.c_ubyte)]

class s_xl_lin_msg_api(ctypes.Union):
    _fields_ = [("s_xl_lin_msg", s_xl_lin_msg),
                ("s_xl_lin_no_ans", s_xl_lin_no_ans),
                ("s_xl_lin_wake_up", s_xl_lin_wake_up),
                ("s_xl_lin_sleep", s_xl_lin_sleep),
                ("s_xl_lin_crc_info", s_xl_lin_crc_info)]

class s_xl_sync_pulse(ctypes.Structure):
    _fields_ = [("pulseCode", ctypes.c_ubyte),
                ("time", XLuint64)]

class s_xl_daio_data(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_ubyte),
                ("timestamp_correction", ctypes.c_uint),
                ("mask_digital", ctypes.c_ubyte),
                ("value_digital", ctypes.c_ubyte),
                ("mask_analog", ctypes.c_ubyte),
                ("reserved", ctypes.c_ubyte),
                ("value_analog", ctypes.c_ubyte*4),
                ("pwm_frequency", ctypes.c_uint),
                ("pwm_value", ctypes.c_ubyte),
                ("reserved1", ctypes.c_uint),
                ("reserved2", ctypes.c_uint)]

class s_xl_transceiver(ctypes.Structure):
    _fields_ = [("event_reason", ctypes.c_ubyte),
                ("is_present", ctypes.c_ubyte)]

class s_xl_tag_data(ctypes.Union):
    _fields_ = [("msg", s_xl_can_msg),
                ("chipState", s_xl_chip_state),
                ("linMsgApi", s_xl_lin_msg_api),
                ("syncPulse", s_xl_sync_pulse),
                ("daioData", s_xl_daio_data),
                ("transceiver", s_xl_transceiver)]

class s_xl_event(ctypes.Structure):
    _fields_ =[ ("tag", XLeventTag),
                ("chanIndex", ctypes.c_ubyte),
                ("transId", ctypes.c_ushort),
                ("portHandle", ctypes.c_ushort),
                ("reserved", ctypes.c_ushort),
                ("timeStamp", XLuint64),
                ("tagData", s_xl_tag_data)]

XLevent = s_xl_event()

class XLchipParams(ctypes.Structure):
    _fields_ = [("bitRate", ctypes.c_ulong),
                ("sjw", ctypes.c_ubyte),
                ("tseg1", ctypes.c_ubyte),
                ("tseg2", ctypes.c_ubyte),
                ("sam", ctypes.c_ubyte)]

class XLbusParamsCAN(ctypes.Structure):
    _fields_ = [("bitRate", ctypes.c_uint),
                ("sjw", ctypes.c_ubyte),
                ("tseg1", ctypes.c_ubyte),
                ("tseg2", ctypes.c_ubyte),
                ("sam", ctypes.c_ubyte),
                ("outputMode", ctypes.c_ubyte)]

class union(ctypes.Union):
    _fields_ = [("can", XLbusParamsCAN),
                ("padding", ctypes.c_ubyte*32)]
                
class XLbusParams(ctypes.Structure):
    _fields_ = [("busType", ctypes.c_uint),
                ("data", union)]
    
class XLchannelConfig(ctypes.Structure):
    _pack_   = 1
    _fields_ = [("name", ctypes.c_char*(XL_MAX_LENGTH + 1)),
                ("hwType", ctypes.c_ubyte),
                ("hwIndex", ctypes.c_ubyte),
                ("hwChannel", ctypes.c_ubyte),
                ("transceiverType", ctypes.c_ushort),
                ("transceiverState", ctypes.c_uint),
                ("channelIndex", ctypes.c_ubyte),
                ("channelMask", XLuint64),
                ("channelCapabilities", ctypes.c_uint),
                ("channelBusCapabilities", ctypes.c_uint),
                ("isOnBus", ctypes.c_ubyte),
                ("connectedBusType", ctypes.c_uint),
                ("busParams", XLbusParams),
                ("driverVersion", ctypes.c_uint),
                ("interfaceVersion", ctypes.c_uint),
                ("raw_data", ctypes.c_uint*10),
                ("serialNumber", ctypes.c_uint),
                ("articleNumber", ctypes.c_uint),
                ("transceiverName", ctypes.c_char*(XL_MAX_LENGTH + 1)),
                ("specialCabFlags", ctypes.c_uint),
                ("dominantTimeout", ctypes.c_uint),
                ("reserved", ctypes.c_uint*8)]

class XLdriverConfig(ctypes.Structure):
    _fields_ = [("dllVersion", ctypes.c_uint),
                ("channelCount", ctypes.c_uint),
                ("reserved", ctypes.c_uint*10),
                ("Channel", XLchannelConfig*XL_CONFIG_MAX_CHANNELS)]

class XlDriver():
    """
        **Description:** This is the XL-Driver class that contains all
        methods needed to commuicate with Vectors XL-Driver.
    """
    #DICTIONARIES
    HARDWARE_TYPE = \
    {
        'XL_HWTYPE_NONE'                        :       0,
        'XL_HWTYPE_VIRTUAL'                     :       1,
        'XL_HWTYPE_CANCARDX'                    :       2,
        'XL_HWTYPE_CANAC2PCI'                   :       6,
        'XL_HWTYPE_CANCARDY'                    :       12,
        'XL_HWTYPE_CANCARDXL'                   :       15,
        'XL_HWTYPE_CANCASEXL'                   :       21,
        'XL_HWTYPE_CANCASEXL_LOG_OBSOLETE'      :       23,
        'XL_HWTYPE_CANBOARDXL'                  :       25,
        'XL_HWTYPE_CANBOARDXL_PXI'              :       27,
        'XL_HWTYPE_VN2600'                      :       29,
        'XL_HWTYPE_VN2610'                      :       29,
        'XL_HWTYPE_VN3300'                      :       37,
        'XL_HWTYPE_VN3600'                      :       39,
        'XL_HWTYPE_VN7600'                      :       41,
        'XL_HWTYPE_CANCARDXLE'                  :       43,
        'XL_HWTYPE_VN8900'                      :       45,
        'XL_HWTYPE_VN8950'                      :       47,
        'XL_HWTYPE_VN2640'                      :       53,
        'XL_HWTYPE_VN1610'                      :       55,
        'XL_HWTYPE_VN1630'                      :       57,
        'XL_HWTYPE_VN1640'                      :       59,
        'XL_HWTYPE_VN8970'                      :       61,
        'XL_HWTYPE_VN1611'                      :       63,
        'XL_HWTYPE_VT6204'                      :       61,
        'XL_HWTYPE_VN5610'                      :       65,
        'XL_HWTYPE_VN7570'                      :       67,
        'XL_HWTYPE_IPCLIENT'                    :       69
    }
    
    BUS_TYPE = \
    {
        'XL_BUS_TYPE_NONE'                      :       0x00000000,
        'XL_BUS_TYPE_CAN'                       :       0x00000001,
        'XL_BUS_TYPE_LIN'                       :       0x00000002,
        'XL_BUS_TYPE_FLEXRAY'                   :       0x00000004,
        'XL_BUS_TYPE_MOST'                      :       0x00000010,
        'XL_BUS_TYPE_DAIO'                      :       0x00000040,
        'XL_BUS_TYPE_J1708'                     :       0x00000100
    }
    
    DRIVER_STATUS = \
    {
        'XL_SUCCESS'                            :       0,  
        'XL_PENDING'                            :       1,       
        'XL_ERR_QUEUE_IS_EMPTY'                 :       10, 
        'XL_ERR_QUEUE_IS_FULL'                  :       11, 
        'XL_ERR_TX_NOT_POSSIBLE'                :       12, 
        'XL_ERR_NO_LICENSE'                     :       14, 
        'XL_ERR_WRONG_PARAMETER'                :       101,
        'XL_ERR_TWICE_REGISTER'                 :       110,
        'XL_ERR_INVALID_CHAN_INDEX'             :       111,
        'XL_ERR_INVALID_ACCESS'                 :       112,
        'XL_ERR_PORT_IS_OFFLINE'                :       113,
        'XL_ERR_CHAN_IS_ONLINE'                 :       116,
        'XL_ERR_NOT_IMPLEMENTED'                :       117,
        'XL_ERR_INVALID_PORT'                   :       118,
        'XL_ERR_HW_NOT_READY'                   :       120,
        'XL_ERR_CMD_TIMEOUT'                    :       121,
        'XL_ERR_HW_NOT_PRESENT'                 :       129,
        'XL_ERR_NOTIFY_ALREADY_ACTIVE'          :       131,
        'XL_ERR_NO_RESOURCES'                   :       152,
        'XL_ERR_WRONG_CHIP_TYPE'                :       153,
        'XL_ERR_WRONG_COMMAND'                  :       154,
        'XL_ERR_INVALID_HANDLE'                 :       155,
        'XL_ERR_RESERVED_NOT_ZERO'              :       157,
        'XL_ERR_INIT_ACCESS_MISSING'            :       158,
        'XL_ERR_CANNOT_OPEN_DRIVER'             :       201,
        'XL_ERR_WRONG_BUS_TYPE'                 :       202,
        'XL_ERR_DLL_NOT_FOUND'                  :       203,
        'XL_ERR_INVALID_CHANNEL_MASK'           :       204,
        'XL_ERR_CONNECTION_BROKEN'              :       210,
        'XL_ERR_CONNECTION_CLOSED'              :       211,
        'XL_ERR_INVALID_STREAM_NAME'            :       212,
        'XL_ERR_CONNECTION_FAILED'              :       213,
        'XL_ERR_STREAM_NOT_FOUND'               :       214,
        'XL_ERR_STREAM_NOT_CONNECTED'           :       215,
        'XL_ERR_QUEUE_OVERRUN'                  :       216,
        'XL_ERROR'                              :       255
    }
    
    CHIP_STATE = \
    {
        'XL_CHIPSTAT_BUSOFF'                    :       0x01,
        'XL_CHIPSTAT_ERROR_PASSIVE'             :       0x02,
        'XL_CHIPSTAT_ERROR_WARNING'             :       0x04,
        'XL_CHIPSTAT_ERROR_ACTIVE'              :       0x08
    }
    
    TRANSCEIVER_STATE = \
    {    
        'XL_TRANSCEIVER_STATUS_PRESENT'         :       0x0001,
        'XL_TRANSCEIVER_STATUS_POWER'           :       0x0002,
        'XL_TRANSCEIVER_STATUS_MEMBLANK'        :       0x0004,
        'XL_TRANSCEIVER_STATUS_MEMCORRUPT'      :       0x0008,
        'XL_TRANSCEIVER_STATUS_POWER_GOOD'      :       0x0010,
        'XL_TRANSCEIVER_STATUS_EXT_POWER_GOOD'  :       0x0020,
        'XL_TRANSCEIVER_STATUS_NOT_SUPPORTED'   :       0x0040
    }
    
    IS_ON_BUS = \
    {
        'YES'                                   :       0x01,
        'NO'                                    :       0x00
    }
    
    DRIVER_STATUS_MSG = \
    {
         0             :      'SUCCESS',                      
         1             :      'PENDING',                           
         10            :      'ERROR QUEUE IS EMPTY',           
         11            :      'ERROR QUEUE IS FULL',            
         12            :      'ERROR TX NOT POSSIBLE',          
         14            :      'ERROR NO LICENSE',               
         101           :      'ERROR WRONG PARAMETER',         
         110           :      'ERROR TWICE REGISTER',          
         111           :      'ERROR INVALID CHAN INDEX',      
         112           :      'ERROR INVALID ACCESS',          
         113           :      'ERROR PORT IS OFFLINE',         
         116           :      'ERROR CHAN IS ONLINE',          
         117           :      'ERROR NOT IMPLEMENTED',         
         118           :      'ERROR INVALID PORT',            
         120           :      'ERROR HW NOT READY',            
         121           :      'ERROR CMD TIMEOUT',             
         129           :      'ERROR HW NOT PRESENT',          
         131           :      'ERROR NOTIFY ALREADY ACTIVE',   
         152           :      'ERROR NO RESOURCES',            
         153           :      'ERROR WRONG CHIP TYPE',         
         154           :      'ERROR WRONG COMMAND',           
         155           :      'ERROR INVALID HANDLE',          
         157           :      'ERROR RESERVED NOT ZERO',       
         158           :      'ERROR INIT ACCESS MISSING',     
         201           :      'ERROR CANNOT OPEN DRIVER',      
         202           :      'ERROR WRONG BUS TYPE',          
         203           :      'ERROR DLL NOT FOUND',           
         204           :      'ERROR INVALID CHANNEL MASK',    
         210           :      'ERROR CONNECTION BROKEN',       
         211           :      'ERROR CONNECTION CLOSED',       
         212           :      'ERROR INVALID STREAM NAME',     
         213           :      'ERROR CONNECTION FAILED',       
         214           :      'ERROR STREAM NOT FOUND',        
         215           :      'ERROR STREAM NOT CONNECTED',    
         216           :      'ERROR QUEUE OVERRUN',           
         255           :      'GENERAL ERROR'                       
    }
    
    HARDWARE_TYPE_MSG = \
    {
         0             :       'XL_HWTYPE_NONE',                        
         1             :       'XL_HWTYPE_VIRTUAL',                     
         2             :       'XL_HWTYPE_CANCARDX',                    
         6             :       'XL_HWTYPE_CANAC2PCI',                   
         12            :       'XL_HWTYPE_CANCARDY',                  
         15            :       'XL_HWTYPE_CANCARDXL',                 
         21            :       'XL_HWTYPE_CANCASEXL',                
         23            :       'XL_HWTYPE_CANCASEXL_LOG_OBSOLETE',    
         25            :       'XL_HWTYPE_CANBOARDXL',                
         27            :       'XL_HWTYPE_CANBOARDXL_PXI',            
         29            :       'XL_HWTYPE_VN2600',                    
         29            :       'XL_HWTYPE_VN2610',                    
         37            :       'XL_HWTYPE_VN3300',                    
         39            :       'XL_HWTYPE_VN3600',                    
         41            :       'XL_HWTYPE_VN7600',                    
         43            :       'XL_HWTYPE_CANCARDXLE',                
         45            :       'XL_HWTYPE_VN8900',                    
         47            :       'XL_HWTYPE_VN8950',                    
         53            :       'XL_HWTYPE_VN2640',                    
         55            :       'XL_HWTYPE_VN1610',                    
         57            :       'XL_HWTYPE_VN1630',                    
         59            :       'XL_HWTYPE_VN1640',                    
         61            :       'XL_HWTYPE_VN8970',                    
         63            :       'XL_HWTYPE_VN1611',                    
         61            :       'XL_HWTYPE_VT6204',                    
         65            :       'XL_HWTYPE_VN5610',                    
         67            :       'XL_HWTYPE_VN7570',                    
         69            :       'XL_HWTYPE_IPCLIENT'                  
    }
    
    TRANSCEIVER_TYPE_MSG = \
    {
         0x0000        :       'XL_TRANSCEIVER_TYPE_NONE',                     
         0x0001        :       'XL_TRANSCEIVER_TYPE_CAN_251',                  
         0x0002        :       'XL_TRANSCEIVER_TYPE_CAN_252',                  
         0x0003        :       'XL_TRANSCEIVER_TYPE_CAN_DNOPTO',               
         0x0005        :       'XL_TRANSCEIVER_TYPE_CAN_SWC_PROTO',            
         0x0006        :       'XL_TRANSCEIVER_TYPE_CAN_SWC',                  
         0x0007        :       'XL_TRANSCEIVER_TYPE_CAN_EVA',                  
         0x0008        :       'XL_TRANSCEIVER_TYPE_CAN_FIBER',                
         0x000B        :       'XL_TRANSCEIVER_TYPE_CAN_1054_OPTO',            
         0x000C        :       'XL_TRANSCEIVER_TYPE_CAN_SWC_OPTO',             
         0x000D        :       'XL_TRANSCEIVER_TYPE_CAN_B10011S',              
         0x000E        :       'XL_TRANSCEIVER_TYPE_CAN_1050',                 
         0x000F        :       'XL_TRANSCEIVER_TYPE_CAN_1050_OPTO',            
         0x0010        :       'XL_TRANSCEIVER_TYPE_CAN_1041',                 
         0x0011        :       'XL_TRANSCEIVER_TYPE_CAN_1041_OPTO',
         0x0016        :       'XL_TRANSCEIVER_VIRTUAL',           
         0x0017        :       'XL_TRANSCEIVER_TYPE_LIN_6258_OPTO',            
         0x0019        :       'XL_TRANSCEIVER_TYPE_LIN_6259_OPTO',            
         0x001D        :       'XL_TRANSCEIVER_TYPE_DAIO_8444_OPTO',           
         0x0021        :       'XL_TRANSCEIVER_TYPE_CAN_1041A_OPTO',
         0x0023        :       'XL_TRANSCEIVER_TYPE_LIN_6259_MAG',             
         0x0025        :       'XL_TRANSCEIVER_TYPE_LIN_7259_MAG',             
         0x0027        :       'XL_TRANSCEIVER_TYPE_LIN_7269_MAG',             
         0x0033        :       'XL_TRANSCEIVER_TYPE_CAN_1054_MAG',             
         0x0035        :       'XL_TRANSCEIVER_TYPE_CAN_251_MAG',              
         0x0037        :       'XL_TRANSCEIVER_TYPE_CAN_1050_MAG',             
         0x0039        :       'XL_TRANSCEIVER_TYPE_CAN_1040_MAG',             
         0x003B        :       'XL_TRANSCEIVER_TYPE_CAN_1041A_MAG',            
         0x0080        :       'XL_TRANSCEIVER_TYPE_TWIN_CAN_1041A_MAG',       
         0x0081        :       'XL_TRANSCEIVER_TYPE_TWIN_LIN_7269_MAG',        
         0x0082        :       'XL_TRANSCEIVER_TYPE_TWIN_CAN_1041AV2_MAG',     
         0x0083        :       'XL_TRANSCEIVER_TYPE_TWIN_CAN_1054_1041A_MAG',
         0x0101        :       'XL_TRANSCEIVER_TYPE_PB_CAN_251',         
         0x0103        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1054',        
         0x0105        :       'XL_TRANSCEIVER_TYPE_PB_CAN_251_OPTO',    
         0x010B        :       'XL_TRANSCEIVER_TYPE_PB_CAN_SWC',         
         0x0115        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1054_OPTO',   
         0x0117        :       'XL_TRANSCEIVER_TYPE_PB_CAN_SWC_OPTO',    
         0x0119        :       'XL_TRANSCEIVER_TYPE_PB_CAN_TT_OPTO',     
         0x011B        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1050',        
         0x011D        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1050_OPTO',   
         0x011F        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1041',        
         0x0121        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1041_OPTO',   
         0x0129        :       'XL_TRANSCEIVER_TYPE_PB_LIN_6258_OPTO',   
         0x012B        :       'XL_TRANSCEIVER_TYPE_PB_LIN_6259_OPTO',   
         0x012D        :       'XL_TRANSCEIVER_TYPE_PB_LIN_6259_MAG',    
         0x012F        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1041A_OPTO',  
         0x0131        :       'XL_TRANSCEIVER_TYPE_PB_LIN_7259_MAG',    
         0x0133        :       'XL_TRANSCEIVER_TYPE_PB_LIN_7269_MAG',    
         0x0135        :       'XL_TRANSCEIVER_TYPE_PB_CAN_251_MAG',     
         0x0136        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1050_MAG',    
         0x0137        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1040_MAG',    
         0x0138        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1041A_MAG',   
         0x0139        :       'XL_TRANSCEIVER_TYPE_PB_DAIO_8444_OPTO',  
         0x013B        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1054_MAG',    
         0x013C        :       'XL_TRANSCEIVER_TYPE_CAN_1051_CAP_FIX',   
         0x013D        :       'XL_TRANSCEIVER_TYPE_DAIO_1021_FIX',      
         0x013E        :       'XL_TRANSCEIVER_TYPE_LIN_7269_CAP_FIX',   
         0x013F        :       'XL_TRANSCEIVER_TYPE_PB_CAN_1051_CAP',    
         0x0140        :       'XL_TRANSCEIVER_TYPE_PB_CAN_SWC_7356_CAP',
         0x0201        :       'XL_TRANSCEIVER_TYPE_PB_FR_1080',     
         0x0202        :       'XL_TRANSCEIVER_TYPE_PB_FR_1080_MAG', 
         0x0203        :       'XL_TRANSCEIVER_TYPE_PB_FR_1080A_MAG',
         0x0204        :       'XL_TRANSCEIVER_TYPE_PB_FR_1082_CAP', 
         0x0205        :       'XL_TRANSCEIVER_TYPE_PB_FRC_1082_CAP',
         0x0220        :       'XL_TRANSCEIVER_TYPE_MOST150_ONBOARD',
         0x0280        :       'XL_TRANSCEIVER_TYPE_PB_DAIO_8642'                                   
    }
    
    BUS_TYPE_MSG = \
    {
         0x00000000    :       'XL_BUS_TYPE_NONE', 
         0x00000001    :       'XL_BUS_TYPE_CAN',
         0x00000002    :       'XL_BUS_TYPE_LIN',
         0x00000004    :       'XL_BUS_TYPE_FLEXRAY',
         0x00000010    :       'XL_BUS_TYPE_MOST',
         0x00000040    :       'XL_BUS_TYPE_DAIO',
         0x00000100    :       'XL_BUS_TYPE_J1708'  
    }
    
    IS_ON_BUS_MSG = \
    {
        0           :       'NO',
        1           :       'YES'
    }
    
    def xlLoadLibrary(self, fileIn = None):
        """
            Load of the *.dll file for Vector XL driver
        """
        if not os.path.exists(fileIn):
            print "[- Dll file not found at:  \'%s' -]"%fileIn
            return False
        
        try:
            self.oDll = ctypes.windll.LoadLibrary(fileIn)
        except:
            print "[- Unable to load DLL file -]"
            return False
        
        return True
    
    def xlOpenDriver(self):
        xlStatus = self.oDll.xlOpenDriver()
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            return True
        else:
            print "[- Error unable to open driver see vendor specific message below -]"
            print "[- %s -]"%self.DRIVER_STATUS_MSG[xlStatus]
            return False

    def xlCloseDriver(self):
        xlStatus = self.oDll.xlCloseDriver()
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            return True
        else:
            print self.DRIVER_STATUS_MSG[xlStatus]
            return False
    
    def xlSetApplConfig(self, appName = ctypes.c_char_p('xlCANControlApp'), appChannel = ctypes.c_uint(0),  hwType = ctypes.c_uint(HARDWARE_TYPE['XL_HWTYPE_VN1630']), hwIndex = ctypes.c_uint(0), hwChannel = ctypes.c_uint(0), busType = ctypes.c_uint(BUS_TYPE['XL_BUS_TYPE_CAN'])):
        self.oDll.xlSetApplConfig.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        xlStatus = self.oDll.xlSetApplConfig(appName, appChannel, hwType, hwIndex, hwChannel, busType)
        if xlStatus == self.DRIVER_STATUS['XL_SUCCESS']:
            return True
        else:
            print self.DRIVER_STATUS[xlStatus]
            return False        
    
    def xlGetApplConfig(self):
        #NOT YET ADDED
        pass
    
    def xlGetDriverConfig(self, oXLdriverConfig = None):
        if(oXLdriverConfig == None):
            oXLdriverConfig = XLdriverConfig()
        self.oDll.xlGetDriverConfig.argtypes = [ctypes.POINTER(XLdriverConfig)]
        xlStatus = self.oDll.xlGetDriverConfig(ctypes.pointer(oXLdriverConfig))
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            self.XLdriverConfig = oXLdriverConfig
            return self.XLdriverConfig
        else:
            print "[- Error unable to get driver configuration see vendor specific message below -]"
            print "[- %s -]"%self.DRIVER_STATUS_MSG[xlStatus]
            return False
    
    def xlGetChannelIndex(self, hwType = ctypes.c_int(HARDWARE_TYPE['XL_HWTYPE_VN1630']), hwIndex = ctypes.c_int(-1), hwChannel = ctypes.c_int(-1)):
        """
            Gets the channel index of a specific hardware channel.
            
            :INPUT:    
            :param: hwType: Required to distinguish the different hardware types e.g. XL_HWTYPE_VN1630, XL_HWTYPE_CANCASEXL ... -1 Can be used of the hardware type dosen't matter 
            :type: hwType: int
            :param: hwIndex: Required to distinguish between two or more devices of the same hardware type 0, 1, 2... -1 can be used to retrieve the first available hardware       
            :type: hwIndex: int
            :param: hwChannel: Required to distinguish the hardware channel of the selected device 0, 1, 2... -1 can be used to retrieve the first available channel
            :type: hwChannel: int         
                      
            
            :OUTPUT:   
            :param: channelIndex: The channel index. If -1 is returned the channel was not found.
            :type: channelIndex: int
        """
        self.oDll.xlGetChannelIndex.argtype = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        channelIndex = self.oDll.xlGetChannelIndex(hwType, hwIndex, hwChannel)
        if channelIndex == -1 :
            print 'Channel not found'
            return False
        else:
            return channelIndex
        
    def xlGetChannelMask(self, hwType = ctypes.c_int(HARDWARE_TYPE['XL_HWTYPE_VN1630']), hwIndex = ctypes.c_int(-1), hwChannel = ctypes.c_int(-1)):
        '''
            Gets the channel mask of a specific hardware channel.
            
            Input:    hwType         Required to distinguish the different 
                                     hardware types e.g. 
                                     XL_HWTYPE_VN1630, XL_HWTYPE_CANCASEXL ... 
                                     -1 Can be used of the hardware type dosen't 
                                     matter
                      hwIndex        Required to distinguish between two or more devices of the same hardware type 0, 1, 2... -1 can be used to retrieve the first available hardware
                      hwChannel      Required to distinguish the hardware channel of the selected device 0, 1, 2... -1 can be used to retrieve the first available channel
            
            Output:   channelMask   The channel mask. If 0 is returned the channel was not found.
        '''
        self.oDll.xlGetChannelMask.argtype = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.oDll.xlGetChannelMask.restype = XLaccess
        channelMask = self.oDll.xlGetChannelMask(hwType, hwIndex, hwChannel)
        if channelMask == 0:
            print 'Unable to get channel mask'
            return False
        else:
            return channelMask
    
    def xlOpenPort(self, portHandle = XLportHandle(XL_INVALID_PORTHANDLE), userName = ctypes.c_char_p('xlCANControlApp'), accessMask = XLaccess(1), permissionMask = XLaccess(1), rxQueueSize = ctypes.c_uint(256), xlInterfaceVersion = ctypes.c_uint(XL_INTERFACE_VERSION), busType = ctypes.c_uint(BUS_TYPE['XL_BUS_TYPE_CAN'])):
        self.oDll.xlOpenPort.argtype = [ctypes.POINTER(XLportHandle), ctypes.c_char_p, XLaccess, ctypes.POINTER(XLaccess), ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        xlStatus = self.oDll.xlOpenPort(ctypes.byref(portHandle), userName, accessMask, ctypes.byref(permissionMask), rxQueueSize, xlInterfaceVersion, busType)
        if xlStatus == self.DRIVER_STATUS['XL_SUCCESS']:
            return portHandle, permissionMask
        else:
            print self.DRIVER_STATUS_MSG[xlStatus]
            
    def xlClosePort(self, portHandel = XLportHandle(XL_INVALID_PORTHANDLE)):
        self.oDll.xlClosePort.argtype = [XLportHandle]
        xlStatus = self.oDll.xlClosePort(portHandel)
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            return True
        else:
            print self.DRIVER_STATUS_MSG[xlStatus]
    
    def xlActivateChannel(self, portHandle, accessMask = XLaccess(1), busType = ctypes.c_uint(BUS_TYPE['XL_BUS_TYPE_CAN']), flags = ctypes.c_uint(XL_ACTIVATE_RESET_CLOCK)):
        self.oDll.xlActivateChannel.argTypes = [XLportHandle, XLaccess, ctypes.c_uint, ctypes.c_uint]
        xlStatus = self.oDll.xlActivateChannel(portHandle, accessMask, busType, flags)
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            return True
        else:
            print self.DRIVER_STATUS_MSG[xlStatus]
            return False
  
    def xlReceive(self, portHandle, pEventCount, pEventList):
        '''
            Reads the received events out of the message queue. An application 
            should read all available messages to be sure to re-enable the event. 
        '''
        #This row dose not work reason is yet unknown JN.
        #self.oDll.xlReceive.argTypes = [XLportHandle, POINTER(c_uint), POINTER(XLevent)]
        xlStatus = self.oDll.xlReceive(portHandle, ctypes.byref(pEventCount), ctypes.byref(pEventList))
        if xlStatus == self.DRIVER_STATUS['XL_SUCCESS']:
            return pEventList
        else:
            if xlStatus != self.DRIVER_STATUS['XL_ERR_QUEUE_IS_EMPTY']:
                print self.DRIVER_STATUS_MSG[xlStatus]
                return False
           
    def xlDeactivateChannel(self, portHandle, accessMask = XLaccess(1)):
        self.oDll.xlDeactivateChannel.argTypes = [XLportHandle, XLaccess]
        xlStatus = self.oDll.xlDeactivateChannel(portHandle, accessMask)
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            return True
        else:
            print self.DRIVER_STATUS_MSG[xlStatus]
    
    def xlPrintDriverConfig(self, channelsIn = None):
        self.xlGetDriverConfig()
        print '--------------------------------------------------------\n'
        print 'DLL Version:', self.XLdriverConfig.dllVersion
        print 'Channel Count:', self.XLdriverConfig.channelCount, '\n'
        print '--------------------------------------------------------'
        
        if channelsIn == None:
            channelsIn = self.XLdriverConfig.channelCount
            
        for i in range(channelsIn):
            print 'Channel:','[',i,']'
            print 'Name:', self.XLdriverConfig.Channel[i].name
            print 'hwType:', self.HARDWARE_TYPE_MSG[self.XLdriverConfig.Channel[i].hwType]
            print 'hwIndex:', self.XLdriverConfig.Channel[i].hwIndex
            print 'hwChannel:', self.XLdriverConfig.Channel[i].hwChannel
            print 'transceiverType:', self.TRANSCEIVER_TYPE_MSG[self.XLdriverConfig.Channel[i].transceiverType]
            print 'transceiverState:', self.XLdriverConfig.Channel[i].transceiverState
            print 'channelIndex:', self.XLdriverConfig.Channel[i].channelIndex
            print 'channelMask: 0x%(mask)02x' % {"mask" : self.XLdriverConfig.Channel[i].channelMask}
            print 'channelCapabilities:', self.XLdriverConfig.Channel[i].channelCapabilities
            print 'channelBusCapabilities:', self.XLdriverConfig.Channel[i].channelBusCapabilities
            print 'isOnBus:', self.IS_ON_BUS_MSG[self.XLdriverConfig.Channel[i].isOnBus]
            print 'connectedBusType:', self.BUS_TYPE_MSG[self.XLdriverConfig.Channel[i].connectedBusType]
            print 'busParams:'
            print '\t busType:', self.BUS_TYPE_MSG[self.XLdriverConfig.Channel[i].busParams.busType]
            print '\t bitRate:', self.XLdriverConfig.Channel[i].busParams.data.can.bitRate
            print '\t sjw:', self.XLdriverConfig.Channel[i].busParams.data.can.sjw
            print '\t tseg1:', self.XLdriverConfig.Channel[i].busParams.data.can.tseg1
            print '\t tseg2:', self.XLdriverConfig.Channel[i].busParams.data.can.tseg2
            print '\t sam:', self.XLdriverConfig.Channel[i].busParams.data.can.sam
            print '\t outputMode:', self.XLdriverConfig.Channel[i].busParams.data.can.outputMode     
            print 'driverVersion:', self.XLdriverConfig.Channel[i].driverVersion
            print 'interfaceVersion:', self.XLdriverConfig.Channel[i].interfaceVersion
            print 'raw_data:', self.XLdriverConfig.Channel[i].raw_data 
            print 'serialNumber:', self.XLdriverConfig.Channel[i].serialNumber
            print 'articleNumber:', self.XLdriverConfig.Channel[i].articleNumber
            print 'transceiverName:', self.XLdriverConfig.Channel[i].transceiverName
            print 'specialCabFlags:', self.XLdriverConfig.Channel[i].specialCabFlags
            print 'dominantTimeout:', self.XLdriverConfig.Channel[i].dominantTimeout, '\n'
            print '************* Next Channel **************\n'

    def xlGetErrorString(self, XLstatus = None):
        self.oDll.xlGetErrorString.restype = ctypes.c_char_p
        sText = self.oDll.xlGetErrorString(XLstatus)
        print sText
        
    def xlCanSetChannelParams(self, portHandle, accessMask = XLaccess(1), oXLchipParams = None):
        '''
            TODO: Add input variables to method so that it can be feed into the struct.
        '''
        if(oXLchipParams == None):
            oXLchipParams = XLchipParams()
        self.oDll.xlCanSetChannelParams.argTypes = [XLportHandle, XLaccess, ctypes.POINTER(XLchipParams)]
        xlStatus = self.oDllxlCanSetChannelParams(portHandle, accessMask, ctypes.pointer(oXLchipParams))
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            self.XLchipParams = oXLchipParams
            return True
        else:
            print self.DRIVER_STATUS_MSG[xlStatus]
            return False
        
    def xlCanSetChannelBitrate(self, portHandle, accessMask = XLaccess(1), bitrate = ctypes.c_ulong(500000)):
        self.oDll.xlCanSetChannelBitrate.argTypes = [XLportHandle, XLaccess, ctypes.c_ulong]
        xlStatus = self.oDll.xlCanSetChannelBitrate(portHandle, accessMask, bitrate)
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            return True
        else:
            print self.DRIVER_STATUS_MSG[xlStatus]
            return False
    
    def xlCanTransmit(self, portHandle, accessMask, messageCount, pMessages):
        '''
            This method is transmitts a message onto CAN.
            
        '''
        self.oDll.xlCanTransmit.argTypes = [XLportHandle, accessMask, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_void_p) ]
        xlStatus = self.oDll.xlCanTransmit(portHandle, accessMask, ctypes.byref(messageCount), ctypes.byref(pMessages))
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            return True
        else:
            print self.DRIVER_STATUS_MSG[xlStatus]
            return False