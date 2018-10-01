import subprocess

games = []

for i in range(5):
    p = subprocess.Popen(["python3", "start.py"], shell=True,
                         stdin=None, stdout=None, stderr=None, close_fds=True)

    print("Process: {}, State: {}".format(p.pid, p.poll()))
    games.append(p)

while len(games) > 0:
    for game in games:
        returncode = game.poll()

        if returncode is None:
            continue

        print("Process: {}, State: {}".format(game.pid, returncode))
        games.remove(game)
