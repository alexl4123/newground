valves_number(24).
%valves_number(5).
valves_per_pipe(2).
tank(1).
tank(7).
tank(9).
junction(1). pipe(1,2). dem(1,2,39).
pipe(1,11). pipe(1,12). dem(1,12,56). dem(1,11,59).
junction(2). pipe(2,3). dem(2,3,23).
pipe(2,14). dem(2,14,29). 
junction(3). pipe(3,4). dem(3,4,26).
junction(4). pipe(4,5). dem(4,5,39).
pipe(4,20). dem(4,20,29). 
junction(5). pipe(5,6). dem(5,6,29).
junction(6). pipe(6,7). dem(6,7,16).
junction(7). pipe(7,8). dem(7,8,30).
junction(8). pipe(8,9). dem(8,9,33).
junction(9). pipe(9,10). dem(9,10,53).
junction(10). pipe(10,11). dem(10,11,73).
junction(11). 
junction(12). pipe(12,13). pipe(12,15). dem(12,15,56). dem(12,13,53).
junction(13). pipe(13,14). pipe(13,16). dem(13,16,35). dem(13,14,39).
junction(14). pipe(14,17). dem(14,17,36).
junction(15). pipe(15,16). dem(15,16,38).
junction(16). pipe(16,17). dem(16,17,32).
junction(17). pipe(17,18). dem(17,18,36).
junction(18). pipe(18,19). dem(18,19,39).
junction(19). pipe(19,20). dem(19,20,36).
junction(20).




swap(pipe(A,B),pipe(A,B)) :- pipe(A,B).
swap(pipe(A,B),pipe(B,A)) :- pipe(A,B).

symm_pipe(A,B) :- swap(P,pipe(A,B)).

less_ico(pipe(A,B),pipe(C,D)) :- pipe(A,B), pipe(C,D), A < C.
less_ico(pipe(A,B),pipe(A,D)) :- pipe(A,B), pipe(A,D), B < D.

drop(B,A) :- symm_pipe(A,B), tank(A), valves_per_pipe(1).
drop(A,C) :- symm_pipe(A,B), symm_pipe(A,C), B < C, not tank(A),
             #count{ D : symm_pipe(A,D) } < 3.

N <= { valve(A,B) : symm_pipe(A,B), not drop(A,B) } <= N :- valves_number(N).
:- symm_pipe(A,B), tank(A), not valve(A,B).
:- valves_per_pipe(1), valve(A,B), valve(B,A).

broken(P,P) :- swap(P,P).
broken(P,Q) :- extend(P,A), swap(Q,pipe(A,B)), not valve(A,B).
extend(P,A) :- broken(P,Q), swap(Q,pipe(A,B)), not valve(A,B), not tank(A).

reached(P,A) :- swap(P,P), tank(A).
reached(P,A) :- deliver(P,Q), swap(Q,pipe(A,B)), not extend(P,A).
deliver(P,Q) :- reached(P,A), swap(Q,pipe(A,B)), not broken(P,Q).

compare(P,Q,pipe(A,B),-N) :- less_ico(P,Q), dem(A,B,N),
                             deliver(P,pipe(A,B)), not deliver(Q,pipe(A,B)).
compare(P,Q,pipe(A,B), N) :- less_ico(P,Q), dem(A,B,N),
                             deliver(Q,pipe(A,B)), not deliver(P,pipe(A,B)).

lower(P) :- less_ico(P,Q), #sum{ N,R : compare(P,Q,R,N) } < X, X=0.
lower(Q) :- less_ico(P,Q), not lower(P).

worst_deliv_dem(A,B,N) :- deliver(P,pipe(A,B)), dem(A,B,N), not lower(P).

:~ dem(A,B,N), not worst_deliv_dem(A,B,N). [N,A,B]
