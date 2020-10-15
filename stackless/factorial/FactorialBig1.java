import java.io.*;
import java.math.*;
import java.util.*;
class FactorialBig1{
    public static void main(String[] args)throws IOException{
        BufferedReader stdin = new BufferedReader (new InputStreamReader(System.in));
        String enteredNum;
        BigInteger bi, decrementBy = new BigInteger("1"), answer, answer2, answer3, answer4;
        //System.out.print("Enter Number: ");
        //enteredNum=stdin.readLine();
        long startTime = System.currentTimeMillis();
        
        enteredNum="1000";
        bi = new BigInteger(enteredNum);
        answer=bi;
        bi = bi.subtract(decrementBy);
        for(int i=bi.intValue();i>0;i--){
            answer = answer.multiply(bi);
            bi = bi.subtract(decrementBy);
        }
        enteredNum="998";
        bi = new BigInteger(enteredNum);
        answer2=bi;
        bi = bi.subtract(decrementBy);
        for(int i=bi.intValue();i>0;i--){
            answer2 = answer2.multiply(bi);
            bi = bi.subtract(decrementBy);
        }
        System.out.println("1000!/998! = " +(answer.divide(answer2)));

        long endTime = System.currentTimeMillis();
        System.out.println("Runtime is :"+ (double)(endTime-startTime)/1000.0);

        startTime = System.currentTimeMillis();

        enteredNum="10000";
        bi = new BigInteger(enteredNum);
        answer3=bi;
        bi = bi.subtract(decrementBy);
        for(int i=bi.intValue();i>0;i--){
            answer3 = answer3.multiply(bi);
            bi = bi.subtract(decrementBy);
        }
        enteredNum="9998";
        bi = new BigInteger(enteredNum);
        answer4=bi;
        bi = bi.subtract(decrementBy);
        for(int i=bi.intValue();i>0;i--){
            answer4 = answer4.multiply(bi);
            bi = bi.subtract(decrementBy);
        }
        System.out.println("10000!/9998! = " +(answer3.divide(answer4)));
        endTime = System.currentTimeMillis();
        System.out.println("Runtime is :"+ (double)(endTime-startTime)/1000.0);
    }
}
