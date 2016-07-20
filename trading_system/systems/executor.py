import threading
import traceback
from datetime import datetime


class SystemExecutor(object):
    def __init__(self, system, interval):
        """
        :type system: trading_system.systems.interfaces.ITradingSystem
        :type interval: long
        """
        self.system = system
        self.interval = interval

    def execute(self):
        try:
            self.system.run()
        except Exception as e:
            curr = datetime.now()
            print('{time} - {text} - {args}'.format(time=curr.strftime('%Y-%m-%d %H:%M:%S'), text=str(e), args=e.args))
            traceback.print_exc()

        if self.interval:
            threading.Timer(self.interval, self.execute).start()
