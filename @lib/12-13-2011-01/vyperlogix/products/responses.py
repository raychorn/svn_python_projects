from vyperlogix.hash import lists

code_error = -404
code_noUpdate = -100
code_isUpdate = 400
code_revoked = -500
code_updated = 100
code_accepted = 200
code_valid = 300
code_invalid = -301

_info_site_address = 'www.VyperLogix.com'

d_responses = lists.HashedLists2({code_error:'Warning: Unable to process your Registration.', 
                                  code_invalid:'Your registration is not valid. Please make sure your payment has processed.', 
                                  code_noUpdate:'You have the latest version.', 
                                  code_revoked:'Your product key has been revoked. You may Register again to regain access.', 
                                  code_updated:'Your registration has been updated and will be processed as quickly as possible.', 
                                  code_accepted:'Your registration has been accepted; you should receive your Product Key shortly.', 
                                  code_valid:'Your Product ID has been accepted; enjoy the power.',
                                  code_isUpdate:'There is a new version available you can download from %s.' % (_info_site_address)
                                 })
