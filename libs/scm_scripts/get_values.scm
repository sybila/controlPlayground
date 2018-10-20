#!/usr/bin/env gosh

(use util.match)
(use sad.channel3-rv)
(use sad.gauche)
(use srfi-19)
(use sad.rendezvous)
(use sad.binary-channels)
(use util.list)
(use gauche.threads)
(use sad.regression)

(define PBR07
  (make-rpc
   (make-binary-unix-client
    "/tmp/devbus" "72700008")))

(spawn-rendezvous-selector-loop)

(print (rpc2 PBR07 `(get-thermoregulator-settings )))