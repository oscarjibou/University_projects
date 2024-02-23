function [med, pot] = media_potencia(x)
 
    % Calcula la media de x, med
    
    med = mean(x);
    
    % Calcula la potencia de x, pot
    
    pot = mean(x.^2);
    
    end