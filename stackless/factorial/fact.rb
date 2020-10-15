# Program to find the factorial of a number
# Save this as fact.rb

def fact(n)
  if n == 0
    1
  else
    n * fact(n-1)
  end
end

def time
  start = Time.now
  yield(Time.now - start).to_s
end

puts "Factorial program using Ruby."
if (ARGV[0].nil? == false) && (ARGV[0].len > 0)
	puts fact(ARGV[0].to_i)
else
	require 'benchmark'

	Benchmark.bm(7) do |x|
	  x.report("5!") {puts '5! = ',fact(5)}
	end

	Benchmark.bm(7) do |x|
	  x.report("1000! / 998!") {puts '1000! / 998! = ',fact(1000)/fact(998)}
	end

	Benchmark.bm(7) do |x|
	  x.report("10000! / 9998!") {puts '10000! / 9998! = ',fact(10000)/fact(9998)}
	end
end


