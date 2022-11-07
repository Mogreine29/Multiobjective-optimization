Pseudo-code

PLS = Pareto Local Search
```
while P != 0 do
    for all x in P do
        for all x' in N(x) do
            if y(x) < y(x') and y(x)!=y(x') then
                if Update(A,x') then
                    Pa <- Pa U {x'}
                endif
            endif
        endfor
    endfor
P<-Pa
Pa<-0
```
with A = initial solutions to explore  
Pa = interesting solutions to explore further  
N(x) denotes neighboorhood of x and Update() the Pareto Archive (A)  