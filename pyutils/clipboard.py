from Foundation import *
from AppKit import *

# Sets the clipboard to a string
def pbcopy(s):
    pb = NSPasteboard.generalPasteboard()
    pb.declareTypes_owner_([NSStringPboardType], None)
    newStr = NSString.stringWithString_(s)
    newData = newStr.nsstring().dataUsingEncoding_(NSUTF8StringEncoding)
    pb.setData_forType_(newData, NSStringPboardType)

# Gets the clipboard contents
def pbpaste():
    pb = NSPasteboard.generalPasteboard()
    content = pb.stringForType_(NSStringPboardType)
    return content
