require 'SalesForcePy'

_address = "127.0.0.1"
_base_port = 55555
_username = "rhorn@magma-da.com"
_password = "Peekab00"

py = SalesforcePy.new(_address,_base_port,verbose=true)
puts py

# This Sample performs a SOQL Query.
_soql = "Select c.Case_Watcher__c, c.Email__c, c.Id, c.Name from Case_Watcher_List__c c where c.Email__c = 'name@domain.com'"
_xml = '<bridge username="' + _username + '" password="' + _password + '" staging="1"><soql>' + _soql + '</soql></bridge>'

_xml_queue = []
_xml_queue.push(_xml)

1.times do |i|
  printf "%s :: ", i+1
  xml = py.query(_xml_queue[0])
  puts xml
  puts ''
end

assert_match(/\A<data(?>.*?<\/data>)\Z/, xml)

# This Sample performs an Object Creation.
_xml = '<bridge username="' + _username + '" password="' + _password + '" staging="1"><create table="Case_Watcher_List__c"><column name="Name" value="+++"/><column name="Email__c" value="name@domain.com"/><column name="Case_Watcher__c" value="a0t30000000CsCnAAK"/></create></bridge>'

_xml_queue = []
_xml_queue.push(_xml)

1.times do |i|
  printf "%s :: ", i+1
  xml = py.query(_xml_queue[0])
  puts xml
  puts ''
end

assert_match(/\A<data(?>.*?<\/data>)\Z/, xml)

py.close_connection