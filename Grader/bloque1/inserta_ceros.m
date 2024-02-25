function y = inserta_ceros(x, L)
    % Entradas:
    % x, senyal a la que insertar ceros,
    % L, factor de interpolación
    %
    %Salidas:
    % y, vector interpolado
        
    x = x(:)'; % Así nos aseguramos de que la entrada siempre sea un vector columna
    
    %Inserte su codigo a partir de aqui
        
    y = zeros(1, length(x)*L);
    y(1:L:end) = x;
    
    end
    
    %matlab -batch "x = 1:4;L=2;y = inserta_ceros(x,L)"