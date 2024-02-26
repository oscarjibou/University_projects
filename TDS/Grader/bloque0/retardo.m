
function y = retardo(x, m)
    % Entradas:
    % x, señal a retardar,
    % m, retardo
    %
    %Salidas:
    % y, señal retardada
    N=length(x);    
    y = zeros(1,N); % Así nos aseguramos de que la entrada siempre será del tamaño de la salida
    
    if (m<N) % si m>N, la salida vale ceros y no hay que hacer nada
    
    y(1+m:end) = x(1:end-m);
        % Escribe tu código aquí
    end
    end
   