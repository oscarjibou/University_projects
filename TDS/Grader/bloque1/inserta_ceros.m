function y = inserta_ceros(x, L)
    % Entradas:
    % x, senyal a la que insertar ceros,
    % L, factor de interpolación
    %
    %Salidas:
    % y, vector interpolado
 
    %Inserte su codigo a partir de aqui
    % Validación de entradas
        x = x(:); % Así nos aseguramos de que la entrada siempre sea un vector columna
    
        N = length(x);  
        y = zeros(N*L,1);
    
        y(1:L:end) = x;
    end    
    %matlab -batch "x = 1:4;L=2;y = inserta_ceros(x,L)"