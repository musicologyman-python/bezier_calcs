#!/usr/bin/env python


from sympy import *

init_printing()

# do i need this line?
n, k, t = symbols('n k t')

bernstein_polynomial = binomial(n, k) * t**k * (1 - t)**(n - k)

cubic_bernstein_polynomial = bernstein_polynomial.subs({'n': 3})

def get_cubic_bernstein_polynomial(k):
    return cubic_bernstein_polynomial.subs({'k': k})

b3 = cubic_bernstein_polynomial

for k in range(4):
    print(get_cubic_bernstein_polynomial(k))

p = [Symbol(f'P_{i}') for i in range(4)]

cubic_bezier = sum([b3.subs({'k': i}) * p[i] for i in range(4)])
cubic_bezier


# In[17]:


from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
    
    def to_vector(self):
        return Matrix([self.x, self.y])


# In[18]:


import more_itertools

bezier3_control_points_string = '0.0 0.0 -45.0 0.0 -69.0 -34.0 -69.0 -88.0'
chunked_points = more_itertools.chunked(
                    (float(s)for s in bezier3_control_points_string.split()), 2)
control_points = [Point(*chunk) for chunk in chunked_points]
control_point_vectors = [pt.to_vector() for pt in control_points]
control_point_vectors


# In[19]:


control_point_subs = {p: x for p, x in zip((f'P_{i}' for i in range(4)), control_point_vectors)}
control_point_subs


# In[20]:


d1b = diff(cubic_bezier.subs(control_point_subs), 't')


# In[21]:


d1b.row(0).col(0)


# In[22]:


d1b.row(1)


# In[23]:


d1b[0]


# In[24]:


d1b[1]


# In[25]:


solve(d1b[0]), solve(d1b[1])


# In[26]:


cubic_bezier.subs(control_point_subs).subs({'t': 1})


# In[27]:


current_bezier = simplify(cubic_bezier.subs(control_point_subs))
current_bezier


# In[28]:


plot_parametric(current_bezier[0], current_bezier[1], ('t', 0, 1))


# In[29]:


y = symbols('y')
p1 = plot_parametric(current_bezier[0], current_bezier[1], ('t', 0, 1), show=False)
p2 = plot_parametric(-69, y, (y, -100, 0), show=False)
p1.append(p2[0])
p1.show()


# In[30]:


x, y = symbols('x y')
p1 = plot(x + 3, (x, -10, 50), show=False)
p2 = plot(10, (y, -10, 50), show=False, line_color='red')
p1.append(p2[0])
p1.show()


# In[ ]:




