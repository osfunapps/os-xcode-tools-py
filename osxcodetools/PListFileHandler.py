import plistlib

###########################################################################
#
# this module meant to manipulate plist files
#
###########################################################################
# return plist file as a dictionary
def read_plist_as_dict(plist_path):
    with open('/Users/home/Desktop/del/dell/Info.plist', 'rb') as fp:
        return plistlib.load(fp)


def save_changes(plist_path, plist):
    with open('/Users/home/Desktop/del/dell/Info.plist', 'wb') as fp:
        plistlib.dump(plist, fp)
