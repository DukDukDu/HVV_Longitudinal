#include "TLorentzVector.h"
#include "TVector3.h"

void example() {
    // Create a four-vector (px, py, pz, E)
    TLorentzVector p4(10, 0, 0, 20);
    
    // Get the boost vector (beta)
    TVector3 boostVec = p4.BoostVector();

    // Create another Lorentz vector
    TLorentzVector p4_other(5, 5, 0, 15);
    
    // Boost the second vector by the boost vector obtained from the first one
    p4_other.Boost(boostVec);

    // Print the boosted vector
    p4_other.Print();
}
