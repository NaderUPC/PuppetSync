#!/bin/bash

curl -sk -X GET -u usuari.ana:<XXX> \
     -H "Content-Type:application/json" \
     -H "login.username:usuarisoa.upcnet" \
     -H "login.password:<XXX>" \
     -H "domini:1123" "https://bus-soa.upc.edu/gN6/Infraestructuresv1/zoe.upc.edu/software"

curl -sk -X POST -u usuari.ana:<XXX> -d '{"versioMinor":"1.8.0_66"}' \
     -H "Content-Type:application/json" \
     -H "login.username:usuarisoa.upcnet" \
     -H "login.password:<XXX>" \
     -H "domini:1123" "https://bus-soa.upc.edu/gN6/Infraestructuresv1/zoe.upc.edu/software/Oracle Java 8"

curl -sk -X POST -u usuari.ana:<XXX> -d '{"versioMinor":"2.15-0ubuntu1"}' \
     -H "Content-Type:application/json" \
     -H "login.username:usuarisoa.upcnet" \
     -H "login.password:<XXX>" \
     -H "domini:1123" "https://bus-soa.upc.edu/gN6/Infraestructuresv1/zoe.upc.edu/software/Nagios"