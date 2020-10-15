from g import symbol_Polymorphic, symbol_PDFXporter, symbol_Logos, symbol_Flexstylus, symbol_ChartsDemo

__change_log__ = {}
__change_log__[symbol_Polymorphic] = '''
Changes for v0.3.0.0:

(1). Suppress prompt for executable editor based on file types or remember the executable for each file type and use that.
(2). Allow user to edit the remembered file editor executable for each file type.
(3). Add counter to track the number of Help Requests - allow 2 per month then ask user to buy a support plan.
(4). Allow 1 update per month then ask user to buy a maintenance plan.
(5). Allow users to edit the regular expression used to determine the class hierarchy.
(6). Allow users to edit the file types being scanned based on rules.

Changes for v0.2.0.0:

(1). Tutorial Video
(2). MenuBar displays a red hint whenever the application is in full screen mode to let the user know how to ESCape full screen mode.
(3). Full-Screen toggle now works as expected.
'''

__change_log__[symbol_PDFXporter] = '''
Initial Release.
'''

__change_log__[symbol_Logos] = '''
Initial Release.
'''

__change_log__[symbol_Flexstylus] = '''
Initial Release.
'''

__change_log__[symbol_ChartsDemo] = '''
Initial Release on 03-04-2011 as Version 0.3.3.0.

Changes for v0.4.0.0:

(1). Working on adding a Dashboard to the Charts Demo Viewer - Requests per Second versus Records Per Second, etc..

Changes for v0.3.18.0:

(1). Corrected a visual issue with the Change Log display when performing an update.

Changes for v0.3.5.0:

(1). Added code to once again show the Vyper Logix Corp Logo and not onl because it is just "cool".
(2). Added code to further optimize how data is being fetched from the Google Cloud.

Changes for v0.3.4.0:

(1). Added code to validate the number of record actually received from the Cloud per Request.
(2). Added an Application Control Bar to the Charts Demo window for greater control of the Demo.
(3). Added a Slider to allow for control over the number of data points per Request.
(4). Added a Button to allow the Demo to be Paused.
(5). Added a Button to allow the Charts Demo Window to be dismissed - this was previousl done using the Close Button on the Title Window.
(6). Coded the changes for this Release in about 90 minutes (including deployment).
'''

def get_data(air_version,domainName,air_id):
    c_token = __change_log__[air_id] if (__change_log__.has_key(air_id)) else 'NOTHING'
    _data = {
        'dmg':{'v':air_version,'u':'http://%s/%s/enterprise/%s.dmg' % (domainName,air_id,air_id),'d':c_token},
        'exe':{'v':air_version,'u':'http://%s/%s/enterprise/%s.exe' % (domainName,air_id,air_id),'d':c_token},
        'deb':{'v':air_version,'u':'http://%s/%s/personal/%s.air' % (domainName,air_id,air_id),'d':c_token},
        'rpm':{'v':air_version,'u':'http://%s/%s/personal/%s.air' % (domainName,air_id,air_id),'d':c_token}
    }
    return _data
