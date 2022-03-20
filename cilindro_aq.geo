// Gmsh project created on Fri May 28 20:49:20 2021
SetFactory("OpenCASCADE");
f=0.1;
//+
Point(1) = {0, 0, 0, f};
//+
Point(2) = {5, 0, 0, f};
//+
Point(3) = {0, 1, 0, f};
//+
Point(4) = {5, 1, 0, f};
//+
Line(1) = {3, 1};
//+
Line(2) = {1, 2};
//+
Line(3) = {2, 4};
//+
Line(4) = {4, 3};
//+

//+
Point(5) = {2.5, 0.5, -0, f};
//+
Point(6) = {2.25, 0.5, -0, f};
//+
Point(7) = {2.75, 0.5, -0, f};
//+
Point(8) = {2.5, 0.25, -0, f};
//+
Point(9) = {2.5, 0.75, -0, f};
//+
Circle(5) = {9, 5, 6};
//+
Circle(6) = {6, 5, 8};
//+
Circle(7) = {8, 5, 7};
//+
Circle(8) = {7, 5, 9};
//+
Line Loop(1) = {1, 2, 3, 4};
//+
Line Loop(2) = {5, 6, 7, 8};
//+
Plane Surface(1) = {1, 2};
//+
Physical Line("esquerda") = {1};
//+
Physical Line("inferior") = {2};
//+
Physical Line("direita") = {3};
//+
Physical Line("superior") = {4};
//+
Physical Line("circulo") = {6, 5, 8, 7};
//+
Physical Surface("sup") = {1};