function y = descuantificador(x,nbits)
   % Calcular Delta
   delta = 1 / (2^(nbits - 1));

   % Calcular salida
   y = x .* delta;
end

% Ejemplo de uso 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% nbits = 5;

% xq = -2^(nbits-1):2^(nbits-1);

% xr = dequantificador(xq,nbits);

% stem(xq,xr);
% title('Respuesta del decuantificador')
% grid
