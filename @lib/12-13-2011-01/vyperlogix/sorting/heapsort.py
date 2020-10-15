import sys 

def heapsort(n, ra) : 
    ir = n 
    l = (n >> 1) + 1 

    while True : 
        if l > 1 : 
            l -= 1 
            rra = ra[l] 
        else : 
            rra = ra[ir] 
            ra[ir] = ra[1] 
            ir -= 1 
            if ir == 1 : 
                ra[1] = rra 
                return 

        i = l 
        j = l << 1 
        while j <= ir : 
            if (j < ir) and (ra[j] < ra[j + 1]) : 
                j += 1 

            if rra < ra[j] : 
                ra[i] = ra[j] 
                i = j 
                j += j 
            else : 
                j = ir + 1; 
        ra[i] = rra; 
