def knapsack01(W,N,v,w):
    DP = [[0 for _ in range(W+1)] for _ in range(N+1)] # Defining DP 

    for i in range(1,N+1) :
        for j in range(1,W+1) :
            if w[i-1] <= j : 
                # Taking max of both the cases i.e to take that 
                # item or to ignore it.
                DP[i][j] = max(v[i-1]+DP[i-1][j-w[i-1]],DP[i-1][j]) 

            else :
                # If the weight of current element is greater 
                # than the space left in the bag we'll ignore it.
                DP[i][j] = DP[i-1][j]
    # returning answer for W space and N items 
    return DP[N][W]

def main():  
    w = [100, 300, 50, 100]
    v = [-2.73, -7.6, -1.8, -2.73]
    print(knapsack01(100, 4, v, w))
    
if __name__ == "__main__":
    main()