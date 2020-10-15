echo @off
mongrel_rails start -e development -a localhost -p 3000 -P tmp/pids/mongrel_3000.pid -l log/mongrel_3000.log
