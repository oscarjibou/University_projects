function y = inserta_ceros(x, L)
    % Entradas:
    % x, senyal a la que insertar ceros,
    % L, factor de interpolación
    %
    %Salidas:
    % y, vector interpolado
        
    if L <= 1
        error('L debe ser mayor que 1');
    end

    x = x(:)'; % Así nos aseguramos de que la entrada siempre sea un vector columna
    
    %Inserte su codigo a partir de aqui
        
    y = zeros(1, length(x)*L);
    y(1:L:end) = x; % Insertamos los valores de x en las posiciones 1, L+1, 2L+1, 3L+1, etc.
                   % y(1:L:end) = x reemplaza cada L-ésimo elemento de y con el elemento correspondiente de x.

    end
    
    %matlab -batch "x = 1:4;L=2;y = inserta_ceros(x,L)"