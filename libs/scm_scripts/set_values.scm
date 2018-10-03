(define (main arguments)
  (for-each print (cdr arguments))
  0)

;  (rpc2 GMS01 `(set-valve-tflow 0 5) ; prvni parametr 0 je CO2
;  (rpc2 GMS01 `(set-valve-tflow 1 495) ; druhý parametr 1 je vzduch = 1% CO2 ve vzduchu pro takto nastavene
; vysledna koncentrace v % je definovana jako (flowCO2 / (flowCO2 + flowAir) + 400 / 1e6) * 100 || v ppm flowCO2 / (flowCO2 + flowAir) * 1e6 + 400
       