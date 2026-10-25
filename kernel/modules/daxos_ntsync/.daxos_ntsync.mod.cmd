savedcmd_daxos_ntsync.mod := printf '%s\n'   ntsync.o | awk '!x[$$0]++ { print("./"$$0) }' > daxos_ntsync.mod
