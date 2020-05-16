import json
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import time

class FailureTurn(RuntimeError):

    def __init__(self, msg):
        self.msg = msg

class PyStreamCallback(StreamCallback):
  def __init__(self):
        pass
  def process(self, inputStream, outputStream):
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        obj = json.loads(text)
        
        if obj['type'] == 'chassis_can' and obj['version'] == 2: 
            newObj = {
                "timestamp": time.time(),
                "version": obj['version'],
                "type": obj['type'],
                "period": obj['period'],
                "message": obj['message']
            }
        elif obj['type'] == 'gnss' and obj['version'] == 2: 
            newObj = {
                "timestamp": time.time(),
                "version": obj['version'],
                "type": obj['type'],
                "period": obj['period'],
                "message": obj['message']
            }
        elif obj['type'] == 'dtg' and obj['version'] == 2: 
            newObj = {
                "timestamp": time.time(),
                "version": obj['version'],
                "type": obj['type'],
                "period": obj['period'],
                "message": obj['message']
            }
        elif obj['type'] == 'vehicle_state' and obj['version'] == 2: 
            newObj = {
                "timestamp": time.time(),
                "version": obj['version'],
                "type": obj['type'],
                "period": obj['period'],
                "message": obj['message']
            }
        elif obj['type'] == 'event' and obj['version'] == 2: 
            newObj = {
                "timestamp": time.time(),
                "version": obj['version'],
                "type": obj['type'],
                "period": obj['period'],
                "message": obj['message']
            }
        else:
            newObj = {}

        print(newObj)
        outputStream.write(bytearray(json.dumps(newObj, indent=4).encode('utf-8')))

flowFile = session.get()
try:
    if(flowFile != None):
        session.write(flowFile, PyStreamCallback())
        session.transfer(flowFile, REL_SUCCESS)
except FailureTurn as e:
    log.warn(str(e.msg))
    session.transfer(flowFile, REL_FAILURE)
except Exception as e:
    log.error(str(e))
    session.transfer(flowFile, REL_FAILURE)

session.commit()

