function y = diezmador(x, M)
    % Entradas:
    % x, senyal entrada
    % M, factor de diezmado
    %
    %Salidas:
    % y, senyal diezmada
        
    x = x(:); % Así nos aseguramos de que la entrada siempre sea un vector columna
    
    %Inserte su codigo a partir de aqui
    
    y = x(1:M:end); % Se queda con una de cada M muestras  de la señal de entrada. Por ejemplo, si  y , la salida sería .
    
    end

    % Se queda con una de cada M muestras  de la señal de entrada. Por ejemplo, si  y , la salida sería .

    %comando: matlab -batch "y=diezmador([1:10],3)" 