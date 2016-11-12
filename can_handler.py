'''
:Author: *Jim Nilsson*  
:Version: *0.9 Beta*
:Status: *Released*

------------------------------------------------------------------------------- 
'''

#IMPORTS
import re
import platform
import time
import ctypes
import threading
from can_vector_driver import XlDriver, s_xl_event                                                      

#MODULE CONSTANTS
XL_INVALID_PORTHANDLE       =       -1
XL_INTERFACE_VERSION        =       3
XL_ACTIVATE_RESET_CLOCK     =       8
XL_NO_INIT_ACCESS           =       0
XL_SUCCESS                  =       0
XL_ERR_QUEUE_IS_EMPTY       =       10

XL_NO_COMMAND               =       0
XL_RECEIVE_MSG              =       1
XL_CHIP_STATE               =       4
XL_TRANSCEIVER              =       6
XL_TIMER                    =       8
XL_TRANSMIT_MSG             =       10
XL_SYNC_PULSE               =       11
XL_APPLICATION_NOTIFICATION =       15

DLC                         =       8
SIZE_MSG_BUFFER             =       256

XLuint64                    =       ctypes.c_longlong
XLaccess                    =       XLuint64
XLportHandle                =       ctypes.c_long
XLeventTag                  =       ctypes.c_ubyte
XLevent                     =       s_xl_event
XLeventList                 =       SIZE_MSG_BUFFER*XLevent

class CanHwChannel():
    """
        **Description this is the generall hardware CAN channel class. It contains all information about the used hardware
        to be able to open a channel for commuication over CAN. 
    """
    def __init__(self):
        self.__create()
        
    def __create(self):
        self.__hardware                 = None
        self.__dllVersion               = None 
        self.__numberOfChannels         = None 
        self.__channelName              = None 
        self.__hardwareType             = None 
        self.__hardwareIndex            = None 
        self.__hardwareChannel          = None 
        self.__transceiverType          = None 
        self.__transceiverState         = None 
        self.__channelIndex             = None 
        self.__channelMask              = None 
        self.__isOnBus                  = None
        self.__connectedBusType         = None
        self.__hardwareSerialNumber     = None 
        self.__hardwareArticleNumber    = None 
        self.__transceiverName          = None
        self.__portHandle               = None
        self.__accessMask               = None
        
    def __setHardware(self, value):
        self.__hardware = value
        
    def __getHardware(self):
        return self.__hardware    
        
    def __setDllversion(self, value):
        self.__dllVersion = value
    
    def __getDllversion(self):
        return self.__dllVersion
    
    def __setNumberOfChannels(self, value):
        self.__numberOfChannels = value
        
    def __getNumberOfChannels(self):
        return self.__numberOfChannels
    
    def __setChannelName(self, value):
        self.__channelName = value
    
    def __getChannelName(self):
        return self.__channelName
    
    def __setHardwareType(self, value):
        self.__hardwareType(value)
        
    def __getHardwareType(self):
        return self.__hardwareType
    
    def __setHardwareIndex(self, value):
        self.__hardwareIndex(value)
        
    def __getHardwareIndex(self):
        return self.__hardwareIndex

    def __setHardwareChannel(self, value):
        self.__hardwareChannel(value)
        
    def __getHardwareChannel(self):
        return self.__hardwareChannel
    
    def __setTransceiverType(self, value):
        self.__transceiverType(value)
        
    def __getTransceiverType(self):
        return self.__transceiverType

    def __setTransceiverState(self, value):
        self.__transceiverState(value)
        
    def __getTransceiverState(self):
        return self.__transceiverState

    def __setChannelIndex(self, value):
        self.__channelIndex(value)
        
    def __getChannelIndex(self):
        return self.__channelIndex

    def __setChannelMask(self, value):
        self.__channelMask(value)
        
    def __getChannelMask(self):
        return self.__channelMask

    def __setIsOnBus(self, value):
        self.__isOnBus(value)
        
    def __getIsOnBus(self):
        return self.__isOnBus   

    def __getConnectedBusType(self, value):
        self.__connectedBusType = value
        
    def __setConnectedBusType(self):
        return self.__connectedBusType

    def __setHardwareSerialNumber(self, value):
        self.__hardwareSerialNumber(value)
        
    def __getHardwareSerialNumber(self):
        return self.__hardwareSerialNumber
    
    def __setHardwareArticleNumber(self, value):
        self.__hardwareArticleNumber(value)
        
    def __getHardwareArticleNumber(self):
        return self.__hardwareArticleNumber
    
    def __setTransceiverName(self, value):
        self.__transceiverName(value)
        
    def __getTransceiverName(self):
        return self.__transceiverName 
    
    def __setPortHandel(self, value):
        self.__portHandle = value
        
    def __getPortHandel(self):
        return self.__portHandle
    
    def __setAccessMask(self, value):
        self.__accessMask = value
        
    def __getAccessMask(self):
        return self.__accessMask
    
    hardware                 = property(__getHardware, __setHardware)
    dllVersion               = property(__getDllversion, __setDllversion)
    numberOfChannels         = property(__getNumberOfChannels, __setNumberOfChannels)
    channelName              = property(__getChannelName, __setChannelName)
    hardwareType             = property(__getHardwareType, __setHardwareType)
    hardwareIndex            = property(__getHardwareIndex, __setHardwareIndex)
    hardwareChannel          = property(__getHardwareChannel, __setHardwareChannel)
    transceiverType          = property(__getTransceiverType, __setTransceiverType)
    transceiverState         = property(__getTransceiverState, __setTransceiverState)
    channelIndex             = property(__getChannelIndex, __setChannelIndex)
    channelMask              = property(__getChannelMask, __setChannelMask)
    isOnBus                  = property(__getIsOnBus, __setIsOnBus)
    connectedBusType         = property(__getConnectedBusType, __setConnectedBusType)
    hardwareSerialNumber     = property(__getHardwareSerialNumber, __setHardwareSerialNumber)
    hardwareArticleNumber    = property(__getHardwareArticleNumber, __setHardwareArticleNumber)
    transceiverName          = property(__getTransceiverName, __setTransceiverName)
    portHandel               = property(__getPortHandel, __setPortHandel)
    accessMask               = property(__getAccessMask, __setAccessMask)
                
class CanMsg():
    """
        This is the general CAN Msg class. Used to store CAN messages.
    """
    def __init__(self):
        """
            Init method
        """
        self.create()
        return

    def __create(self):
        self.__id           = None #Frame MSG ID
        self.__flags        = None #Flags from tranciver
        self.__dlc          = None #Data length code
        self.__res1         = None #Only used by Vector HW
        self.__timeStamp    = None #Actual timestamp generated by the hardware (for vectore HW Value is in nanoseconds).
        self.__data         = None #Payload i.e. the transmitted / recived data
    
    def __setId(self, value):
        self.__id = value
        
    def __getId(self):
        return self.__id
    
    def __setFlags(self, value):
        self.__flags = value
        
    def __getFlags(self):
        return self.__flags
    
    def __setDlc(self, value):
        self.__dlc = value
    
    def __getDlc(self):
        return self.__dlc

    def __setRes1(self, value):
        self.__res1 = value
    
    def __getRes1(self):
        return self.__res1
    
    def __setData(self, value):
        self.__data = value
        
    def __getData(self):
        return self.__data

    def __setTimeStamp(self, value):
        self.__timeStamp = value
    
    def __getTimeStamp(self):
        return self.__timeStamp
    
    id          = property(__getId, __setId)
    flags       = property(__getFlags, __setFlags)
    dlc         = property(__getDlc, __setDlc)
    res1        = property(__getRes1, __setRes1)
    data        = property(__getData, __setData)
    timeStamp   = property(__getTimeStamp, __setTimeStamp)

class CanMsgHolder():
    """
        **Description:** The Can Msg Holder class is used to hold CAN frames 
        from a specific CAN ID. The CAN ID correlates to the MSG ID in the 
        DBC-file that can be viewed and used together with vectors CANAlyzer. 
        It has a frame buffer that is the size of SIZE_MSG_BUFFER same as that 
        the HW buffer is initialized to.  
    """
    
    def __init__(self):
        """
            Internal method.
        """
        self.__bufferSize           = SIZE_MSG_BUFFER 
        self.__msgBuffer            = []
        self.__latestTimeStamp      = None

    def addMsgToBuffer(self, msgIn):
        """
            **Description:** Adds a CAN message to the messaged buffer.
            
            :INPUT:
            :param msgIn: The CAN msg that will be added to the buffer
            :type msgIn: XLevent
            
            **Detailed Description:** The msg buffer is a list and each candrivers 
            a new msg is added to the msg buffer its added to the end of the
            list. If the msg buffer is full the last entry of the msg buffer is
            disregarded and the new msg is added in its place.            
        """
        if len(self.__msgBuffer) == SIZE_MSG_BUFFER:
            self.__msgBuffer.pop()
        self.__msgBuffer.append(msgIn)
        return
    
    def getMsgFromBuffer(self):
        """
            **Not yet implemented**
        """
        pass
    
    def getLatestMsgFromBuffer(self):
        """
            **Description:** Retrieves the latest added msg in the msg buffer.
            
            :OUTPUT:
            :param msg: The latest msg in the msg buffer
            :type msg: XLevent
        """
        if len(self.__msgBuffer) != 0:
            msg = self.__msgBuffer.pop()
            return msg 
        
    def getOldestMsgFromBuffer(self):
        """
            **Description:** Retrieves the oldest added msg in the msg buffer.
            
            :OUTPUT:
            :param msg: The oldest msg in the msg buffer
            :type msg: XLevent
        """
        if len(self.__msgBuffer) != 0:
            msg = self.__msgBuffer.pop(0)
            return msg 
    
    def getNumberOfMsgInBuffer(self):
        """
            **Description:** Retrieves the number of msg contained in the msg
            buffer.
            
            :OUTPUT:
            :param lengthMsgBuffer: The number of msg currently in the msg buffer
            :type lengthMsgBuffer: Integer
        """
        lengthMsgBuffer = len(self.__msgBuffer)
        return lengthMsgBuffer
    
    def clearBuffer(self):
        """
            **Description:** Clears the msg buffer of all messages
        """
        self.__msgBuffer = []

    def __printMsgBuffer(self):
        """
            Internal method.
            
            Used to print out what is currently contained in the msg buffer 
            onto the standard output
        """
        msgNumber   = 0
        timeStamp   = None
        
        print "---------------------------------------------------------------"
        for msg in self.__msgBuffer:
            tmpResponse = []
            
            timeStamp = msg.timeStamp
            for i in range(8):
                tmpResponse.append(msg.tagData.msg.data[i])
            print "[ MSG NR: %d ]"%msgNumber
            print "[ TIMESTAMP: %d ]"%timeStamp
            print "- MSG: \t%s\n" %self.__li2ls(tmpResponse)
            msgNumber += 1
        print "---------------------------------------------------------------" 
        
    def __li2ls(self, liIn, iBaseIn = 16, iMinNrOfChars = 2 ):
        """
            Internal method.
            
            takes a list of integers and returns a list of strings.
        """
        if( iBaseIn == 16 ):
            sConv = "%0*X"
        else:
            sConv = "%0*d"
    
        ls = []
        for iData in liIn:
            ls.append( sConv % (iMinNrOfChars,iData) )
        return ls
    
class CanHw():
    """
        **Description:** This is the CANHW class that handles all the CAN 
        communication for the library BeeJay. The class can be used stand alone
        to send an receive CAN messages on CAN.
        
        It uses the Vector GmbH XL Driver Library to interface with all 
        of Vectors supported hardware.
    """
    
    ERROR_MSG = \
    {             
        0  :   '[- General error -]',
        1  :   '[- Not yet implemented -]',         
        2  :   '[- Not supported yet -]',
        3  :   '[- No hardware selected -]',
        4  :   '[- No hardware present -]',
        5  :   '[- No availble channels to select.-]',
        6  :   '[- Not yet supported please choose none interactive mode i.e. interactive = False -]',
        7  :   '[- All channels occupied or no hardware present. Please make atleast one channel available -]',
        8  :   '[-  -]'
    }
    
    def __init__(self):
        """
            Internal method.
        """
        self.create()        
        return
    
    """
        **The methods below are common methods for all HW
    """ 
    
    def create(self):
        """
            **Description:** The methods is called automatically when a instance
            of the class is created by being called from the __init__ method. It
            creates and initilizes all the global variables for the class.            
        """
        #NEW
        self.__channelList              = []                # A list containing all available channes from each connected HW
        self.__selectedChannel          = None              # The selcted HW channel to transmitt and recvive messages from
        self.__msgHolderList            = {}                # Container of all recived CAN mesages
        self.__commonResourceThreadLock = threading.Lock()  # Thred lock for common resources
        self.__threadFrequency          = 0.005             # Recive thred frequency
           
        #OLD
        self.__xlDriverConfig           = None
        self.__hwTypeList               = None
        self.__hwIndexList              = None
        self.__canChannel               = None
        self.__portHandle               = None
        self.__permissionMask           = None
        self.__txListenerThread         = None
        self.__msgBufferListTx          = None
        self.__msgBufferListRx          = None
        self.__canLoggin                = None
        self.__canLoggFile              = None
        self.__isOnBus                  = False

        
        

        return
    
    def setup(self, fileIn = None, canLoggingOnOff = False, hardwareType = None, interactive = False):
        """
            **Description:** The setup method is used to setup the CAN Hardware 
            with a available channel to send and receive from.
            
            :INPUT:
            :param fileIn: The file location of the vxlapi.dll file for the vectors XL Library.
            :type fileIn: string
            :param canLoggingOnOff: Turn on or off logging of the CAN traffic.
            :type canLoggingOnOff: Bool
            
            **Detailed Description:** N/A
        """
        if(hardwareType == 'Vector'):
            self.__setupVectorHw(fileIn, interactive)
            
        elif(hardwareType == 'Kvaser'):
            print self.ERROR_MSG[2]
        
        elif(hardwareType == 'Peak'):
            print self.ERROR_MSG[2]
            
        else:
            print self.ERROR_MSG[3]
            return
        
        #TODO fix independent logging from diffrent CAN HW soruces    
        if canLoggingOnOff:
            self.__canLoggin = canLoggingOnOff
            currentDate = time.strftime("%Y-%m-%d")
            currentTime = time.strftime("%H-%M-%S") 
            canLoggFileName = "canLogg_"+"Date_"+currentDate+"_Time_"+currentTime+".txt"           
            self.__canLoggFile = open(canLoggFileName, "w")
            loggFileHeader = "[ - TIMESTAMP - ]\t [ - ID - ]\t\t\t [ - DATA - ]\n"
            self.__canLoggFile.write(loggFileHeader)
        return
   
    def manualSetup(self, fileIn = None):
        """
            **Description:** Setup the CAN hardware manually
            
            **Not yet implemented**
        """
        pass

    def request(self):
        """
            **Description:** The request method opens a selected channel and 
            activates it.
            
            **Detailed Description:** The request class needs to be called after
            the setup method and takes the requested channel opens and 
            activates it for sending and receiving messages onto CAN. It will
            exit if no channel is availeble.
            
            Once the channel is open and activated the listener thread is started
            and it in it's turn starts to collect CAN messages from CAN. The 
            thread is executed periodically according to the "threadFrequency" 
            that is setup in the create method.
        """
        if self.__canChannel == None:
            print "No CAN Channel chosen to open \n"
            return
        else:
            if not self.__openChannel():
                print "Port could not be opened already initialized \n"
                return
            if not self.__activateChannel():
                print "Could not activate channel \n"
                return
            
            text = "Opened and activated [ %s ] \n" %self.__canChannel.name
            print text
            
            time.sleep(0.005) #Allows the MSG Queue to fill up with messages
            self.__rxListenerThreadStart()

    def sendOneCanMsg(self, msgId, msgIn):
        """
        **Description:** Sends a CAN msg out on the CAN network.
        
        :INPUT:
        :param msgId: The MSG ID of the msg to send out onto CAN.
        :type msgId: Hex
        :param msgIn: The MSG to send out on to the CAN network.
        :type msgIn: List of Hex
        
        **Detailed Description:** The CAN msg need to be formated as below 
        illustrated for this method to work. First byte is always reserved for 
        the number of bytes in the CAN msg. The method returns true of 
        successful otherwise returns false.
        
        .. code:: python
            
            msgListIn = [0x02, 0xF1, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00]
          
        :OUTPUT:
        :param return: Returns true if successful otherwise returns false 
        :type return: Bool
        """
        if self.__isOnBus == None:
            print "No CAN Channel open for transmit aborting request \n"
            return False
           
        self.__msgBufferListTx = XLeventList()
        
        messageCount    =   ctypes.c_uint(1)
        portHandle      =   self.__portHandle
        accessMask      =   self.__permissionMask
        
        self.__msgBufferListTx[0].tag                = XL_TRANSMIT_MSG
        self.__msgBufferListTx[0].tagData.msg.id     = msgId
        self.__msgBufferListTx[0].tagData.msg.dlc    = DLC
        
        for byte in range(len(msgIn)):
            self.__msgBufferListTx[0].tagData.msg.data[byte]  = msgIn[byte]
            
        self.oXLDRIVER.xlCanTransmit(portHandle, accessMask, messageCount \
                                         ,self.__msgBufferListTx)
        
        self.__msgBufferListTx = None
        return True
    
    def sendMultipleCanMsg(self):
        """
            **Description:** Sending multiple CAN MSG
            
            **Not yet implemented** 
        """
        pass
    
    def reciveCanMsg(self):
        """
        **Description:** This method is used to grab all messaged that are in 
        the hardware messaged buffer in the CAN hardware.  
        
        The following code takes the messages grabbed from the HW messaged 
        buffer and adds it to the appropriate msg holder object's msg buffer. 
        If no msg holder object exists for that specific msg ID one is created 
        and the messaged is added to it's msg buffer. This ensourse that each
        msg sent on CAN has its own msg holder object and its own msg buffer the
        size of MAX_MSG_BUFFER_SIZE.
        
        .. code:: python
            
            for msg in self.__msgBufferListRx:
                try: 
                    oFrameHolder = self.__msgHolderList[msg.tagData.msg.id]
                except:
                    oFrameHolder = CanMsgHolder()
                    self.__msgHolderList[msg.tagData.msg.id] = oFrameHolder
                    
                oFrameHolder.addMsgToBuffer(msg)
        
        This method is also called by the thread *"rxListenerThread"*
        periodically according to the *"threadFrequency"* defined in the create
        method. 
        """
        if self.__isOnBus == False:
            print "No CAN Channel open for transmit aborting request \n"
            return False
        
        self.__msgBufferListRx = XLeventList()
        
        portHandle          =   self.__portHandle
        pEventCount         =   ctypes.c_uint(SIZE_MSG_BUFFER)
        
        xlStatus = self.oXLDRIVER.xlReceive(portHandle, pEventCount, self.__msgBufferListRx)
       
        self.__commonResourceThreadLock.acquire() 
        if xlStatus != XL_ERR_QUEUE_IS_EMPTY:
            
            for msg in self.__msgBufferListRx:
                try: 
                    oFrameHolder = self.__msgHolderList[msg.tagData.msg.id]
                except:
                    oFrameHolder = CanMsgHolder()
                    self.__msgHolderList[msg.tagData.msg.id] = oFrameHolder
                    
                oFrameHolder.addMsgToBuffer(msg)
                          
                if self.__canLoggin:
                    if msg.tagData.msg.id != 0x00:
                        self.__canlogger(msg)
        else:
            return
        self.__commonResourceThreadLock.release()
        return
    
    def readCanMsg(self, msgId = None, outPutInfo = False):
        """
        **Description:** This method is used to read CAN MSG's form a specific 
        MSG ID's msg-buffer. 
        
        :INPUT:
        :param msgId: The specific MSG ID to fetch CAN MSG from.
        :type msgId: Hex
        :param outPutInfo: Displays information text to the standards output if 
                           put to true.
        :type outPutInfo: Bool
        
        **Detailed Description:** The msg retreived from the msg buffer of the
        specific CAN MSG ID is always the first stored CAN MSG from the CAN 
        Network. This is because the msg que in the CanMsgHolder object is 
        designed as a FIFO-Que see image bellow. Once the msg is retrieved from
        the buffer it is removed from the que and can't be retrieved again. 
        Running the method again will retrieve the next message in the que and
        so forth until the que is empty.
        
        .. figure:: images/CanMsgBuffer.png
           :align: center
           
        :OUTPUT:
        :param tmpMsg: Retrieved message from the msg buffer.
        :type tmpMsg: XLevent
        """
        self.__commonResourceThreadLock.acquire()
        if msgId == None:
            print "No MSG ID given"
            self.__commonResourceThreadLock.release()
            return
        elif (msgId not in self.__msgHolderList.keys()) and not outPutInfo:
            print "No MSG from ID 0x%0.2X received...\n"%msgId
            self.__commonResourceThreadLock.release()
            return
        elif msgId in self.__msgHolderList.keys():
            tmpMsgHolder = self.__msgHolderList[msgId]
            tmpMsg =  tmpMsgHolder.getOldestMsgFromBuffer()  
            self.__commonResourceThreadLock.release()
            return tmpMsg
        self.__commonResourceThreadLock.release()
        return
        
    def release(self):
        """
        **Description:** This method is used to release the requested 
        resources.
        """
        if self.__portHandle == None:
            return
        
        self.__rxListenerThreadStop()
        self.__deactivateChannel()
        self.__closeChannel()
     
    def destroy(self):
        """
        **Description:** This method is used to clean up all.
        """
        self.__xlDriverConfig       = None
        self.__hwTypeList           = None
        self.__hwIndexList          = None
        self.__canChannel           = None
        self.__portHandle           = None
        self.__permissionMask       = None
    
    def printHardware(self, channelsIn = None):
        """
        **Description:** This method prints the connected hardware. 
            
        :INPUT: 
        :param channelIn: Number of channels to print starts at zero i.e. the
                          first channel.
        :type channelIn: Int
        
        **Detailed Description:** If no channel is given the method the driver
        scans the ports for connected hardware and prints all avalible hardware
        onto the standard output.
        """
        self.oXLDRIVER.xlPrintDriverConfig(channelsIn)
        
        return
    
    def __setupVectorHw(self, fileIn, interactive):
        self.__oXLDRIVER = XlDriver() 
        
        if fileIn == None:
            print "[- No path to the VectorXL driver was given -]"
            
            if platform.machine() == 'i386':
                print "[- Using default path: C:\\Users\\Public\\Documents\\Vector XL Driver Library\\bin\\vxlapi.dll -]\n"
                fileIn = 'C:\\Users\\Public\\Documents\\Vector XL Driver Library\\bin\\vxlapi.dll'
            elif platform.machine() == 'AMD64':
                print "[- Using default path: C:\\Users\\Public\\Documents\\Vector XL Driver Library\\bin\\vxlapi64.dll -]\n"
                fileIn = 'C:\\Users\\Public\\Documents\\Vector XL Driver Library\\bin\\vxlapi64.dll'
            else:
                print "[- Platform not recognisable -]"
                print "[- No library loaded! -]"
                return False
        
        #Load library for access to the Vextor XL Driver               
        if not self.__oXLDRIVER.xlLoadLibrary(fileIn):
            return False
        
        #Open driver to access the internal functions of the XL driver
        if not self.__oXLDRIVER.xlOpenDriver():
            return False
        
        #If interactive = True then the user will be promed via standard I/O to enter input to the setup
        #If interactive = False then the software will automatically find the first avilable channel and open it
        if interactive == True:
            print self.ERROR_MSG[6]
        else:
            #Check if the software can access the driver configuration
            if not self.__oXLDRIVER.xlGetDriverConfig():
                return False
            else:
                #Get the complete driver configuration (all channels)
                xlDriverConfig = self.__oXLDRIVER.xlGetDriverConfig()
                #Extract each channels driver configuration and add it to a new channel object in the channelList
                for channel in range(xlDriverConfig.channelCount):
                    tmpCanHwChannel = CanHwChannel() 
                    tmpCanHwChannel.hardware                = 'Vector'
                    tmpCanHwChannel.dllVersion              = xlDriverConfig.dllVersion
                    tmpCanHwChannel.numberOfChannels        = xlDriverConfig.channelCount
                    tmpCanHwChannel.channelName             = xlDriverConfig.Channel[channel].name
                    tmpCanHwChannel.hardwareType            = self.__oXLDRIVER.HARDWARE_TYPE_MSG[xlDriverConfig.Channel[channel].hwType]
                    tmpCanHwChannel.hardwareIndex           = xlDriverConfig.Channel[channel].hwIndex
                    tmpCanHwChannel.hardwareChannel         = xlDriverConfig.Channel[channel].hwChannel
                    tmpCanHwChannel.transceiverType         = self.__oXLDRIVER.TRANSCEIVER_TYPE_MSG[xlDriverConfig.Channel[channel].transceiverType]
                    tmpCanHwChannel.transceiverState        = xlDriverConfig.Channel[channel].transceiverState
                    tmpCanHwChannel.channelIndex            = xlDriverConfig.Channel[channel].channelIndex
                    tmpCanHwChannel.channelMask             = xlDriverConfig.Channel[channel].channelMask
                    tmpCanHwChannel.isOnBus                 = self.__oXLDRIVER.IS_ON_BUS_MSG[xlDriverConfig.Channel[channel].isOnBus]
                    tmpCanHwChannel.connectedBusType        = self.__oXLDRIVER.BUS_TYPE_MSG[xlDriverConfig.Channel[channel].connectedBusType]
                    tmpCanHwChannel.hardwareSerialNumber    = xlDriverConfig.Channel[channel].serialNumber
                    tmpCanHwChannel.hardwareArticleNumber   = xlDriverConfig.Channel[channel].articleNumber
                    tmpCanHwChannel.transceiverName         = xlDriverConfig.Channel[channel].transceiverName                
                    self.__channelList.append(tmpCanHwChannel) #Add the channel to the list
                    
                    #Find the first available channel that is not occupied or open.
                    if re.search('CAN', tmpCanHwChannel.transceiverType) and (tmpCanHwChannel.isOnBus == 'NO'):
                        self.__selectedChannel = tmpCanHwChannel
                        
            if self.__selectedChannel == None:
                print self.ERROR_MSG[5]
                print self.ERROR_MSG[7]
                return False 
            
            #Open CAN selected channel
            [self.__selectedChannel.portHandel, self.__selectedChannel.accessMask] = self.__oXLDRIVER.xlOpenPort(portHandle, userName, accessMask, permissionMask, rxQueueSize, xlInterfaceVersion, busType)

    def __openChannel(self):
        """
            Internal method.
            
            Opens a CAN Channel for read/write access
        """
        portHandle          = XLportHandle(XL_INVALID_PORTHANDLE)
        userName            = ctypes.c_char_p('xlCANControlApp')
        accessMask          = XLaccess(self.__canChannel.channelMask)
        permissionMask      = XLaccess(self.__canChannel.channelMask)
        rxQueueSize         = ctypes.c_uint(SIZE_MSG_BUFFER)
        xlInterfaceVersion  = ctypes.c_uint(XL_INTERFACE_VERSION)
        busType             = ctypes.c_uint(XlDriver.BUS_TYPE['XL_BUS_TYPE_CAN'])
        
        [portHandle, permissionMask] = self.oXLDRIVER.xlOpenPort(portHandle, \
                                       userName, accessMask, permissionMask, \
                                       rxQueueSize, xlInterfaceVersion, busType)
        
        if permissionMask.value == XL_NO_INIT_ACCESS:
            return False
        else:
            self.__portHandle       = portHandle
            self.__permissionMask   = permissionMask
            return True
        
    def __activateChannel(self):
        """
            Internal method.
            
            Activates a designated CAN channel
        """
        portHandle = self.__portHandle
        accessMask = self.__permissionMask
        busType    = ctypes.c_uint(XlDriver.BUS_TYPE['XL_BUS_TYPE_CAN'])
        flags      = ctypes.c_uint(XL_ACTIVATE_RESET_CLOCK)
        
        if not self.oXLDRIVER.xlActivateChannel(portHandle, accessMask, \
                                                busType, flags):
            return False
        else:
            return True

    def __canlogger(self, msg):
        """
            Internal method.
            
            This method loggs all the traffic on CAN during the measurements
        """
        timeStamp   =   msg.timeStamp
        msgId       =   "%02X "%msg.tagData.msg.id
        byte1       =   "%02X "%msg.tagData.msg.data[0]
        byte2       =   "%02X "%msg.tagData.msg.data[1]
        byte3       =   "%02X "%msg.tagData.msg.data[2]
        byte4       =   "%02X "%msg.tagData.msg.data[3]
        byte5       =   "%02X "%msg.tagData.msg.data[4]
        byte6       =   "%02X "%msg.tagData.msg.data[5]
        byte7       =   "%02X "%msg.tagData.msg.data[6]
        byte8       =   "%02X "%msg.tagData.msg.data[7]
        loggStr = "\t" + str(timeStamp) + "\t\t\t" + msgId + "\t\t" + byte1 + byte2 + byte3 + byte4 + byte5 + byte6 + byte7 + byte8 + "\n"
        self.__canLoggFile.write(loggStr)

    def __printCanMsgList(self, canMsgListIn = None):
        """
            Internal method.
            
            This internal method is for debug purpose only. It takes a list of
            can messaged of type XLeventList and prints it to the standard
            output. if no input variable is given to the method it prints all the
            messages that are currently in the msgBufferListRx variable.
        """
        if canMsgListIn == None:
            i = 0
            for x in range(SIZE_MSG_BUFFER/4):
                msg1 = self.__msgBufferListRx[i]
                msg2 = self.__msgBufferListRx[i+1]
                msg3 = self.__msgBufferListRx[i+2]
                msg4 = self.__msgBufferListRx[i+3]
                print "\n--------------------------------------------------------------------------------------------"
                print "[ %d ]" %x
                print "Buffer Slot Nr: ", i,                       "\t Buffer Slot Nr: ", i+1,                       "\t Buffer Slot Nr: ", i+2,                       "\t Buffer Slot Nr: ", i+3
                print "Event Tag: ", msg1.tag,                     "\t\t Event Tag: ", msg2.tag,                     "\t\t Event Tag: ", msg3.tag,                     "\t\t Event Tag: ", msg4.tag
                print "Time Stamp: ", msg1.timeStamp,              "\t Time Stamp: ", msg2.timeStamp,                "\t Time Stamp: ", msg3.timeStamp,                "\t Time Stamp: ", msg4.timeStamp
                print "Msg Id: 0x%0.2X" %(msg1.tagData.msg.id),    "\t\t Msg Id: 0x%0.2X" %(msg2.tagData.msg.id),    "\t\t Msg Id: 0x%0.2X" %(msg3.tagData.msg.id),    "\t\t Msg Id: 0x%0.2X" %(msg4.tagData.msg.id)     
                print "Data: 0x%0.2X" %(msg1.tagData.msg.data[0]), "\t\t Data: 0x%0.2X" %(msg2.tagData.msg.data[0]), "\t\t Data: 0x%0.2X" %(msg3.tagData.msg.data[0]), "\t\t Data: 0x%0.2X" %(msg4.tagData.msg.data[0])
                print "Data: 0x%0.2X" %(msg1.tagData.msg.data[1]), "\t\t Data: 0x%0.2X" %(msg2.tagData.msg.data[1]), "\t\t Data: 0x%0.2X" %(msg3.tagData.msg.data[1]), "\t\t Data: 0x%0.2X" %(msg4.tagData.msg.data[1])
                print "Data: 0x%0.2X" %(msg1.tagData.msg.data[2]), "\t\t Data: 0x%0.2X" %(msg2.tagData.msg.data[2]), "\t\t Data: 0x%0.2X" %(msg3.tagData.msg.data[2]), "\t\t Data: 0x%0.2X" %(msg4.tagData.msg.data[2])
                print "Data: 0x%0.2X" %(msg1.tagData.msg.data[3]), "\t\t Data: 0x%0.2X" %(msg2.tagData.msg.data[3]), "\t\t Data: 0x%0.2X" %(msg3.tagData.msg.data[3]), "\t\t Data: 0x%0.2X" %(msg4.tagData.msg.data[3])
                print "Data: 0x%0.2X" %(msg1.tagData.msg.data[4]), "\t\t Data: 0x%0.2X" %(msg2.tagData.msg.data[4]), "\t\t Data: 0x%0.2X" %(msg3.tagData.msg.data[4]), "\t\t Data: 0x%0.2X" %(msg4.tagData.msg.data[4])
                print "Data: 0x%0.2X" %(msg1.tagData.msg.data[5]), "\t\t Data: 0x%0.2X" %(msg2.tagData.msg.data[5]), "\t\t Data: 0x%0.2X" %(msg3.tagData.msg.data[5]), "\t\t Data: 0x%0.2X" %(msg4.tagData.msg.data[5])
                print "Data: 0x%0.2X" %(msg1.tagData.msg.data[6]), "\t\t Data: 0x%0.2X" %(msg2.tagData.msg.data[6]), "\t\t Data: 0x%0.2X" %(msg3.tagData.msg.data[6]), "\t\t Data: 0x%0.2X" %(msg4.tagData.msg.data[6])
                print "Data: 0x%0.2X" %(msg1.tagData.msg.data[6]), "\t\t Data: 0x%0.2X" %(msg2.tagData.msg.data[7]), "\t\t Data: 0x%0.2X" %(msg3.tagData.msg.data[7]), "\t\t Data: 0x%0.2X" %(msg4.tagData.msg.data[7])
                i = i + 4
        
    def __rxListenerThreadStart(self):
        self.__rxListenerThread = RxListenerThread(self.reciveCanMsg, \
                                                   "rxListenerThread", \
                                                   self.__threadFrequency)
        
        self.__rxListenerThread.start()
            
    def __rxListenerThreadStop(self):
        self.__rxListenerThread.stop()
   
    def __deactivateChannel(self):
        '''
            Deactivates the CAN channel
        '''
        if (self.__permissionMask == None) or (self.__portHandle == None):
            return
        
        portHandle = self.__portHandle
        accessMask = self.__permissionMask
        
        self.oXLDRIVER.xlDeactivateChannel(portHandle, accessMask)
        
    def __closeChannel(self):
        '''
            Closes the opened CAN channel
        '''
        portHandle = self.__portHandle
        
        self.oXLDRIVER.xlClosePort(portHandle)

class RxListenerThread(threading.Thread):
    """
    **Description:** This class handles the thread that is assigned to listen
    to the CAN network and read all the messages transmitted on the connected
    CAN network. 
    """

    def __init__(self, methodToRunIn, threadNameIn, runFrequencyIn = None):
        """
        internal method
        """
        threading.Thread.__init__(self)
        
        self.methodToRun    = methodToRunIn
        self.threadName     = threadNameIn
        self.runFrequency   = runFrequencyIn
        self.stopThread     = False
                
        if runFrequencyIn == None:
            self.runFrequency = 0.005
        
    def run(self):
        """
            **Description:** starts the CAN listener thread with the desired
            thread frequency.
        """
        text = "Starting CAN listener thread with FRQ %.3f [sec]\n" %self.runFrequency
        print text
        
        while not(self.stopThread):
            if self.stopThread == True:
                break
            
            self.methodToRun()
            time.sleep(self.runFrequency)
            
        text = "Stopping CAN listener thread\n"
        print text
        return         
    
    def stop(self):
        """
        **Description:** This method stops the listener thread.
        """
        self.stopThread = True
        time.sleep(1)
        return

if __name__ == '__main__':  
    """
        IMPORTAN READ THIS!
        *******************
          
        This is used to debug the module or to run the module
        by it self. Pleas comment away when not in use.
    """
    oCANHW = CanHw()
    fileIn = 'C:\\Users\\Public\\Documents\\Vector XL Driver Library\\bin\\vxlapi64.dll'
    oCANHW.setup(fileIn = None, canLoggingOnOff = False, hardwareType = 'Vector', interactive = False) 
#     oCANHW.request()
#     oCANHW.printHardware()
#     msgBufferList = []
#               
#     msg = [0x03,0x22,0xF1,0x86]
#     nodeAdress = 0x738
#          
#     oCANHW.sendOneCanMsg(nodeAdress, msg)
#               
#     
#     while(1):          
#         msg = oCANHW.readCanMsg(0x10)
#              
#         print "\n[ TIMESTAMP: %d ]"%msg.timeStamp
#         print "[ BYTE 1:\t 0x%0.2X ]"%msg.tagData.msg.data[0]
#         time.sleep(0.05)
#     print "[ BYTE 2:\t 0x%0.2X ]"%msg.tagData.msg.data[1]
#     print "[ BYTE 3:\t 0x%0.2X ]"%msg.tagData.msg.data[2]
#     print "[ BYTE 4:\t 0x%0.2X ]"%msg.tagData.msg.data[3]
#     print "[ BYTE 5:\t 0x%0.2X ]"%msg.tagData.msg.data[4]
#     print "[ BYTE 6:\t 0x%0.2X ]"%msg.tagData.msg.data[5]
#     print "[ BYTE 7:\t 0x%0.2X ]"%msg.tagData.msg.data[6]
#     print "[ BYTE 8:\t 0x%0.2X ]\n"%msg.tagData.msg.data[7]
            
    oCANHW.release()

