from  cleaner_api import setup, start, move, turn, set_state, stop


setup >>  move(100) >> turn(-90) >> set_state("soap") >> start() >> move(50) >> stop()
