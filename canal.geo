//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {3, 0, 0, 1.0};
//+
Point(3) = {3, 1, 0, 1.0};
//+
Point(4) = {0, 1, 0, 1.0};
//+
Line(1) = {1, 1};
//+
Line(2) = {1, 2};
//+
Line(3) = {2, 3};
//+
Line(4) = {3, 4};
//+
Line(5) = {4, 1};
//+
Line Loop(1) = {4, 5, 2, 3};
//+
Plane Surface(1) = {1};
//+
Physical Line("paredesup") = {4};
//+
Physical Line("paredeinf") = {2};
//+
Physical Line("in") = {5};
//+
Physical Line("out") = {3};
//+
Physical Surface(5) = {1};
