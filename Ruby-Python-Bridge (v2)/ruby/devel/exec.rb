require "rubygems"
require 'win32/process'

puts "Process::WIN32_PROCESS_VERSION=" + Process::WIN32_PROCESS_VERSION

ENV["PYTHONPATH"]="C:\\Python25\\lib;Z:\\@myMagma\\python-local-new-trunk-ruby-daemon;Z:\\@myMagma\\python-local-new-trunk;Z:\\@myMagma\\python-local-new-trunk-ruby-daemon\\bridge;Z:\\python projects\\@lib;Z:\\@myMagma\\python-local-new-trunk\\sfapi2\\sflib;"
if RUBY_PLATFORM =~ /win/i
  @pid = Process.create(
    :app_name         => "python.exe",
    :creation_flags   => Process::DETACHED_PROCESS,
    :process_inherit  => false,
    :thread_inherit   => true,
    :username         => "rhorn@magma-da.com",
    :password         => "Peekab00"
  ).process_id
elif RUBY_PLATFORM =~ /ix/i
  fork { exec("python", "salesForce.py", "--username=rhorn@magma-da.com", "--password=Peekab00") }
end
puts "Ruby Done !"
