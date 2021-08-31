# Bluetooth Core Specification Version 5.2 | Vol 3, Part B
# Service Discovery Protocol (SDP) Specification
import struct
from scapy.packet import Packet
from scapy.fields import Field, ByteEnumField, ShortField, ShortEnumField, IntField
from tools.logger import Log

# 3.1 DATA ELEMENT
class DataElementField(Field):

    # 3.2 DATA ELEMENT TYPE DESCRIPTOR
    m_type_def = {
        0: "Nil",
        1: "Unsigned Integer",
        2: "Signed Integer",
        3: "UUID",
        4: "Text string",
        5: "Boolean",
        6: "Sequence",
        7: "Alternative",
        8: "URL",
    }

    # 3.3 DATA ELEMENT SIZE DESCRIPTOR
    m_size_def = {
        # Exception: if the data element type is nil, the data size is 0 bytes.
        0: "1 byte",
        1: "2 bytes",
        2: "4 bytes",
        3: "8 bytes",
        4: "16 bytes",
        # The data size is contained in the additional 8 bits, which are interpreted as an unsigned integer.
        5: "uint8", 
        # The data size is contained in the additional 16 bits, which are interpreted as an unsigned integer.
        6: "uint16",
        # The data size is contained in the additional 32 bits, which are interpreted as an unsigned integer.
        7: "uint32",
    }

    def __init__(self, name, default):
        Field.__init__(self, name, default)

    def addlistfield(self, pkt, s, val):
        for e in val:
            if isinstance(e, dict):
                new_s = self.addfield(pkt, s, e)
                s = new_s
            elif isinstance(e, list):
                new_s = self.addlistfield(pkt, s, e)
                s = new_s
        return s

    """
    Add an internal value to a string

    Copy the network representation of field `val` (belonging to layer
    `pkt`) to the raw string packet `s`, and return the new string packet.
    """
    def addfield(self, pkt, s, val):
        # Resolve DataElementType
        if isinstance(val["DataElementType"], str):
            type_and_size = list(DataElementField.m_type_def.values()).index(val["DataElementType"]) << 3
        else:
            type_and_size = int(val["DataElementType"]) << 3
        
        # Resolve DataElementSize
        var_size_addon_byte = 0
        if isinstance(val["DataElementSize"], str):
            data_element_size_int = list(DataElementField.m_size_def.values()).index(val["DataElementSize"])
            type_and_size |= data_element_size_int
            if val["DataElementSize"].startswith("uint"):
                var_size_addon_byte = 2 ** (data_element_size_int - 5) 
        else:
            type_and_size |= int(val["DataElementSize"])
            if int(val["DataElementSize"]) > 4:
                var_size_addon_byte = 2 ** (int(val["DataElementSize"]) - 5) 
        
        # Resolve DataElementVarSize
        if var_size_addon_byte != 0:
            full_bytes = struct.pack("B", type_and_size) + val["DataElementVarSize"]
        else:
            # No DataElementVarSize exists for DataElementSize = 0~4
            full_bytes = struct.pack("B", type_and_size)
        
        # Resolve DataValue
        if isinstance(val["DataValue"], dict):
            # DataValue is a DataElement resolving recursion
            return self.addfield(pkt, s + full_bytes, val["DataValue"])
        if isinstance(val["DataValue"], list):
            # DataValue is a DataElement list, resolving recursion
            return self.addlistfield(pkt, s + full_bytes, val["DataValue"])
        elif isinstance(val["DataValue"], bytes):
            # DataValue is bytes, just adding bytes
            return s + full_bytes + val["DataValue"]
        elif isinstance(val["DataValue"], str):
            # DataValue is a string, encoding string and adding bytes
            return s + full_bytes + val["DataValue"].encode("ascii")
        else:
            # DataValue is unknown type 
            Log.warn("Unknown DataValue type, must be dict, list, bytes or str")
            return s + full_bytes + val["DataValue"]
    
    """
    Extract an internal value from a string

    Extract from the raw packet `s` the field value belonging to layer
        `pkt`.

    Returns a two-element list,
    first the raw packet string after having removed the extracted field,
    second the extracted field itself in internal representation.
    """
    def getfield(self, pkt, s):
        Log.fatal("Not implemented!")


# 4.2 PROTOCOL DATA UNIT FORMAT
#
# - Bluetooth SDP Protocol Header
#   |- PDU ID (1 byte, range: 0x01-0x07, all other values are reversed for future use)
#   |- TransactionID (2 bytes, range: 0x0000-0xFFFF)
#   |- ParameterLength (2 bytes, range: 0x0000-0xFFFF)
#
class SDP_BASE(Packet):
    name = "SDP_BASE"

    fields_desc = [
        ByteEnumField("PDUID", 0x00, {
            0x01: "SDP_ERROR_RSP",
            0x02: "SDP_SERVICE_SEARCH_REQ",
            0x03: "SDP_SERVICE_SEARCH_RSP",
            0x04: "SDP_SERVICE_ATTR_REQ",
            0x05: "SDP_SERVICE_ATTR_RSP",
            0x06: "SDP_SERVICE_SEARCH_ATTR_REQ",
            0x07: "SDP_SERVICE_SEARCH_ATTR_RSP"
            # All other values: Reversed for future use
        }),
        ShortField("TransactionID", 0x0000),
        # TODO Auto complete the ParameterLength field using LenField or similar type
        ShortField("ParameterLength", 0x0000)
    ]

    fields_strategy = {
        "PDUID": {
            "strategy_group": [
                # Fuzzing defined values
                ["random_in_range", 50, [0x01, 0x07]],
                # Fuzzing reversed values
                ["random_all", 50, [0x00, 0xFF]]
            ],
            "rate": 100
        },
        "TransactionID": {
            "strategy_group":[
                ["random_all", 50, [0x0000, 0xFFFF]]
            ],
            "rate": 100
        },
        "ParameterLength": {
            "strategy_group":[
                ["random_all", 50, [0x0000, 0xFFFF]]
            ],
            "rate": 100
        }
    }




# 4.3 PARTIAL RESPONSES AND CONTINUATION STATE
#
# - ContinuationState (1-17 bytes)
#   |- InfoLength (1 byte, maximum allowable value: 16)
#   |- ContinuationInformation (InfoLength byte(s), range: 0-16 bytes)
#
class ContinuationStateField(Field):
    def __init__(self, name, default):
        Field.__init__(self, name, default)

    def addfield(self, pkt, s, val):
        # Resolve InfoLength
        if isinstance(val["InfoLength"], int):
            info_length_bytes = struct.pack("B", val["InfoLength"])
        else:
            info_length_bytes = val["InfoLength"][-1:]
        # Resolve ContinuationInformation
        if "ContinuationInformation" in val:
            return s + info_length_bytes + val["ContinuationInformation"]
        else:
            return s + info_length_bytes
        

    def getfield(self, pkt, s):
        Log.fatal("Not implemented!")


# 4.4 ERROR HANDLING
# 4.4.1 SDP_ERROR_RSP PDU
#
# - SDP_ERROR_RSP
#   |- Bluetooth SDP Protocol Header (5 bytes)
#   |- ErrorCode (2 bytes, range: 0x0001-0x0006, all other values are reversed for future use)
#
class SDP_ERROR_RSP(SDP_BASE):
    name = "SDP_ERROR_RSP"

    fields_desc = SDP_BASE.fields_desc + [
        ShortEnumField("ErrorCode", 0x0000, {
            0x0001: "SDP_ERROR_INVALID_SDP_VERSION",
            0x0002: "SDP_ERROR_INVALID_SERVICE_RECORD_HANDLE",
            0x0003: "SDP_ERROR_INVALID_REQUEST_SYNTAX",
            0x0004: "SDP_ERROR_INVALID_PDU_SIZE",
            0x0005: "SDP_ERROR_INVALID_CONTINUATION_STATE",
            0x0006: "SDP_ERROR_INSUFFICIENT_RESOURCES_TO_SATISFY_REQUEST"
        })
    ]

    fields_strategy = SDP_BASE.fields_strategy
    fields_strategy.update({
        "ErrorCode": {
            "strategy_group": [
                # Fuzzing defined values
                ["random_in_range", 50, [0x0001, 0x0006]],
                # Fuzzing reversed values
                ["random_all", 50, [0x0000, 0xFFFF]]
            ],
            "rate": 100
        }
    })


# 4.5 SERVICESEARCH TRANSACTION
## 4.5.1 SDP_SERVICE_SEARCH_REQ PDU
class SDP_SERVICE_SEARCH_REQ(SDP_BASE):
    name = "SDP_SERVICE_SEARCH_REQ"

    fields_desc = SDP_BASE.fields_desc + [
        DataElementField("ServiceSearchPattern", None),
        ShortField("MaximumServiceRecordCount", 0x0000),
        ContinuationStateField("ContinuationState", {
            "InfoLength": 0
        })
    ]


## 4.5.2 SDP_SERVICE_SEARCH_RSP PDU
class SDP_SERVICE_SEARCH_RSP(SDP_BASE):
    name = "SDP_SERVICE_SEARCH_RSP"

    fields_desc = SDP_BASE.fields_desc + [
        ShortField("TotalServiceRecordCount", 0x0000),
        ShortField("CurrentServiceRecordCount", 0x0000),
        DataElementField("ServiceRecordHandleList", None),
        ContinuationStateField("ContinuationState", {
            "InfoLength": 0
        })
    ]


# 4.6 SERVICEATTRIBUTE TRANSACTION
## 4.6.1 SDP_SERVICE_ATTR_REQ PDU
class SDP_SERVICE_ATTR_REQ(SDP_BASE):
    name = "SDP_SERVICE_ATTR_REQ"

    fields_desc = SDP_BASE.fields_desc + [
        IntField("ServiceRecordHandle", 0x00000000),
        ShortField("MaximumAttributeByteCount", 0x0000),
        DataElementField("AttributeIDList", None),
        ContinuationStateField("ContinuationState", {
            "InfoLength": 0
        })
    ]


## 4.6.2 SDP_SERVICE_ATTR_RSP PDU
class SDP_SERVICE_ATTR_RSP(SDP_BASE):
    name = "SDP_SERVICE_ATTR_RSP"

    fields_desc = SDP_BASE.fields_desc + [
        ShortField("AttributeListByteCount", 0x0000),
        DataElementField("AttributeList", None),
        ContinuationStateField("ContinuationState", {
            "InfoLength": 0
        })
    ]


# 4.7 SERVICESEARCHATTRIBUTE TRANSACTION
## 4.7.1 SDP_SERVICE_SEARCH_ATTR_REQ PDU
class SDP_SERVICE_SEARCH_ATTR_REQ(SDP_BASE):
    name = "SDP_SERVICE_SEARCH_ATTR_REQ"

    fields_desc = SDP_BASE.fields_desc + [
        DataElementField("ServiceSearchPattern", None),
        ShortField("MaximumAttributeByteCount", 0x0000),
        DataElementField("AttributeIDList", None),
        ContinuationStateField("ContinuationState", {
            "InfoLength": 0
        })
    ]


## 4.7.2 SDP_SERVICE_SEARCH_ATTR_RSP PDU
class SDP_SERVICE_SEARCH_ATTR_RSP(SDP_BASE):
    name = "SDP_SERVICE_SEARCH_ATTR_RSP"

    fields_desc = SDP_BASE.fields_desc + [
        ShortField("AttributeListsByteCount", 0x0000),
        DataElementField("AttributeLists", None),
        ContinuationStateField("ContinuationState", {
            "InfoLength": 0
        })
    ]

