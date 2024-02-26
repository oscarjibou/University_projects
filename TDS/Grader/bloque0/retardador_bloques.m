function [bloque_ret, new_state] = retardador_bloques(bloque, m, state)
    %
    % Programa la función asumiendo que "bloque" y "state" son vectores columna
    % Los vectores de salida "bloque_ret" y "new_state" también deben ser vectores columna
    
    
    %Inicializar state con m ceros si state==[] (está vacío). Mira la ayuda de la función isempty
    if isempty(state)
        state = zeros(m,1);
    end

    
    %Generar salida bloque_ret a partir de state y bloque
    bloque_ret = [state; bloque(1:end-m)];
    
    %Generar actualizacion del estado new_state para los siguientes bloques
    new_state = bloque(end-m+1:end);
    
    end


% Ejemplo de uso

% % Generamos señal cualquiera
% x = filter(fir1(100,0.1),1, randn(1500,1));
% x = x(100:end);
% x = x(1:900); % Nos quedamos con las 900 muestras iniciales (3 bloques de 300 muestras)
% y = zeros(900,1); % Resevamos memoria

% state = []; %  Inicializamos el estado con vector vacio para el primer bloque
% for b = 1:3 
%    disp(['Procesando bloque: ',num2str(b)])
%    muestra_ini =(b-1)*300+1;
%    muestra_fin = b*300;
%    bloque = x(muestra_ini:muestra_fin);
%    [bloque_out, state] = retardador_bloques(bloque,60,state); % Retardamos y actualizamos estado
%    y(muestra_ini:muestra_fin) = bloque_out;
% end

% subplot(211)
% plot(x)
% title('original')
% subplot(212)
% plot(y)
% title('retardada')
