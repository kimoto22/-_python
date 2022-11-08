import thinkgear
import datetime
import re
import csv
import threading
import keyboard
import sys
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2

def record(cap, out, fil):
    tm=cv2.TickMeter()
    tm.start()
    count = 0
    count1 = 0
    max_count = 1
    fps = 0
    n = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if count == max_count:
                tm.stop()
                fps = max_count / tm.getTimeSec()
                tm.reset()
                tm.start()
                count = 0
            cv2.putText(frame, 'FPS: {:.2f}'.format(fps),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
            #cv2.putText(frame, 'Frame:{:.0f}'.format(count1),(1000, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
            out.write(frame)
            #cv2.imshow('camera', frame)
            fil.write(str(count1) + "," + str(fps) + "\n")
            count1 += 1
            count += 1

            k = cv2.waitKey(1)
            if k == 27:    # Esc key to stop
                break
        else:
            break

    fil.close()
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():

    """file_path = "./csv/"+datetime.datetime.now().strftime('%Y_%m_%d %H.%M.%S.%f')[:-3]+".csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(["date", "POOR SIGNAL", "delta", "theta", "lowalpha", "highalpha", "lowbeta", "highbeta", "lowgamma", "midgamma", "ATTENTION eSense", "MEDITATION eSense", "russell_arousal", "Beta/Alpha"])
    """
    time = datetime.datetime.now().strftime('%Y_%m_%d %H.%M.%S.%f')[:-3]
    f = open('./csv/'+time+'.csv', 'w')
    f1 = open('./csv/a_raw/'+time+'_raw.csv', 'w')
    write = csv.writer(f,lineterminator="\n")
    write1 = csv.writer(f1,lineterminator="\n")
    write.writerow(["date", "POOR SIGNAL", "delta", "theta", "lowalpha", "highalpha", "lowbeta", "highbeta", "lowgamma", "midgamma", "ATTENTION eSense", "MEDITATION eSense", "russell_arousal", "Beta/Alpha"])
    write1.writerow(["time","raw_wave"])

    PORT = 'COM4'

    for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
        a = []

        if keyboard.is_pressed("escape"):
            print("end")
            fil.close()
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            sys.exit()
        for p in packets:
            #print(p)
            time = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            b = [time, p.value]
            write1.writerow(b)
            #print(b)
            #print(time.microsecond)


            if isinstance(p, thinkgear.ThinkGearRawWaveData):
                continue
            print(p)
            if type(p.value) == thinkgear.thinkgear.EEGPowerData:
                m = re.findall(r'\d+', str(p.value))
                a=a+m
            else:
                a.append(str(p.value))

            if int(a[0])>10:
                print("not fitted properly!!!")
                break

        if a!=[] and int(a[0])<10:
            time = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            #print(time)
            a.insert(0, time)

            attention = int(a[10])
            meditation = int(a[11])

            highAlpha = int(a[5])
            lowAlpha = int(a[4])
            highBeta = int(a[7])
            lowBeta = int(a[6])

            alpha = float(lowAlpha) + float(highAlpha)
            beta = float(lowBeta) + float(highBeta)


            if (attention + meditation != 0):
                russell_arousal = (float(attention - meditation) / float(attention + meditation)) * 100.0
                concentrate = beta / alpha
                print("russell_arousal:"+str(russell_arousal))
                a.append(russell_arousal)
                a.append(concentrate)

            print(a)
            write.writerow(a)



if __name__ == '__main__':

    dt_before = datetime.datetime.now().strftime('%Y/%m/%d %H.%M.%S.%f')[:-3]
    print("Camera start:"+str(dt_before))
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    fps = 30
    w = 1280
    h = 720
    cap.set(cv2.CAP_PROP_FPS, fps)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'));

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(fps)
    print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    m="test1"
    name="./camera/"+str(m)
    txt_name = str(name)+'.txt'
    fil = open(str(txt_name), 'w')
    #print(f)
    camera_name = str(name)+'_video.mp4'
    out = cv2.VideoWriter(str(camera_name), fourcc, fps, (w, h))
    dt_after = datetime.datetime.now().strftime('%Y/%m/%d %H.%M.%S.%f')[:-3]

    print("Camera after start:"+str(dt_after))
    fil.write("Camera start,"+str(dt_before)+"\nCamera after start,"+str(dt_after)+"\nresolution,"+str(w)+"*"+str(h)+"\nMovie FPS,"+str(fps)+"\n")
    fil.write("frame,FPS\n")
    thread = threading.Thread(name="thread", target=record, args=[cap, out, fil])#, daemon=True)
    thread.daemon = True
    thread.start()


    main()


    fil.close()
    cap.release()
    out.release()
    cv2.destroyAllWindows()

