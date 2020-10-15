#!/usr/bin/env ruby
require "socket"
require 'rexml/document'
include REXML

# Please do not put initializers into this class as this code may change during the development process.

class SalesforcePy
  attr_accessor :port, :addr, :verbose
  def initialize(addr, port, verbose=false)
    @addr = addr || '127.0.0.1'
    @port = port || 55555
    @verbose = verbose || false
    open_connection
  end  
     
  def to_s   
    self.class.to_s + ":: Controller Address=" + @addr.to_s + ":" + @port.to_s
  end  
  
  def open_connection
    _not_done = true
    while (_not_done)
      begin
        @sock = TCPSocket.open(@addr.to_s, @port)
        _not_done = false
      rescue
        print "An error occurred: ",$!, "\n" if @verbose
        printf 'Retrying port... (%s)', @port if @verbose
        puts '' if @verbose
      end
    end
  end
  
  def do_receive
    str = @sock.recv(1024*1024*10) # 10 MB receive buffer
    return str
  end
  
  def do_query(xml)
    # Make a simple connection...
    # First request a connection from the server...
    _not_done = true
    while (_not_done)
      begin
        puts 'Sending XML to the Bridge...' if @verbose
        @sock.send(xml,0)
        str = do_receive
        _not_done = false
      rescue
        print "An error occurred: ",$!, "\n" if @verbose
        puts 'Rescue and retry...' if @verbose
        open_connection
      end
    end
    return str
  end

  def query(xml)
    return self.do_query(xml)
  end
  
  def close_connection
    @sock.close()
  end
end

