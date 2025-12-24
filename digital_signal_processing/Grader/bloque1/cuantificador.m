function y = cuantificador(x,nbits)
    % Comprueba si hay saturación y si la hay, recorta al rango [-1,1]
    x(x > 1) = 1;
    x(x < -1) = -1;

    % Realiza la cuantificacion. La salida es un número entero
    y = round(x * (2^(nbits-1)));

end

%Ejemplo de uso de la función
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% x = linspace(-2,2,1000);
% nbits = 4;
% xq = quantificador(x,nbits);

% % Comprobamos respuesta. Hay que fijarse que sature si x>1 o x<-1
% plot(x,xq);
% title('Respuesta del cuantificador')
% grid

