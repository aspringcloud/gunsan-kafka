import json
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import time

class FailureTurn(RuntimeError):

    def __init__(self, msg):
        self.msg = msg

class ModJSON(StreamCallback):

  def __init__(self):
        pass
  
  def process(self, inputStream, outputStream):
    text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
    obj = json.loads(text)
    newObj = {}
    if obj['type'] == 'pocapay' and obj['version'] == 1:
      obj['timestamp'] = time.time()*1000
    elif obj['type'] == 'gnss' and obj['version'] == 2:
      obj['timestamp'] = time.time()*1000
    else:
      raise FailureTurn(obj) 

    outputStream.write(bytearray(json.dumps(obj, indent=4).encode('utf-8')))

flowFile = session.get()

try:
    if(flowFile != None):
        session.write(flowFile, ModJSON())
        session.transfer(flowFile, REL_SUCCESS)
except FailureTurn as e:
    log.warn(str(e.msg))
    session.transfer(flowFile, REL_FAILURE)
except Exception as e:
    log.error(str(e))
    session.transfer(flowFile, REL_FAILURE)

session.commit()