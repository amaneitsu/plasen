# Definition of the version number
version_info = 3, 8, 0  # major, minor, patch, -extra

# Nice string for the version
__version__ = '.'.join(map(str, version_info)).replace('.-', '-').strip('.-')
