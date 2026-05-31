function [wynik] = silnia(n)
    if n < 0
        wynik = -1;
    elseif n == 0
        wynik = 1;
    else
        wynik = 1;
        for j = 1:n
            wynik = wynik * j;
        end
    end
end

a = 5;
b = silnia(a);
if b > 100
    disp('Wynik jest duży');
else
    disp('Wynik jest mały');
end