savedcmd_daxos_sec.mod := printf '%s\n'   daxos_security.o | awk '!x[$$0]++ { print("./"$$0) }' > daxos_sec.mod
