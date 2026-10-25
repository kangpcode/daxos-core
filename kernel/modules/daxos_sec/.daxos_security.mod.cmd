savedcmd_daxos_security.mod := printf '%s\n'   daxos_security.o | awk '!x[$$0]++ { print("./"$$0) }' > daxos_security.mod
