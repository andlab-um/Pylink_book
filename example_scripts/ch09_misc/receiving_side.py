import pylink
import pylsl
 
# open a data outlet to stream data
info = pylsl.stream_info("EyeLink","Gaze", 3, 500, pylsl.cf_float32,"eyelink")
outlet = pylsl.stream_outlet(info)

# connect to the tracker
tracker = EyeLink("100.1.1.1")
# set sampling rate to 500 Hz
tracker.sendCommand('sample_rate 500') 

# start recording
tracker.startRecording(1, 1, 1, 1)         
 
print("Retrieving and streaming samples...")
while True:
    smp = tracker.getNewestSample()
    if smp is not None:
        now = pylsl.local_clock()
        em_sample = [0, 0, 0]
        if smp.isLeftSample():
            em_sample[0:2] = smp.getLeftEye().getGaze()
            em_sample[2] = smp.getLeftEye().getPupilSize()
        else:
            em_sample[0:2] = smp.getRightEye().getGaze()
            em_sample[2] = smp.getRighttEye().getPupilSize()

        # push the gaze sample to the network
        outlet.push_sample(pylsl.vectord(em_sample), now, True)
