savedcmd_daxos_boost.mod := printf '%s\n'   drex_boost.o | awk '!x[$$0]++ { print("./"$$0) }' > daxos_boost.mod
