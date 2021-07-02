from numpy import dot, empty_like, array

def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def RayIntersection(a1,a2,b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
   
    x3 = ((num / denom.astype(float))*db + b1)[0]
    y3 = ((num / denom.astype(float))*db + b1)[1]

    return array([x3,y3])