# g:=Group((1,2,3,4),(1,2));;n:=Subgroup(g,[(1,2)(3,4),(1,3)(2,4)]);;
# hom:=NaturalHomomorphismByNormalSubgroup(g,n);
# Size(ImagesSource(hom));

http://en.wikipedia.org/wiki/Wreath_product


EmbeddedWreathSquareSymmetries := function(W, A1, A2)
    local A1tilde, A2tilde, tau;
    A1tilde := Image(Embedding(W,1), A1);
    A2tilde := Image(Embedding(W,2), A2);
    tau := Image(Embedding(W,3));
    return [Group(Union([A1tilde, A2tilde, tau])), [tau]];
end;;
fs:=SymmetricGroup(3);
w:=WreathProduct(fs,SymmetricGroup(2));
e:=EmbeddedWreathSymmetries(w, Subgroup(w,[(1,2)]), Subgroup(w,[(1,2)]));

x:=Subgroup(W,[(5,6)]);

PermOfWreathElt := function(n, g)
    local t;
    t := OnTuples([1..(2*n)], g);
    return [t{[1..n]}, t{[(n+1)..(2*n)]} - n];
end;;
PermOfWreathElt(3,(5,6));

i1 := Embedding(w,1);
i2 := Embedding(w,2);
Image(i1, Subgroup(g,[(1,2)]));
Image(i2, Subgroup(g,[(1,2)]));
a :=
Subgroup(w,
Union([Image(i1, Subgroup(g,[(1,2)])),
       Image(i2, Subgroup(g,[(1,2)])),
       Image(Embedding(w,3))
       ]));
c := DoubleCosets(w, a, a);
Size(c);

c := RightCosets(w, a);
Size(c);

RightCoset(a,(1,2)) = RightCoset(a,(4,5));

(1,2,3) * tau;

tauL := GeneratorsOfGroup(Image(Embedding(w,3)));
tau := tauL[1];

b :=
Subgroup(w,
Union([Image(i1, Subgroup(g,[(1,2)])),
       Image(i2, Subgroup(g,[(1,2)]))
       ]));

