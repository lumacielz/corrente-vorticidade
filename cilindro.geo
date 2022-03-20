//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {3, 0, 0, 1.0};
//+
Point(3) = {3, 1, 0, 1.0};
//+
Point(4) = {0, 1, 0, 1.0};
//+
Point(5) = {1.5, 0.5, 0, 1.0};
//+
Point(6) = {1.5, 0.6, 0, 1.0};
//+
Point(7) = {1.6, 0.5, 0, 1.0};
//+
Point(8) = {1.4, 0.5, 0, 1.0};
//+
Point(9) = {1.5, 0.4, 0, 1.0};
//+
Circle(1) = {8, 5, 6};
//+
Circle(2) = {6, 5, 7};
//+
Circle(3) = {7, 5, 9};
//+
Circle(4) = {9, 5, 8};
//+
Line(5) = {4, 3};
//+
Line(6) = {3, 2};
//+
Line(7) = {2, 1};
//+
Line(8) = {1, 4};
//+
Line Loop(1) = {5, 6, 7, 8};
//+
Line Loop(2) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1, 2};
//+
Physical Line("paredeinf") = {7};
//+
Physical Line("paredesup") = {5};
//+
Physical Line("in") = {8};
//+
Physical Line("out") = {6};
//+
Physical Line("cilindro") = {1, 2, 3, 4};
//+
Physical Surface("superficie") = {1};
//+
Physical Point("center") = {5};
