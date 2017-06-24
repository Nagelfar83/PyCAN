'''
Created on 13 Jun 2017

@author: nagelfar
'''

import ctypes

# GENERAL DEFINES
MAX_MSG_LEN = 8
XL_MAX_LENGTH = 31
XL_ACTIVATE_NONE = 0
XL_INVALID_PORTHANDLE = -1
XL_CONFIG_MAX_CHANNELS = 64
XL_ACTIVATE_RESET_CLOCK = 8

# INTERFACE VERSION DEFINES
XL_INTERFACE_VERSION_V2 = 2
XL_INTERFACE_VERSION_V3 = 3
XL_INTERFACE_VERSION_V4 = 4
XL_INTERFACE_VERSION = XL_INTERFACE_VERSION_V3

# GENERAL CAN MSG DEFINES
XL_CAN_MSG_FLAG_ERROR_FRAME = 1
XL_CAN_MSG_FLAG_OVERRUN = 2          # Overrun in Driver or CAN Controller, previous msgs have been lost.
XL_CAN_MSG_FLAG_NERR = 4             # Line Error on Lowspeed
XL_CAN_MSG_FLAG_WAKEUP = 8           # High Voltage Message on Single Wire CAN
XL_CAN_MSG_FLAG_REMOTE_FRAME = 16
XL_CAN_MSG_FLAG_RESERVED_1 = 32
XL_CAN_MSG_FLAG_TX_COMPLETED = 64    # Message Transmitted
XL_CAN_MSG_FLAG_TX_REQUEST = 128     # Transmit Message stored into Controller
XL_CAN_MSG_FLAG_SRR_BIT_DOM = 512    # SRR bit in CAN message is dominant

# GENERAL XL EVENT DEFINES
XL_EVENT_FLAG_OVERRUN = 1            # Used in XLevent.flags

# GENERAL DAIO DEFINES
XL_DAIO_DATA_GET = 0x8000            # (32760)
XL_DAIO_DATA_VALUE_DIGITAL = 0x0001  # (1)
XL_DAIO_DATA_VALUE_ANALOG = 0x0002   # (2)
XL_DAIO_DATA_PWM = 0x0010            # (16)
XL_DAIO_MODE_PULSE0 = 0x0020         # (32) Generates pulse in values of PWM
XL_DAIO_TRIGGER_LEVEL_NONE = 0       # no trigger level is defined
XL_DAIO_POLLING_NONE = 0             # periodic measurement is disabled

XL_TRANSCEIVER_STATUS_PRESENT = ctypes.c_uint(0x0001)
XL_TRANSCEIVER_STATUS_POWER = ctypes.c_uint(0x0002)
XL_TRANSCEIVER_STATUS_MEMBLANK = ctypes.c_uint(0x0004)
XL_TRANSCEIVER_STATUS_MEMCORRUPT = ctypes.c_uint(0x0008)
XL_TRANSCEIVER_STATUS_POWER_GOOD = ctypes.c_uint(0x0010)
XL_TRANSCEIVER_STATUS_EXT_POWER_GOOD = ctypes.c_uint(0x0020)
XL_TRANSCEIVER_STATUS_NOT_SUPPORTED = ctypes.c_uint(0x0040)

XLuint64 = ctypes.c_longlong
XLaccess = XLuint64
XLportHandle = ctypes.c_long
XLeventTag = ctypes.c_ubyte


class s_xl_can_msg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ulong),
                ("flags", ctypes.c_ushort),
                ("dlc", ctypes.c_ushort),
                ("res1", XLuint64),
                ("data", ctypes.c_ubyte * MAX_MSG_LEN)]


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
                ("data", ctypes.c_ubyte * 8),
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
                ("value_analog", ctypes.c_ubyte * 4),
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
    _fields_ = [("tag", XLeventTag),
                ("chanIndex", ctypes.c_ubyte),
                ("transId", ctypes.c_ushort),
                ("portHandle", ctypes.c_ushort),
                ("reserved", ctypes.c_ushort),
                ("timeStamp", XLuint64),
                ("tagData", s_xl_tag_data)]


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
                ("padding", ctypes.c_ubyte * 32)]


class XLbusParams(ctypes.Structure):
    _fields_ = [("busType", ctypes.c_uint),
                ("data", union)]


class XLchannelConfig(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("name", ctypes.c_char * (XL_MAX_LENGTH + 1)),
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
                ("raw_data", ctypes.c_uint * 10),
                ("serialNumber", ctypes.c_uint),
                ("articleNumber", ctypes.c_uint),
                ("transceiverName", ctypes.c_char * (XL_MAX_LENGTH + 1)),
                ("specialCabFlags", ctypes.c_uint),
                ("dominantTimeout", ctypes.c_uint),
                ("reserved", ctypes.c_uint * 8)]


class XLdriverConfig(ctypes.Structure):
    _fields_ = [("dllVersion", ctypes.c_uint),
                ("channelCount", ctypes.c_uint),
                ("reserved", ctypes.c_uint * 10),
                ("Channel", XLchannelConfig * XL_CONFIG_MAX_CHANNELS)]


BUS_TYPE = {
    'XL_BUS_TYPE_NONE':     0x00000000,  # No bus
    'XL_BUS_TYPE_CAN':      0x00000001,  # CAN
    'XL_BUS_TYPE_LIN':      0x00000002,  # LIN
    'XL_BUS_TYPE_FLEXRAY':  0x00000004,  # FLEXRAY
    'XL_BUS_TYPE_AFDX':     0x00000008,  # Former BUS_TYPE_BEAN
    'XL_BUS_TYPE_MOST':     0x00000010,  # MOST
    'XL_BUS_TYPE_DAIO':     0x00000040,  # IO cab/piggy (Digital In/Out)
    'XL_BUS_TYPE_J1708':    0x00000100,  # J1708
    'XL_BUS_TYPE_ETHERNET': 0x00001000,  # ETHERNET
    'XL_BUS_TYPE_A429':     0x00002000   # A429
}

TRANSCEIVER_TYPE = {
    'XL_TRANSCEIVER_TYPE_NONE':                     0x0000,
    'XL_TRANSCEIVER_TYPE_CAN_251':                  0x0001,
    'XL_TRANSCEIVER_TYPE_CAN_252':                  0x0002,
    'XL_TRANSCEIVER_TYPE_CAN_DNOPTO':               0x0003,
    'XL_TRANSCEIVER_TYPE_CAN_SWC_PROTO':            0x0005,  # Prototype. Driver may latch-up.
    'XL_TRANSCEIVER_TYPE_CAN_SWC':                  0x0006,
    'XL_TRANSCEIVER_TYPE_CAN_EVA':                  0x0007,
    'XL_TRANSCEIVER_TYPE_CAN_FIBER':                0x0008,
    'XL_TRANSCEIVER_TYPE_CAN_1054_OPTO':            0x000B,  # 1054 with optical isolation
    'XL_TRANSCEIVER_TYPE_CAN_SWC_OPTO':             0x000C,  # SWC with optical isolation
    'XL_TRANSCEIVER_TYPE_CAN_B10011S':              0x000D,  # B10011S truck-and-trailer
    'XL_TRANSCEIVER_TYPE_CAN_1050':                 0x000E,  # 1050
    'XL_TRANSCEIVER_TYPE_CAN_1050_OPTO':            0x000F,  # 1050 with optical isolation
    'XL_TRANSCEIVER_TYPE_CAN_1041':                 0x0010,  # 1041
    'XL_TRANSCEIVER_TYPE_CAN_1041_OPTO':            0x0011,  # 1041 with optical isolation
    'XL_TRANSCEIVER_TYPE_CAN_VIRTUAL':              0x0016,  # Virtual CAN Trasceiver for Virtual CAN Bus Driver
    'XL_TRANSCEIVER_TYPE_LIN_6258_OPTO':            0x0017,  # Vector LINcab 6258opto with transceiver Infineon TLE6258
    'XL_TRANSCEIVER_TYPE_LIN_6259_OPTO':            0x0019,  # Vector LINcab 6259opto with transceiver Infineon TLE6259
    'XL_TRANSCEIVER_TYPE_DAIO_8444_OPTO':           0x001D,  # Vector IOcab 8444  (8 dig.Inp.; 4 dig.Outp.; 4 ana.Inp.; 4 ana.Outp.)
    'XL_TRANSCEIVER_TYPE_CAN_1041A_OPTO':           0x0021,  # 1041A with optical isolation
    'XL_TRANSCEIVER_TYPE_LIN_6259_MAG':             0x0023,  # LIN transceiver 6259, with transceiver Infineon TLE6259, magnetically isolated, stress functionality
    'XL_TRANSCEIVER_TYPE_LIN_7259_MAG':             0x0025,  # LIN transceiver 7259, with transceiver Infineon TLE7259, magnetically isolated, stress functionality
    'XL_TRANSCEIVER_TYPE_LIN_7269_MAG':             0x0027,  # LIN transceiver 7269, with transceiver Infineon TLE7269, magnetically isolated, stress functionality
    'XL_TRANSCEIVER_TYPE_CAN_1054_MAG':             0x0033,  # TJA1054, magnetically isolated, with selectable termination resistor (via 4th IO line)
    'XL_TRANSCEIVER_TYPE_CAN_251_MAG':              0x0035,  # 82C250/251 or equivalent, magnetically isolated
    'XL_TRANSCEIVER_TYPE_CAN_1050_MAG':             0x0037,  # TJA1050, magnetically isolated
    'XL_TRANSCEIVER_TYPE_CAN_1040_MAG':             0x0039,  # TJA1040, magnetically isolated
    'XL_TRANSCEIVER_TYPE_CAN_1041A_MAG':            0x003B,  # TJA1041A, magnetically isolated
    'XL_TRANSCEIVER_TYPE_TWIN_CAN_1041A_MAG':       0x0080,  # TWINcab with two TJA1041, magnetically isolated
    'XL_TRANSCEIVER_TYPE_TWIN_LIN_7269_MAG':        0x0081,  # TWINcab with two 7259, Infineon TLE7259, magnetically isolated, stress functionality
    'XL_TRANSCEIVER_TYPE_TWIN_CAN_1041AV2_MAG':     0x0082,  # TWINcab with two TJA1041, magnetically isolated
    'XL_TRANSCEIVER_TYPE_TWIN_CAN_1054_1041A_MAG':  0x0083,  # TWINcab with TJA1054A and TJA1041A with magnetic isolation
    'XL_TRANSCEIVER_TYPE_PB_CAN_251':               0x0101,
    'XL_TRANSCEIVER_TYPE_PB_CAN_1054':              0x0103,
    'XL_TRANSCEIVER_TYPE_PB_CAN_251_OPTO':          0x0105,
    'XL_TRANSCEIVER_TYPE_PB_CAN_SWC':               0x010B,
    'XL_TRANSCEIVER_TYPE_PB_CAN_1054_OPTO':         0x0115,
    'XL_TRANSCEIVER_TYPE_PB_CAN_SWC_OPTO':          0x0117,
    'XL_TRANSCEIVER_TYPE_PB_CAN_TT_OPTO':           0x0119,
    'XL_TRANSCEIVER_TYPE_PB_CAN_1050':              0x011B,
    'XL_TRANSCEIVER_TYPE_PB_CAN_1050_OPTO':         0x011D,
    'XL_TRANSCEIVER_TYPE_PB_CAN_1041':              0x011F,
    'XL_TRANSCEIVER_TYPE_PB_CAN_1041_OPTO':         0x0121,
    'XL_TRANSCEIVER_TYPE_PB_LIN_6258_OPTO':         0x0129,  # LIN piggy back with transceiver Infineon TLE6258
    'XL_TRANSCEIVER_TYPE_PB_LIN_6259_OPTO':         0x012B,  # LIN piggy back with transceiver Infineon TLE6259
    'XL_TRANSCEIVER_TYPE_PB_LIN_6259_MAG':          0x012D,  # LIN piggy back with transceiver Infineon TLE6259, magnetically isolated, stress functionality
    'XL_TRANSCEIVER_TYPE_PB_CAN_1041A_OPTO':        0x012F,  # CAN transceiver 1041A
    'XL_TRANSCEIVER_TYPE_PB_LIN_7259_MAG':          0x0131,  # LIN piggy back with transceiver Infineon TLE7259, magnetically isolated, stress functionality
    'XL_TRANSCEIVER_TYPE_PB_LIN_7269_MAG':          0x0133,  # LIN piggy back with transceiver Infineon TLE7269, magnetically isolated, stress functionality
    'XL_TRANSCEIVER_TYPE_PB_CAN_251_MAG':           0x0135,  # 82C250/251 or compatible, magnetically isolated
    'XL_TRANSCEIVER_TYPE_PB_CAN_1050_MAG':          0x0136,  # TJA 1050, magnetically isolated
    'XL_TRANSCEIVER_TYPE_PB_CAN_1040_MAG':          0x0137,  # TJA 1040, magnetically isolated
    'XL_TRANSCEIVER_TYPE_PB_CAN_1041A_MAG':         0x0138,  # TJA 1041A, magnetically isolated
    'XL_TRANSCEIVER_TYPE_PB_DAIO_8444_OPTO':        0x0139,  # optically isolated IO piggy
    'XL_TRANSCEIVER_TYPE_PB_CAN_1054_MAG':          0x013B,  # TJA1054, magnetically isolated, with selectable termination resistor (via 4th IO line)
    'XL_TRANSCEIVER_TYPE_CAN_1051_CAP_FIX':         0x013C,  # TJA1051 - fixed transceiver on e.g. 16xx/8970
    'XL_TRANSCEIVER_TYPE_DAIO_1021_FIX':            0x013D,  # Onboard IO of VN1630/VN1640
    'XL_TRANSCEIVER_TYPE_LIN_7269_CAP_FIX':         0x013E,  # TLE7269 - fixed transceiver on 1611
    'XL_TRANSCEIVER_TYPE_PB_CAN_1051_CAP':          0x013F,  # TJA 1051, capacitive isolated
    'XL_TRANSCEIVER_TYPE_PB_CAN_SWC_7356_CAP':      0x0140,  # Single Wire NCV7356, capacitive isolated
    'XL_TRANSCEIVER_TYPE_PB_CAN_1055_CAP':          0x0141,  # TJA1055, capacitive isolated, with selectable termination resistor (via 4th IO line)
    'XL_TRANSCEIVER_TYPE_PB_CAN_1057_CAP':          0x0142,  # TJA 1057, capacitive isolated
    'XL_TRANSCEIVER_TYPE_A429_HOLT8596_FIX':        0x0143,  # Onboard HOLT 8596 TX transceiver on VN0601
    'XL_TRANSCEIVER_TYPE_A429_HOLT8455_FIX':        0x0144,  # Onboard HOLT 8455 RX transceiver on VN0601
    'XL_TRANSCEIVER_TYPE_PB_FR_1080':               0x0201,  # TJA 1080
    'XL_TRANSCEIVER_TYPE_PB_FR_1080_MAG':           0x0202,  # TJA 1080 magnetically isolated piggy
    'XL_TRANSCEIVER_TYPE_PB_FR_1080A_MAG':          0x0203,  # TJA 1080A magnetically isolated piggy
    'XL_TRANSCEIVER_TYPE_PB_FR_1082_CAP':           0x0204,  # TJA 1082 capacitive isolated piggy
    'XL_TRANSCEIVER_TYPE_PB_FRC_1082_CAP':          0x0205,  # TJA 1082 capacitive isolated piggy with CANpiggy form factor
    'XL_TRANSCEIVER_TYPE_FR_1082_CAP_FIX':          0x0206,  # TJA 1082 capacitive isolated piggy fixed transceiver - e.g. 7610
    'XL_TRANSCEIVER_TYPE_MOST150_ONBOARD':          0x0220,  # Onboard MOST150 transceiver of VN2640
    'XL_TRANSCEIVER_TYPE_ETH_BCM54810_FIX':         0x0230,  # Onboard Broadcom Ethernet PHY on VN5610 and VX0312
    'XL_TRANSCEIVER_TYPE_ETH_AR8031_FIX':           0x0231,  # Onboard Atheros Ethernet PHY
    'XL_TRANSCEIVER_TYPE_ETH_BCM89810_FIX':         0x0232,  # Onboard Broadcom Ethernet PHY
    'XL_TRANSCEIVER_TYPE_ETH_TJA1100_FIX':          0x0233,  # Onboard NXP Ethernet PHY
    'XL_TRANSCEIVER_TYPE_ETH_BCM54810_89811_FIX':   0x0234,  # Onboard Broadcom Ethernet PHYs (e.g. VN5610A - BCM54810: RJ45, BCM89811: DSUB)
    'XL_TRANSCEIVER_TYPE_PB_DAIO_8642':             0x0280,  # Iopiggy for VN8900
    'XL_TRANSCEIVER_TYPE_DAIO_AL_ONLY':             0x028f,  # virtual piggy type for activation line only (e.g. VN8810ini)
    'XL_TRANSCEIVER_TYPE_DAIO_1021_FIX_WITH_AL':    0x0290,  # On board IO with Activation Line (e.g. VN5640)
    'XL_TRANSCEIVER_TYPE_DAIO_AL_WU':               0x0291   # virtual piggy type for activation line and WakeUp Line only (e.g. VN5610A)
}

TRANSCEIVER_STATE = {
    'XL_TRANSCEIVER_STATUS_PRESENT':        0x0001,
    'XL_TRANSCEIVER_STATUS_POWER':          0x0002,
    'XL_TRANSCEIVER_STATUS_MEMBLANK':       0x0004,
    'XL_TRANSCEIVER_STATUS_MEMCORRUPT':     0x0008,
    'XL_TRANSCEIVER_STATUS_POWER_GOOD':     0x0010,
    'XL_TRANSCEIVER_STATUS_EXT_POWER_GOOD': 0x0020,
    'XL_TRANSCEIVER_STATUS_NOT_SUPPORTED':  0x0040
}

DRIVER_STATUS = {
    'XL_SUCCESS':                   0,
    'XL_PENDING':                   1,
    'XL_ERR_QUEUE_IS_EMPTY':        10,
    'XL_ERR_QUEUE_IS_FULL':         11,
    'XL_ERR_TX_NOT_POSSIBLE':       12,
    'XL_ERR_NO_LICENSE':            14,
    'XL_ERR_WRONG_PARAMETER':       101,
    'XL_ERR_TWICE_REGISTER':        110,
    'XL_ERR_INVALID_CHAN_INDEX':    111,
    'XL_ERR_INVALID_ACCESS':        112,
    'XL_ERR_PORT_IS_OFFLINE':       113,
    'XL_ERR_CHAN_IS_ONLINE':        116,
    'XL_ERR_NOT_IMPLEMENTED':       117,
    'XL_ERR_INVALID_PORT':          118,
    'XL_ERR_HW_NOT_READY':          120,
    'XL_ERR_CMD_TIMEOUT':           121,
    'XL_ERR_HW_NOT_PRESENT':        129,
    'XL_ERR_NOTIFY_ALREADY_ACTIVE': 131,
    'XL_ERR_NO_RESOURCES':          152,
    'XL_ERR_WRONG_CHIP_TYPE':       153,
    'XL_ERR_WRONG_COMMAND':         154,
    'XL_ERR_INVALID_HANDLE':        155,
    'XL_ERR_RESERVED_NOT_ZERO':     157,
    'XL_ERR_INIT_ACCESS_MISSING':   158,
    'XL_ERR_CANNOT_OPEN_DRIVER':    201,
    'XL_ERR_WRONG_BUS_TYPE':        202,
    'XL_ERR_DLL_NOT_FOUND':         203,
    'XL_ERR_INVALID_CHANNEL_MASK':  204,
    'XL_ERR_CONNECTION_BROKEN':     210,
    'XL_ERR_CONNECTION_CLOSED':     211,
    'XL_ERR_INVALID_STREAM_NAME':   212,
    'XL_ERR_CONNECTION_FAILED':     213,
    'XL_ERR_STREAM_NOT_FOUND':      214,
    'XL_ERR_STREAM_NOT_CONNECTED':  215,
    'XL_ERR_QUEUE_OVERRUN':         216,
    'XL_ERROR':                     255
}

EVENT_TAGS = {
    'XL_NO_COMMAND':                0,
    'XL_RECEIVE_MSG':               1,
    'XL_CHIP_STATE':                3,
    'XL_TRANSCEIVER_INFO':          6,
    'XL_TRANSCEIVER':               6,  # Same as XL_TRANSCEIVER_INFO
    'XL_TIMER_EVENT':               8,
    'XL_TIMER':                     8,  # Same as XL_TIMER_EVENT
    'XL_TRANSMIT_MSG':              10,
    'XL_SYNC_PULSE':                11,
    'XL_APPLICATION_NOTIFICATION':  15,
    'LIN_MSG':                      20,
    'LIN_ERRMSG':                   21,
    'LIN_SYNCERR':                  22,
    'LIN_NOANS':                    23,
    'LIN_WAKEUP':                   24,
    'LIN_SLEEP':                    25,
    'LIN_CRCINFO':                  26,
    'RECEIVE_DAIO_DATA':            32,
    'XL_RECEIVE_DAIO_PIGGY':        34
}  # TODO: Add XL_FR_XX for FlexRay

APPLICATION_NOTIFICATION = {
    'XL_NOTIFY_REASON_CHANNEL_ACTIVATION':      1,
    'XL_NOTIFY_REASON_CHANNEL_DEACTIVATION':    2,
    'XL_NOTIFY_REASON_PORT_CLOSED':             3
}

HARDWARE_TYPE = {
    'XL_HWTYPE_NONE':                   0,
    'XL_HWTYPE_VIRTUAL':                1,
    'XL_HWTYPE_CANCARDX':               2,
    'XL_HWTYPE_CANAC2PCI':              6,
    'XL_HWTYPE_CANCARDY':               12,
    'XL_HWTYPE_CANCARDXL':              15,
    'XL_HWTYPE_CANCASEXL':              21,
    'XL_HWTYPE_CANCASEXL_LOG_OBSOLETE': 23,
    'XL_HWTYPE_CANBOARDXL':             25,  # CANboardXL, CANboardXL PCIe
    'XL_HWTYPE_CANBOARDXL_PXI':         27,  # CANboardXL pxi
    'XL_HWTYPE_VN2600':                 29,
    'XL_HWTYPE_VN2610':                 29,  # Same as XL_HWTYPE_VN2600
    'XL_HWTYPE_VN3300':                 37,
    'XL_HWTYPE_VN3600':                 39,
    'XL_HWTYPE_VN7600':                 41,
    'XL_HWTYPE_CANCARDXLE':             43,
    'XL_HWTYPE_VN8900':                 45,
    'XL_HWTYPE_VN8950':                 47,
    'XL_HWTYPE_VN2640':                 53,
    'XL_HWTYPE_VN1610':                 55,
    'XL_HWTYPE_VN1630':                 57,
    'XL_HWTYPE_VN1640':                 59,
    'XL_HWTYPE_VN8970':                 61,
    'XL_HWTYPE_VN1611':                 63,
    'XL_HWTYPE_VN5610':                 65,
    'XL_HWTYPE_VN7570':                 67,
    'XL_HWTYPE_IPCLIENT':               69,
    'XL_HWTYPE_IPSERVER':               71,
    'XL_HWTYPE_VX1121':                 73,
    'XL_HWTYPE_VX1131':                 75,
    'XL_HWTYPE_VT6204':                 77,
    'XL_HWTYPE_VN1630_LOG':             79,
    'XL_HWTYPE_VN7610':                 81,
    'XL_HWTYPE_VN7572':                 83,
    'XL_HWTYPE_VN8972':                 85,
    'XL_HWTYPE_VN0601':                 87,
    'XL_HWTYPE_VX0312':                 91,
    'XL_HWTYPE_VN8800':                 95,
    'XL_HWTYPE_IPCL8800':               96,
    'XL_HWTYPE_IPSRV8800':              97,
    'XL_HWTYPE_CSMCAN':                 98,
    'XL_HWTYPE_VN5610A':                101,
    'XL_HWTYPE_VN7640':                 102,
    'XL_MAX_HWTYPE':                    102
}

CHIP_STATE = {
    'XL_CHIPSTAT_BUSOFF':           0x01,
    'XL_CHIPSTAT_ERROR_PASSIVE':    0x02,
    'XL_CHIPSTAT_ERROR_WARNING':    0x04,
    'XL_CHIPSTAT_ERROR_ACTIVE':     0x08
}

TRANSIVER_STATE = {
    'XL_TRANSCEIVER_EVENT_NONE':            0,
    'XL_TRANSCEIVER_EVENT_INSERTED':        1,
    'XL_TRANSCEIVER_EVENT_REMOVED':         2,
    'XL_TRANSCEIVER_EVENT_STATE_CHANGE':    3
}

OUTPUT_MODE = {
    'XL_OUTPUT_MODE_SILENT':            0,
    'XL_OUTPUT_MODE_NORMAL':            1,
    'XL_OUTPUT_MODE_TX_OFF':            2,
    'XL_OUTPUT_MODE_SJA_1000_SILENT':   3
}

TRANSCEIVER_MODE = {
    'XL_TRANSCEIVER_EVENT_ERROR':   1,
    'XL_TRANSCEIVER_EVENT_CHANGED': 2
}

DAIO_DIGITAL = {
    'XL_DAIO_DIGITAL_ENABLED':  1,  # digital port is enable
    'XL_DAIO_DIGITAL_INPUT':    2,  # digital port is input, otherwise it is an output
    'XL_DAIO_DIGITAL_TRIGGER':  4   # digital port is trigger
}

DAIO_ANALOG = {
    'XL_DAIO_ANALOG_ENABLED':   1,  # analog port is enable
    'XL_DAIO_ANALOG_INPUT':     2,  # analog port is input, otherwise it is an output
    'XL_DAIO_ANALOG_TRIGGER':   4,  # analog port is trigger
    'XL_DAIO_ANALOG_RANGE_32V': 8   # analog port is in range 0..32,768V, otherwise 0..8,192V
}

DAIO_TRIGGER_MODE = {
    'XL_DAIO_TRIGGER_MODE_NONE':                0,  # no trigger configured
    'XL_DAIO_TRIGGER_MODE_DIGITAL':             1,  # trigger on preconfigured digital lines
    'XL_DAIO_TRIGGER_MODE_ANALOG_ASCENDING':    2,  # trigger on input 3 ascending
    'XL_DAIO_TRIGGER_MODE_ANALOG_DESCENDING':   4,  # trigger on input 3 ascending
    'XL_DAIO_TRIGGER_MODE_ANALOG':              6   # trigger on input 3
}

IS_ON_BUS = {
    'YES':  0x01,
    'NO':   0x00
}

###############################################################
#
#        Bellow is only used for interpretation
#
###############################################################

DRIVER_STATUS_MSG = \
{
     0          :   'XL_SUCCESS',                   
     1          :   'XL_PENDING',                   
     10         :   'XL_ERR_QUEUE_IS_EMPTY',        
     11         :   'XL_ERR_QUEUE_IS_FULL',         
     12         :   'XL_ERR_TX_NOT_POSSIBLE',       
     14         :   'XL_ERR_NO_LICENSE',            
     101        :   'XL_ERR_WRONG_PARAMETER',       
     110        :   'XL_ERR_TWICE_REGISTER',        
     111        :   'XL_ERR_INVALID_CHAN_INDEX',   
     112        :   'XL_ERR_INVALID_ACCESS',        
     113        :   'XL_ERR_PORT_IS_OFFLINE',       
     116        :   'XL_ERR_CHAN_IS_ONLINE',        
     117        :   'XL_ERR_NOT_IMPLEMENTED',       
     118        :   'XL_ERR_INVALID_PORT',          
     120        :   'XL_ERR_HW_NOT_READY',          
     121        :   'XL_ERR_CMD_TIMEOUT',           
     122        :   'XL_ERR_CMD_HANDLING',          
     129        :   'XL_ERR_HW_NOT_PRESENT',        
     131        :   'XL_ERR_NOTIFY_ALREADY_ACTIVE', 
     132        :   'XL_ERR_INVALID_TAG',           
     133        :   'XL_ERR_INVALID_RESERVED_FLD',  
     134        :   'XL_ERR_INVALID_SIZE',          
     135        :   'XL_ERR_INSUFFICIENT_BUFFER',   
     136        :   'XL_ERR_ERROR_CRC',             
     137        :   'XL_ERR_BAD_EXE_FORMAT',        
     138        :   'XL_ERR_NO_SYSTEM_RESOURCES',   
     139        :   'XL_ERR_NOT_FOUND',             
     140        :   'XL_ERR_INVALID_ADDRESS',       
     141        :   'XL_ERR_REQ_NOT_ACCEP',         
     142        :   'XL_ERR_INVALID_LEVEL',         
     143        :   'XL_ERR_NO_DATA_DETECTED',      
     144        :   'XL_ERR_INTERNAL_ERROR',        
     145        :   'XL_ERR_UNEXP_NET_ERR',         
     146        :   'XL_ERR_INVALID_USER_BUFFER',   
     152        :   'XL_ERR_NO_RESOURCES',          
     153        :   'XL_ERR_WRONG_CHIP_TYPE',       
     154        :   'XL_ERR_WRONG_COMMAND',         
     155        :   'XL_ERR_INVALID_HANDLE',        
     157        :   'XL_ERR_RESERVED_NOT_ZERO',     
     158        :   'XL_ERR_INIT_ACCESS_MISSING',   
     201        :   'XL_ERR_CANNOT_OPEN_DRIVER',    
     202        :   'XL_ERR_WRONG_BUS_TYPE',        
     203        :   'XL_ERR_DLL_NOT_FOUND',         
     204        :   'XL_ERR_INVALID_CHANNEL_MASK',  
     205        :   'XL_ERR_NOT_SUPPORTED',         
     210        :   'XL_ERR_CONNECTION_BROKEN',     
     211        :   'XL_ERR_CONNECTION_CLOSED',     
     212        :   'XL_ERR_INVALID_STREAM_NAME',   
     213        :   'XL_ERR_CONNECTION_FAILED',     
     214        :   'XL_ERR_STREAM_NOT_FOUND',      
     215        :   'XL_ERR_STREAM_NOT_CONNECTED',  
     216        :   'XL_ERR_QUEUE_OVERRUN',         
     255        :   'XL_ERROR',                     
     0x0201     :   'XL_ERR_INVALID_DLC',            #DLC with invalid value                                            
     0x0202     :   'XL_ERR_INVALID_CANID',          #CAN Id has invalid bits set                                       
     0x0203     :   'XL_ERR_INVALID_FDFLAG_MODE20',  #Flag set that must not be set when configured for CAN20 (e.g. EDL)
     0x0204     :   'XL_ERR_EDL_RTR',                #RTR must not be set in combination with EDL                       
     0x0205     :   'XL_ERR_EDL_NOT_SET',            #EDL is not set but BRS and/or ESICTRL is                          
     0x0206     :   'XL_ERR_UNKNOWN_FLAG'            #Unknown bit in flags field is set                                 
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
    0x0000 : 'XL_TRANSCEIVER_TYPE_NONE',                     
    0x0001 : 'XL_TRANSCEIVER_TYPE_CAN_251',                  
    0x0002 : 'XL_TRANSCEIVER_TYPE_CAN_252',                  
    0x0003 : 'XL_TRANSCEIVER_TYPE_CAN_DNOPTO',               
    0x0005 : 'XL_TRANSCEIVER_TYPE_CAN_SWC_PROTO',           # Prototype. Driver may latch-up.
    0x0006 : 'XL_TRANSCEIVER_TYPE_CAN_SWC',                 
    0x0007 : 'XL_TRANSCEIVER_TYPE_CAN_EVA',                 
    0x0008 : 'XL_TRANSCEIVER_TYPE_CAN_FIBER',               
    0x000B : 'XL_TRANSCEIVER_TYPE_CAN_1054_OPTO',           # 1054 with optical isolation
    0x000C : 'XL_TRANSCEIVER_TYPE_CAN_SWC_OPTO',            # SWC with optical isolation
    0x000D : 'XL_TRANSCEIVER_TYPE_CAN_B10011S',             # B10011S truck-and-trailer
    0x000E : 'XL_TRANSCEIVER_TYPE_CAN_1050',                # 1050
    0x000F : 'XL_TRANSCEIVER_TYPE_CAN_1050_OPTO',           # 1050 with optical isolation
    0x0010 : 'XL_TRANSCEIVER_TYPE_CAN_1041',                # 1041
    0x0011 : 'XL_TRANSCEIVER_TYPE_CAN_1041_OPTO',           # 1041 with optical isolation
    0x0016 : 'XL_TRANSCEIVER_TYPE_CAN_VIRTUAL',             # Virtual CAN Trasceiver for Virtual CAN Bus Driver
    0x0017 : 'XL_TRANSCEIVER_TYPE_LIN_6258_OPTO',           # Vector LINcab 6258opto with transceiver Infineon TLE6258 
    0x0019 : 'XL_TRANSCEIVER_TYPE_LIN_6259_OPTO',           # Vector LINcab 6259opto with transceiver Infineon TLE6259
    0x001D : 'XL_TRANSCEIVER_TYPE_DAIO_8444_OPTO',          # Vector IOcab 8444  (8 dig.Inp.; 4 dig.Outp.; 4 ana.Inp.; 4 ana.Outp.)
    0x0021 : 'XL_TRANSCEIVER_TYPE_CAN_1041A_OPTO',          # 1041A with optical isolation
    0x0023 : 'XL_TRANSCEIVER_TYPE_LIN_6259_MAG',            # LIN transceiver 6259, with transceiver Infineon TLE6259, magnetically isolated, stress functionality
    0x0025 : 'XL_TRANSCEIVER_TYPE_LIN_7259_MAG',            # LIN transceiver 7259, with transceiver Infineon TLE7259, magnetically isolated, stress functionality
    0x0027 : 'XL_TRANSCEIVER_TYPE_LIN_7269_MAG',            # LIN transceiver 7269, with transceiver Infineon TLE7269, magnetically isolated, stress functionality
    0x0033 : 'XL_TRANSCEIVER_TYPE_CAN_1054_MAG',            # TJA1054, magnetically isolated, with selectable termination resistor (via 4th IO line) 
    0x0035 : 'XL_TRANSCEIVER_TYPE_CAN_251_MAG',             # 82C250/251 or equivalent, magnetically isolated
    0x0037 : 'XL_TRANSCEIVER_TYPE_CAN_1050_MAG',            # TJA1050, magnetically isolated
    0x0039 : 'XL_TRANSCEIVER_TYPE_CAN_1040_MAG',            # TJA1040, magnetically isolated
    0x003B : 'XL_TRANSCEIVER_TYPE_CAN_1041A_MAG',           # TJA1041A, magnetically isolated
    0x0080 : 'XL_TRANSCEIVER_TYPE_TWIN_CAN_1041A_MAG',      # TWINcab with two TJA1041, magnetically isolated
    0x0081 : 'XL_TRANSCEIVER_TYPE_TWIN_LIN_7269_MAG',       # TWINcab with two 7259, Infineon TLE7259, magnetically isolated, stress functionality
    0x0082 : 'XL_TRANSCEIVER_TYPE_TWIN_CAN_1041AV2_MAG',    # TWINcab with two TJA1041, magnetically isolated
    0x0083 : 'XL_TRANSCEIVER_TYPE_TWIN_CAN_1054_1041A_MAG', # TWINcab with TJA1054A and TJA1041A with magnetic isolation
    0x0101 : 'XL_TRANSCEIVER_TYPE_PB_CAN_251',               
    0x0103 : 'XL_TRANSCEIVER_TYPE_PB_CAN_1054',              
    0x0105 : 'XL_TRANSCEIVER_TYPE_PB_CAN_251_OPTO',          
    0x010B : 'XL_TRANSCEIVER_TYPE_PB_CAN_SWC',               
    0x0115 : 'XL_TRANSCEIVER_TYPE_PB_CAN_1054_OPTO',         
    0x0117 : 'XL_TRANSCEIVER_TYPE_PB_CAN_SWC_OPTO',          
    0x0119 : 'XL_TRANSCEIVER_TYPE_PB_CAN_TT_OPTO',           
    0x011B : 'XL_TRANSCEIVER_TYPE_PB_CAN_1050',              
    0x011D : 'XL_TRANSCEIVER_TYPE_PB_CAN_1050_OPTO',         
    0x011F : 'XL_TRANSCEIVER_TYPE_PB_CAN_1041',              
    0x0121 : 'XL_TRANSCEIVER_TYPE_PB_CAN_1041_OPTO',         
    0x0129 : 'XL_TRANSCEIVER_TYPE_PB_LIN_6258_OPTO',        # LIN piggy back with transceiver Infineon TLE6258
    0x012B : 'XL_TRANSCEIVER_TYPE_PB_LIN_6259_OPTO',        # LIN piggy back with transceiver Infineon TLE6259
    0x012D : 'XL_TRANSCEIVER_TYPE_PB_LIN_6259_MAG',         # LIN piggy back with transceiver Infineon TLE6259, magnetically isolated, stress functionality
    0x012F : 'XL_TRANSCEIVER_TYPE_PB_CAN_1041A_OPTO',       # CAN transceiver 1041A
    0x0131 : 'XL_TRANSCEIVER_TYPE_PB_LIN_7259_MAG',         # LIN piggy back with transceiver Infineon TLE7259, magnetically isolated, stress functionality
    0x0133 : 'XL_TRANSCEIVER_TYPE_PB_LIN_7269_MAG',         # LIN piggy back with transceiver Infineon TLE7269, magnetically isolated, stress functionality
    0x0135 : 'XL_TRANSCEIVER_TYPE_PB_CAN_251_MAG',          # 82C250/251 or compatible, magnetically isolated
    0x0136 : 'XL_TRANSCEIVER_TYPE_PB_CAN_1050_MAG',         # TJA 1050, magnetically isolated
    0x0137 : 'XL_TRANSCEIVER_TYPE_PB_CAN_1040_MAG',         # TJA 1040, magnetically isolated
    0x0138 : 'XL_TRANSCEIVER_TYPE_PB_CAN_1041A_MAG',        # TJA 1041A, magnetically isolated
    0x0139 : 'XL_TRANSCEIVER_TYPE_PB_DAIO_8444_OPTO',       # optically isolated IO piggy
    0x013B : 'XL_TRANSCEIVER_TYPE_PB_CAN_1054_MAG',         # TJA1054, magnetically isolated, with selectable termination resistor (via 4th IO line) 
    0x013C : 'XL_TRANSCEIVER_TYPE_CAN_1051_CAP_FIX',        # TJA1051 - fixed transceiver on e.g. 16xx/8970
    0x013D : 'XL_TRANSCEIVER_TYPE_DAIO_1021_FIX',           # Onboard IO of VN1630/VN1640 
    0x013E : 'XL_TRANSCEIVER_TYPE_LIN_7269_CAP_FIX',        # TLE7269 - fixed transceiver on 1611
    0x013F : 'XL_TRANSCEIVER_TYPE_PB_CAN_1051_CAP',         # TJA 1051, capacitive isolated
    0x0140 : 'XL_TRANSCEIVER_TYPE_PB_CAN_SWC_7356_CAP',     # Single Wire NCV7356, capacitive isolated
    0x0141 : 'XL_TRANSCEIVER_TYPE_PB_CAN_1055_CAP',         # TJA1055, capacitive isolated, with selectable termination resistor (via 4th IO line) 
    0x0142 : 'XL_TRANSCEIVER_TYPE_PB_CAN_1057_CAP',         # TJA 1057, capacitive isolated
    0x0143 : 'XL_TRANSCEIVER_TYPE_A429_HOLT8596_FIX',       # Onboard HOLT 8596 TX transceiver on VN0601
    0x0144 : 'XL_TRANSCEIVER_TYPE_A429_HOLT8455_FIX',       # Onboard HOLT 8455 RX transceiver on VN0601
    0x0201 : 'XL_TRANSCEIVER_TYPE_PB_FR_1080',              # TJA 1080
    0x0202 : 'XL_TRANSCEIVER_TYPE_PB_FR_1080_MAG',          # TJA 1080 magnetically isolated piggy
    0x0203 : 'XL_TRANSCEIVER_TYPE_PB_FR_1080A_MAG',         # TJA 1080A magnetically isolated piggy
    0x0204 : 'XL_TRANSCEIVER_TYPE_PB_FR_1082_CAP',          # TJA 1082 capacitive isolated piggy
    0x0205 : 'XL_TRANSCEIVER_TYPE_PB_FRC_1082_CAP',         # TJA 1082 capacitive isolated piggy with CANpiggy form factor
    0x0206 : 'XL_TRANSCEIVER_TYPE_FR_1082_CAP_FIX',         # TJA 1082 capacitive isolated piggy fixed transceiver - e.g. 7610
    0x0220 : 'XL_TRANSCEIVER_TYPE_MOST150_ONBOARD',         # Onboard MOST150 transceiver of VN2640
    0x0230 : 'XL_TRANSCEIVER_TYPE_ETH_BCM54810_FIX',        # Onboard Broadcom Ethernet PHY on VN5610 and VX0312
    0x0231 : 'XL_TRANSCEIVER_TYPE_ETH_AR8031_FIX',          # Onboard Atheros Ethernet PHY
    0x0232 : 'XL_TRANSCEIVER_TYPE_ETH_BCM89810_FIX',        # Onboard Broadcom Ethernet PHY
    0x0233 : 'XL_TRANSCEIVER_TYPE_ETH_TJA1100_FIX',         # Onboard NXP Ethernet PHY
    0x0234 : 'XL_TRANSCEIVER_TYPE_ETH_BCM54810_89811_FIX',  # Onboard Broadcom Ethernet PHYs (e.g. VN5610A - BCM54810: RJ45, BCM89811: DSUB)
    0x0280 : 'XL_TRANSCEIVER_TYPE_PB_DAIO_8642',            # Iopiggy for VN8900
    0x028f : 'XL_TRANSCEIVER_TYPE_DAIO_AL_ONLY',            # virtual piggy type for activation line only (e.g. VN8810ini)
    0x0290 : 'XL_TRANSCEIVER_TYPE_DAIO_1021_FIX_WITH_AL',   # On board IO with Activation Line (e.g. VN5640) 
    0x0291 : 'XL_TRANSCEIVER_TYPE_DAIO_AL_WU',              # virtual piggy type for activation line and WakeUp Line only (e.g. VN5610A)                                
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