# g:=Group((1,2,3,4),(1,2));;n:=Subgroup(g,[(1,2)(3,4),(1,3)(2,4)]);;
# hom:=NaturalHomomorphismByNormalSubgroup(g,n);
# Size(ImagesSource(hom));

http://en.wikipedia.org/wiki/Wreath_product


g:=SymmetricGroup(3);
p:=SymmetricGroup(2);
w:=WreathProduct(g,p);

dp:=DirectProduct(g,g);

RightCoset(Group( [ (), (4,5), (1,2) ] ),(5,6));
a:=Subgroup(w, [ (), (4,5), (1,2) ] );
RightCosets(w,a);

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



b :=
Subgroup(w,
Union([Image(i1, Subgroup(g,[(1,2)])),
       Image(i2, Subgroup(g,[(1,2)]))
       ]));

