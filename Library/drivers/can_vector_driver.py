'''
Terms and conditions
--------------------

Copywrite 2009 Jim Nilsson.
PyCAN is distributed under the terms of the GNU Lesser General Public License.

    This file is part of the PyCAN Libary.

    PyCAN is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyCAN is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU General Public License and
    GNU Lesser General Public License along with PyCAN.  
    If not, see <http://www.gnu.org/licenses/>.
'''

#IMPORTS
import os
from can_vector_driver_types import *

XLevent = s_xl_event()

class XlDriver():
    """
        **Description:** This is the XL-Driver class that contains all
        methods needed to commuicate with Vectors XL-Driver.
    """
    def __init__(self):
        pass
     
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