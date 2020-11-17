from subprocess import call

def RestartService():

    cmd='systemctl restart raspotify'
    call(cmd, shell=True)
