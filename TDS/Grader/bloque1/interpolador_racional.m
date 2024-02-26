function [y, fc, B, xL, xF, xG]  = interpolador_racional(x,L,M)
%   Entradas:
% x, senyal que se va a interpolar
% L, factor de interpolación
% M, factor de diezmado
%   Salidas:
% y, senyal interpolada
% fc, B, xL, xF, xG variables para comprobacion automatica del programa

% Obliga a que la salida sea un vector columna
x = x(:);

% Calcula la frecuencia de corte del filtro
fc = 1 / (2 * max(L, M));

N = 80;

% Calcula los coeficienets del filtro paso bajo
B = fir1(N, 2*fc);

% Inserta ceros mediante la función inserta_ceros. Hay que definirla abajo
xL = inserta_ceros(x, L);

% Filtra la señal xL con el filtro paso bajo diseñado
xF = filter(B,1,xL);

% Aplica la ganancia del filtro a la señal xF
xG = xF * L;

% Diezma mediante la función diezmador. Hay que definirla abajo
y = diezmador(xG,M),

end

function y = inserta_ceros(x, L)
% Inserte aqui el codigo que programo anteriormente  
x = x(:); % Así nos aseguramos de que la entrada siempre sea un vector columna
    
N = length(x);  
y = zeros(N*L,1);
y(1:L:end) = x;
    
end

function y = diezmador(x, M)
% Inserte aqui el codigo que programo anteriormente
x = x(:); % Así nos aseguramos de que la entrada siempre sea un vector columna
    
    %Inserte su codigo a partir de aqui
y = x(1:M:end); % Se queda con una de cada M muestras  de la señal de entrada. Por ejemplo, si  y , la salida sería .
    

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Ejemplo de uso de la función interpolador_racional (se introduce en la consola de comandos de Matlab)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% n = 0:1024;
% M=8;
% L=3;

% %Sinusoide de frecuencia normalizada 0.1
% x = sin(2*pi*0.1*n);

% [y, fc, B, xL, xF, xG] = interpolador_racional(x,L,M);

% figure(1)
% subplot(121)
% plot(x)
% axis([0,100,-1.5,1.5])
% title('Senyal original')
% xlabel('n')
% subplot(122)
% plot(y)
% axis([0,100,-1.5,1.5])
% title('Senyal interpolada')
% xlabel('n')

% figure(2)
% subplot(121)
% [Px,W] = pspectrum(x);
% plot(W/2/pi,Px)
% axis([0,0.5,0,1])
% title('Senyal original en frecuencia')
% subplot(122)
% [Py, W] = pspectrum(y);
% plot(W/2/pi,Py)
% axis([0,0.5,0,1])
% title('Senyal interpolada en frecuencia')
