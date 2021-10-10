import turtle as t
t.speed(10)
#hello abd how r u?
# all good
# kita koro?
# nana
# tumar
# amaro nai tumar oi


def sum(num1, num2):
  return str(num1 + num2)

def draw_rect(a:int, b:int, col='yellow') -> None:
  t.fillcolor(col)
  t.begin_fill()
  for _ in range(2):
    t.fd(a)
    t.lt(90)
    t.fd(b)
    t.lt(90)
  t.end_fill()

def draw_square(side: int, col='cyan') -> None:
  t.fillcolor(col)
  t.begin_fill()
  for _ in range(4):
    t.forward(side)
    t.left(90)
  t.end_fill()

def draw_triagle(side: int, col='lime') -> None:
  t.fillcolor(col)
  t.begin_fill()
  for _ in range(3):
    t.fd(side)
    t.lt(120)
  t.end_fill()

list = ['a','b','c','d','e']
a,b,c=10,20,30
print(a,b,c,sep='\n')

draw_square(100)
draw_rect(120, 80)
draw_triagle(100)
print(sum(b,c)[0])
