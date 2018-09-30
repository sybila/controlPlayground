; #!/usr/bin/env gosh

; (use util.match)
; (use sad.channel3-rv)
; (use sad.gauche)
; (use srfi-19)
; (use sad.rendezvous)
; (use sad.binary-channels)
; (use util.list)
; (use gauche.threads)
; (use sad.regression)

; (define PBR07
;   (make-rpc
;    (make-binary-unix-client
;     "/tmp/devbus" "72700007")))

; (spawn-rendezvous-selector-loop)

; (define now
;   (let ((t0 (current-time)))
;     (lambda ()
;       (time->seconds (time-difference (current-time) t0)))))

; (while #t    
;   (let ((t (now)))

;     (apply
;      print
;      (intersperse
;       ","
;       (list
;        t
;        (rpc2 PBR07 `(get-ph 5 0))
;        (rpc2 PBR07 `(get-current-temperature))
;       ;  (rpc2 GAS01 `(get-co2-air))
;       ; AKCNI ZASAH prihlad:
;       ;  (rpc2 GMS01 `(set-valve-tflow 0 5) ; prvni parametr 0 je CO2
;       ;  (rpc2 GMS01 `(set-valve-tflow 1 495) ; druhý parametr 1 je vzduch = 1% CO2 ve vzduchu pro takto nastavene
;       ; vysledna koncentrace v % je definovana jako (flowCO2 / (flowCO2 + flowAir) + 400 / 1e6) * 100 || v ppm flowCO2 / (flowCO2 + flowAir) * 1e6 + 400
;        )))
;     (thread-sleep! 3) ;pauza
;   )
; )

(print 
  (intersperse
      ","
      (list
        1.9
        2.7
        3.333)
    )
) 