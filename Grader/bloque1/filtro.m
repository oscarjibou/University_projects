function minAtenuacion = filtro()
    L = 5
    M = 3
    
    %Obtenga el valor de la frecuencia de corte del filtro
    fc = 1 / (2 * max(L, M));
    
    N = 60 % Orden del filtro 
    
    %Calculo de los coeficientes del filtro con la función fir1, 
    %tenga en cuenta que debe multiplicar por 2 el valor de fc
    B = fir1(N, 2*fc);
    
    %Obtenga la respuesta en frecuencia con freqz
    
    [H,W]= freqz(B,1);
    
    % Convierta W a frecuencia normalizada
    f = W/(2*pi);
    % Representación en escala lineal
    figure(1)
    %inserte aqui la instruccion con el plot
    plot(f, abs(H))
    
    title('Respuesta en frecuencia (escala lineal)')
    xlabel('Frecuencia normalizada')
    ylabel('abs(H)')
    
    % Convierta el resultado a dBs
    Hdb = 20*log10(abs(H));
    
    %Representación en dBs
    figure(2)
    %inserte aqui la instruccion con el plot
    plot(f,Hdb)
    title('Respuesta en frecuencia (escala dBs)')
    xlabel('Frecuencia normalizada')
    ylabel('abs(H) (dB)')
    
    %Una vez ejecute el script descomente la siguiente linea y completela con el valor observado el la grafica
    minAtenuacion = 52.3381;
    
end 

%matlab -batch "B=filtro()" 