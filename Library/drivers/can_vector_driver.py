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

# IMPORTS
import os
import ctypes
from can_vector_driver_types import (DRIVER_STATUS_MSG,
                                     DRIVER_STATUS,
                                     XL_INVALID_PORTHANDLE,
                                     XL_INTERFACE_VERSION,
                                     XL_ACTIVATE_RESET_CLOCK,
                                     XL_CHANNEL_NOT_FOUND,
                                     XL_NO_CHANNEL_MASK,
                                     HARDWARE_TYPE,
                                     BUS_TYPE,
                                     XLdriverConfig,
                                     XLaccess,
                                     XLportHandle,
                                     XLchipParams,
                                     s_xl_event,)

XLevent = s_xl_event()


class XlDriver():
    '''
    **Description:** This is the XL-Driver class that contains all
    methods needed to commuicate with Vectors XL-Driver.

    **Detailed Description:** This class uses the ctypes libary to wrapp the C-Function
    calls for the Vector XL API. All types are convered using the C-Ty
    '''

    def __init__(self):
        pass

    def xlLoadLibrary(self, fileDest):
        '''
        **Description:** This method is used to load the librart used by
        Vectors XL Library.

        :INPUT:
        :param fileDest: The specific MSG ID to fetch CAN MSG from.
        :type fileDest: string

        **Detailed Description:** The method takes one argument fileDest
        and uses this to load the librar *.dll file form Vector GmbH using
        ctypes windll class.
        '''

        try:
            if not os.path.exists(fileDest):
                print "[- Dll file not found at:  \'%s' -]" % fileDest
                return False
            self.oDll = ctypes.windll.LoadLibrary(fileDest)
        except Exception as error:
            print "[- Unable to load DLL file %s-]" % error
            return False

        return True

    def xlOpenDriver(self):
        '''
        **Description:** This method opens the link to the vector
        driver.

        **Detailed Description:** The uses the xlOpenDriver(); functions
        inside the XL Library and returns XL_SUCCCESS if a successful
        link has been established to the driver. Otherwise it will return
        a specific error message that will be displayed on the stadnard output.
        '''

        xlStatus = self.oDll.xlOpenDriver()

        if(xlStatus == DRIVER_STATUS['XL_SUCCESS']):
            return True
        else:
            print '[- Error unable to open driver see vendor specific message below -]'
            print '[- %s -]' % DRIVER_STATUS_MSG[xlStatus]
            return False

    def xlCloseDriver(self):
        '''
        **Description:** This method close the link to the vector
        driver.

        **Detailed Description:** The uses the xlCloseDriver(); functions
        inside the XL Library and returns XL_SUCCCESS if a successful
        link has been closed to the driver. Otherwise it will return
        a specific error message that will be displayed on the stadnard output.
        '''

        xlStatus = self.oDll.xlCloseDriver()
        if(xlStatus == self.DRIVER_STATUS['XL_SUCCESS']):
            return True
        else:
            print '[- Error unable to close the driver, see vendor specific message below -]'
            print '[- %s -]' % self.DRIVER_STATUS_MSG[xlStatus]
            return False

    def xlSetApplConfig(self,
                        appName,
                        appChannel,
                        hwType,
                        hwIndex,
                        hwChannel,
                        busType):
        '''
        **Description:** This method creates or changes a Vector application instance

        :INPUT:
        :param appName: The name of the application instance.
        :type appName: string
        :param appChannel: Index of the application channel to be accessed
        if it does not exist it will be created by the library.
        :type appChannel: integear
        :param hwType: The hardware type associated with application
        (see can_vector_driver_types.py).
        :type hwType: integear
        :param hwIndex: Index of the same hardware type.
        :type hwIndex: integear
        :param busType: specifices the specific bus type for the application
        (see can_vector_driver_types.py).
        :type bysType: integear

        **Detailed Description:** Creates a new application in the Vector
        Hardware Config tool or sets the channel configuration in an existing
        application. To set an application channel to "not assigned" state set
        hwType, hwIndex and hwChannelto 0.
        '''
        appName = ctypes.c_char_p(appName)
        appChannel = ctypes.c_uint(appChannel)
        hwType = ctypes.c_uint(hwType)
        hwIndex = ctypes.c_uint(hwIndex)
        hwChannel = ctypes.c_uint(hwChannel)
        busType = ctypes.c_uint(busType)

        self.oDll.xlSetApplConfig.argtypes = [ctypes.c_char_p,
                                              ctypes.c_uint,
                                              ctypes.c_uint,
                                              ctypes.c_uint,
                                              ctypes.c_uint,
                                              ctypes.c_uint]

        xlStatus = self.oDll.xlSetApplConfig(appName,
                                             appChannel,
                                             hwType,
                                             hwIndex,
                                             hwChannel,
                                             busType)

        if xlStatus == DRIVER_STATUS['XL_SUCCESS']:
            return True
        else:
            print '[- Error unable to set the application, see vendor specific message below -]'
            print '[- %s -]' % DRIVER_STATUS_MSG[xlStatus]
            return False

    def xlGetApplConfig(self):
        # TODO: Implement this function.
        pass

    def xlGetDriverConfig(self, oXLdriverConfig=None):
        '''
        **Description:** This method is used to access the current driver configuration.

        :INPUT:
        :param oXLdriverConfig: A instance of the class XLdriverConfig()
        :type class:

        **Detailed Description:** This method is used to readout the current Vector driver
        configueration. It takes a instance of the class XLdriverConfig() that can be accessed
        via the can_vector_driver_types.py and returns a copy of that. If a instance of the class
        XLdriverConfig() is not given one will be temporay created within this method.
        '''
        if oXLdriverConfig is None:
            oXLdriverConfig = XLdriverConfig()

        self.oDll.xlGetDriverConfig.argtypes = [ctypes.POINTER(XLdriverConfig)]
        xlStatus = self.oDll.xlGetDriverConfig(ctypes.byref(oXLdriverConfig))

        if(xlStatus == DRIVER_STATUS['XL_SUCCESS']):
            return oXLdriverConfig
        else:
            print "[- Error unable to get driver configuration see vendor specific message below -]"
            print "[- %s -]" % DRIVER_STATUS_MSG[xlStatus]
            return False

    def xlGetChannelIndex(self,
                          hwType,
                          hwIndex,
                          hwChannel):
        '''
        **Description:** Gets the channel index of a specific hardware channel.

        :INPUT:
        :param hwType: Required to distinguish the different hardware types e.g. XL_HWTYPE_VN1630, XL_HWTYPE_CANCASEXL ... -1 Can be used of the hardware type dosen't matter
        :type hwType: int
        :param hwIndex: Required to distinguish between two or more devices of the same hardware type 0, 1, 2... -1 can be used to retrieve the first available hardware
        :type hwIndex: int
        :param hwChannel: Required to distinguish the hardware channel of the selected device 0, 1, 2... -1 can be used to retrieve the first available channel
        :type hwChannel: int


        :OUTPUT:
        :param: channelIndex: The channel index. If -1 is returned the channel was not found.
        :type: channelIndex: int

        **Detailed description:** N/a
        '''

        hwType = ctypes.c_int(hwType)
        hwIndex = ctypes.c_int(hwIndex)
        hwChannel = ctypes.c_int(hwChannel)

        self.oDll.xlGetChannelIndex.argtype = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        channelIndex = self.oDll.xlGetChannelIndex(hwType, hwIndex, hwChannel)

        if channelIndex == XL_CHANNEL_NOT_FOUND:
            print 'Channel not found'
            return False
        else:
            return channelIndex

    def xlGetChannelMask(self,
                         hwType,
                         hwIndex,
                         hwChannel):
        '''
         **Description:** Gets the channel mask of a specific hardware channel.

        :INPUT:
        :param hwType: Required to distinguish the different hardware types e.g. XL_HWTYPE_VN1630, XL_HWTYPE_CANCASEXL ... -1 Can be used of the hardware type dosen't matter
        :type hwType: int
        :param hwIndex: Required to distinguish between two or more devices of the same hardware type 0, 1, 2... -1 can be used to retrieve the first available hardware
        :type hwIndex: int
        :param hwChannel: Required to distinguish the hardware channel of the selected device 0, 1, 2... -1 can be used to retrieve the first available channel
        :type hwChannel: int


        :OUTPUT:
        :param: channelMask: The channel mask. If 0 is returned the channel was not found.
        :type: channelMask: int

        **Detailed description:** This method retrives the channel mask for a sprcific channel
        on a specific hardware. These parameters can also be readout of the Vector Hardware
        Configuration tool.
        '''

        hwType = ctypes.c_int(hwType)
        hwIndex = ctypes.c_int(hwIndex)
        hwChannel = ctypes.c_int(hwChannel)
        channelMask = XLaccess(0)

        self.oDll.xlGetChannelMask.argtype = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.oDll.xlGetChannelMask.restype = XLaccess
        channelMask = self.oDll.xlGetChannelMask(hwType, hwIndex, hwChannel)

        if channelMask == XL_NO_CHANNEL_MASK:
            print 'Unable to get channel mask'
            return False
        else:
            return int(channelMask)

    def xlOpenPort(self,
                   portHandle,
                   userName,
                   accessMask,
                   permissionMask,
                   rxQueueSize,
                   xlInterfaceVersion,
                   busType):
        '''
         **Description:** Gets the channel mask of a specific hardware channel.

        :INPUT:
        :param portHandle: The handle to the port. This handle must be used in all further calls
        towards the specific port. If XL_INVALID_PORT_HANDLE is returned then the port handled was neither
        created nor opend.
        :type portHandle: int
        :param userName: The name of the application as seen the vector hardware configuration tool.
        :type userName: string
        :param accesMask: The mask of the channel to be open. The access mask can be derived from the
        Vector Hardware Configuration Tool if there is a prepared application already.
        :type accessMask: int
        :param permissionMask: The mask of the channels that requests init access.
        :type permissionMask: int
        :param rxQueueSize: The size of the recived que in the driver. The value given bust be of the
        power of 2 i.e. 2, 4, 8, 16, 32 etc...
        :type rxQueueSize: int
        


        :param hwIndex: Required to distinguish between two or more devices of the same hardware type 0, 1, 2... -1 can be used to retrieve the first available hardware
        :type hwIndex: int
        :param hwChannel: Required to distinguish the hardware channel of the selected device 0, 1, 2... -1 can be used to retrieve the first available channel
        :type hwChannel: int


        :OUTPUT:
        :param portHandle: The handle to the port. This handle must be used in all further calls
        towards the specific port. If XL_INVALID_PORT_HANDLE is returned then the port handled was neither
        created nor opend.
        :type portHandle: int
        :param permissionMask: On out this variable contains the ports that was given init access to.
        :type permissionMask: int

        **Detailed description:** This method retrives the channel mask for a sprcific channel
        on a specific hardware. These parameters can also be readout of the Vector Hardware
        Configuration tool. For definition of XLaccess see can_vector_driver_types.py.
        '''

        portHandle = XLportHandle(portHandle)
        userName = ctypes.c_char_p(userName)
        accessMask = XLaccess(accessMask)
        permissionMask = XLaccess(permissionMask)
        rxQueueSize = ctypes.c_uint(rxQueueSize)
        xlInterfaceVersion = ctypes.c_uint(xlInterfaceVersion)
        busType = ctypes.c_uint(busType)

        self.oDll.xlOpenPort.argtype = [ctypes.POINTER(XLportHandle),
                                        ctypes.c_char_p,
                                        XLaccess,
                                        ctypes.POINTER(XLaccess),
                                        ctypes.c_uint,
                                        ctypes.c_uint,
                                        ctypes.c_uint]

        xlStatus = self.oDll.xlOpenPort(ctypes.byref(portHandle),
                                        userName,
                                        accessMask,
                                        ctypes.byref(permissionMask),
                                        rxQueueSize,
                                        xlInterfaceVersion,
                                        busType)

        if xlStatus == DRIVER_STATUS['XL_SUCCESS']:
            return portHandle, permissionMask
        else:
            print DRIVER_STATUS_MSG[xlStatus]

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
        
if      __name__ == '__main__':
    
    oDriver = XlDriver()
    
    oDriver.xlLoadLibrary('C:\\Users\\Public\\Documents\\Vector XL Driver Library\\bin\\vxlapi64.dll')
    oDriver.xlOpenDriver()
    
    print oDriver.xlGetChannelMask(-1, -1, -1)
    oDriver.xlOpenPort(1, 'PyCan', 1, -1, 256, 01, 01)
    
    print "hej"

