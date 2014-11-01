# Group action on double cosets.
# Note that this is not always a well defined group action as described below.
OnDoubleCosets := function(coset, g)
      return DoubleCoset(LeftActingGroup(coset),
               OnRight(Representative(coset), g),
               RightActingGroup(coset));;
end;;


# Given UgV returns Vg^{-1}U.
DoubleCosetInverse := function(coset)
      return DoubleCoset(RightActingGroup(coset),
               Inverse(Representative(coset)),
               LeftActingGroup(coset));;
end;;


# This function returns a list of double cosets of the form UgU in G that are
# unique under inversion. That is, a complete list of such double cosets where
# we consider UgU and Ug^{-1}U to be the same.
InverseUniqueDoubleCosets := function(G, U)
    # GAP likes all the local variables at the beginning.
    local reps, cosets, uniques, skips, repi, i, j, x, xinv;
    reps := AsSet(List(DoubleCosetRepsAndSizes(G, U, U),
                       x -> x[1])); # Forget the sizes.
    cosets := List(reps, x -> DoubleCoset(U, x, U));
    uniques := [];
    skips := [];
    repi := List([1 .. Length(reps)]);
    for i in repi do
        if i in skips then
            # We have encountered the inverse of this coset.
            continue;
        fi;
        Add(uniques, i);
        x := reps[i];
        xinv := Inverse(x);
        if x <> xinv and not xinv in cosets[i] then
            # Inverse is distinct, so we need to add it to `skips`.
            if xinv in reps then
                # We found it easily (and quickly).
                Print("lucky!");
                j := Position(reps, xinv);
            else
                # Slow but sure way to find it.
                Print("notlucky!");
                j := First(repi, k -> xinv in cosets[k]);
            fi;
            if j = fail then
                Error("Wasn't able to find the coset for xinv!");
            fi;
            Add(skips, j);
        fi;
    od;
    return cosets{uniques};;
end;;

