A = [1, 2, 3; 4, 5, 6; 7, 8, 9];
B = [9, 8, 7; 6, 5, 4; 3, 2, 1];

C = A * B';
D = A .* B;
E = A.^2;
F = A^2;

res1 = (C > 10) & (D < 50);
res2 = ~res1;

disp(C);
disp(D);
disp(res1);
disp(res2);
val = (10 + 5) * 2 / 3;
check = (val == 10) || (val < 0);