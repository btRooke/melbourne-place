# Implementation of the CIE 1931 lightness formula to create a lookup table for dimming
def cie1931(L):
    L = L * 100.0
    if L <= 8:
        return (L / 903.3)
    else:
        return ((L + 16.0) / 119.0) ** 3