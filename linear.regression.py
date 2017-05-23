from numpy import arange,array,ones#,random,linalg
from pylab import plot,show
from scipy import stats

xi = arange(0,9)
A = array([ xi, ones(9)])
# linearly generated sequence
y = [19, 20, 20.5, 21.5, 22, 23, 23, 25.5, 24]

print A
slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)

print 'r value', r_value
print  'p_value', p_value
print 'standard deviation', std_err

# r_value is the correlation coefficient and 
# p_value is the p-value for a hypothesis test whose null hypothesis is that the slope is zero.

line = slope*xi+intercept
plot(xi,line,'r-',xi,y,'o')
show()
