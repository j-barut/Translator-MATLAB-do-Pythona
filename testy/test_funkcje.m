function [res] = skomplikowana_funkcja(n, m)
    res = 0;
    for i = 1:n
        if (i < m) && (i > 0)
            res = res + i;
        elseif i == m
            res = res + 100;
        else
            res = res - 1;
        end
    end
    
    while res < 200
        res = res + 10;
        if res == 150
            break;
        end
    end
end

disp(skomplikowana_funkcja(2, 3))