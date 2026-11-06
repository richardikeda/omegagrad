"""Array reverse AD plus forward directional second derivatives.

hessian_direction is d²f(x+t*v)/dt², not a dense Hessian. For independent
coordinate batches it supplies the per-coordinate Hessian. Coupled outputs
require separate directions; no full Hessian is claimed.
"""
import numpy as np
class TensorValue:
    def __init__(self,data,direction=0,children=()):
        self.data=np.asarray(data,dtype=float);self.grad=np.zeros_like(self.data)
        self.tangent=np.broadcast_to(direction,self.data.shape).copy();self.hessian_direction=np.zeros_like(self.data)
        self.parents=children;self.pull=lambda:None
    @staticmethod
    def wrap(x):return x if isinstance(x,TensorValue) else TensorValue(x)
    def addgrad(self,g):
        g=np.asarray(g)
        while g.ndim>self.data.ndim:g=g.sum(0)
        for i,s in enumerate(self.data.shape):
            if s==1:g=g.sum(i,keepdims=True)
        self.grad+=g
    def __add__(self,b):
        b=self.wrap(b);o=TensorValue(self.data+b.data,children=(self,b));o.tangent=self.tangent+b.tangent;o.hessian_direction=self.hessian_direction+b.hessian_direction
        def pull():self.addgrad(o.grad);b.addgrad(o.grad)
        o.pull=pull;return o
    __radd__=__add__
    def __mul__(self,b):
        b=self.wrap(b);o=TensorValue(self.data*b.data,children=(self,b));o.tangent=self.tangent*b.data+self.data*b.tangent;o.hessian_direction=self.hessian_direction*b.data+2*self.tangent*b.tangent+self.data*b.hessian_direction
        def pull():self.addgrad(o.grad*b.data);b.addgrad(o.grad*self.data)
        o.pull=pull;return o
    __rmul__=__mul__
    def __neg__(self):return self*-1
    def __sub__(self,b):return self+-self.wrap(b)
    def __rsub__(self,b):return self.wrap(b)+-self
    def unary(self,value,d1,d2):
        o=TensorValue(value,children=(self,));o.tangent=d1*self.tangent;o.hessian_direction=d2*self.tangent**2+d1*self.hessian_direction;o.pull=lambda:self.addgrad(o.grad*d1);return o
    def __pow__(self,n):return self.unary(self.data**n,n*self.data**(n-1),np.zeros_like(self.data) if n in (0,1) else n*(n-1)*self.data**(n-2))
    def __truediv__(self,b):return self*self.wrap(b)**-1
    def sin(self):return self.unary(np.sin(self.data),np.cos(self.data),-np.sin(self.data))
    def cos(self):return self.unary(np.cos(self.data),-np.sin(self.data),-np.cos(self.data))
    def log(self):
        if np.any(self.data<=0):raise ValueError('log domain')
        return self.unary(np.log(self.data),1/self.data,-1/self.data**2)
    def exp(self):
        e=np.exp(self.data);return self.unary(e,e,e)
    def sum(self,axis=None):
        o=TensorValue(self.data.sum(axis=axis),children=(self,));o.tangent=self.tangent.sum(axis=axis);o.hessian_direction=self.hessian_direction.sum(axis=axis)
        o.pull=lambda:self.addgrad(np.ones_like(self.data)*(o.grad if axis is None else np.expand_dims(o.grad,axis)));return o
    def backward(self):
        visited=set();order=[];stack=[(self,False)]
        while stack:
            n,done=stack.pop()
            if done:order.append(n)
            elif n not in visited:visited.add(n);stack.append((n,True));stack.extend((p,False) for p in n.parents)
        for n in order:n.grad=np.zeros_like(n.data)
        self.grad=np.ones_like(self.data)
        for n in reversed(order):n.pull()

def batch_potential(coordinates, points, epsilon, background=None):
    """Independent coordinate Hessians; chunk caller to bound memory."""
    x=TensorValue(np.asarray(coordinates)[:,None],direction=1)
    value=((x-np.asarray(points))**2+epsilon).log().sum(axis=1)
    if background is not None:
        b=x.unary(background.field(x.data),background.field(x.data,1),background.field(x.data,2)).sum(axis=1)
        value=value-b
    value.sum().backward()
    return value.data,x.grad[:,0],value.hessian_direction
