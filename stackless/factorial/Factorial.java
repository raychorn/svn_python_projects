import java.io.*; 

/**
 * Factorial.java - 
 *   A recursive program to calculate the factorial
 *   of a number.
 *
 *   n! = n * (n-1) * (n-2) * ... * 1
 *
 *   A recursive definition of factorial is:
 *
 *   n! = 1          if n <= 1
 *      = n * (n-1)! if n > 2
 *
 * @author Grant William Braught
 * @author Dickinson College
 * @version 2/11/2000
 */
public class Factorial {
    public static void main (String[] args) {
	
	double theNum, theFact;

	String line = null;
	int val = 0;
	System.out.println("This program computes the factorial " +
			   "of a number.");
	System.out.print("Enter a number: ");
	try {
	  BufferedReader is = new BufferedReader(new InputStreamReader(System.in));
	  line = is.readLine();
	  val = Integer.parseInt(line);
	} catch (NumberFormatException ex) {
	  System.err.println("Not a valid number: " + line);
	} catch (IOException e) {
	  System.err.println("Unexpected IO ERROR: " + e);
	}
	theNum=(double) val;
	
	theFact = fact(theNum);

	System.out.println(theNum + "! = " + theFact + ".");
    }

    /**
     * Calculate the factorial of n.
     *
     * @param n the number to calculate the factorial of.
     * @return n! - the factorial of n.
     */
    static double fact(double n) {
      double _fact = 1;
      for (int i= 1; i<=n; i++){
	_fact=_fact*i;
      }
      return _fact;
  }
}
