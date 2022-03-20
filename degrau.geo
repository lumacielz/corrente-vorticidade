//+
Point(1) = {1, 1, 0, 1.0};
//+
Point(2) = {1, 0, 0, 1.0};
//+
Point(3) = {7, 0, 0, 1.0};
//+
Point(4) = {7, 2, 0, 1.0};
//+
Point(5) = {0, 2, 0, 1.0};
//+
Point(6) = {0, 1, 0, 1.0};
//+
Line(1) = {2, 3};
//+
Line(2) = {3, 4};
//+
Line(3) = {4, 5};
//+
Line(4) = {5, 6};
//+
Line(5) = {6, 1};
//+
Line(6) = {1, 2};
//+
Line Loop(1) = {3, 4, 5, 6, 1, 2};
//+
Plane Surface(1) = {1};
//+
Physical Line("cavidade") = {6, 5};
//+
Physical Line("paredeinf") = {1};
//+
Physical Line("paredesup") = {3};
//+
Physical Line("in") = {4};
//+
Physical Line("out") = {2};
//+
Physical Surface(6) = {1};
