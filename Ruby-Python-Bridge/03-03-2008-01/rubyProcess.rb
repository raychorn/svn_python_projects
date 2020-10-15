#!/usr/bin/env ruby
require "socket"

_Code1 = "x = lib01.func(102)"
_Code2 = "x = lib01.func(x)"
_Code3 = "x = lib01.func(x)"
_Code4 = "'x = (%s)' % (str(x))"

_Queue_i = 0
_Queue = ['100/3', '200*3', 'len(str(100/3))', 'import lib01', _Code1, _Code2, _Code3, _Code4, 'xxxShutdownxxx']

sock = TCPSocket.open("localhost", 2727)
loop do
    cmd = _Queue[_Queue_i]
    printf 'Sending... cmd=(%s)', cmd
    puts ''
    sock.send(cmd,0)
    str = sock.recv(1024)
    break if str.length == 0
    printf 'Received... (%s)', str
    puts ''
    _Queue_i += 1
    if (_Queue_i > (_Queue.length - 1)) then
        break
    end
    #sleep(1)
end

