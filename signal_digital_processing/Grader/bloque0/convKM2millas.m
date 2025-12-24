
function Lmillas = convKM2millas(Lkm)
    % Insertar el codigo
    factorConversion = 0.621371;
    Lmillas = Lkm * factorConversion;
end

%% Comand to use is: 
% matlab -batch "Lkm = [42, 180, 212]; Lmillas = convKM2millas(Lkm); disp(Lmillas)" 
