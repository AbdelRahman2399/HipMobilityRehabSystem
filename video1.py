import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
import time
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
import socket



def plotting(i,t_history, x_history,  y_history, z_history):
    ax.clear()
    ax.plot(t_history, x_history, color='r')
    ax.plot(t_history, y_history, color='g')
    ax.plot(t_history, z_history, color='b')


def main():
    try:
        while cap.isOpened():
            ret, img = cap.read()
            cv2.imshow("IMG",img)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            #cv2.imshow("IMG",gray)
            ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
            if ret == True:
                corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)

                ret, r_vec, t_vec = cv2.solvePnP(objp, corners2, intrinsic, dist)
                clientsocket.send(bytes(f"{r_vec[0]},{r_vec[2]}", "utf-8"))
                x_history.append(r_vec[0])
                y_history.append(r_vec[1])
                z_history.append(r_vec[2])
                t_history.append(time.time()-t)
            print(x_history)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                
                break
        cv2.destroyAllWindows()
        cap.release()
    except Exception as e:
        cv2.destroyAllWindows()
        cap.release()
        print(f"Error: {e}")
        

        
if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1234))
        s.listen(5)
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")
        
        file_path = 'data_webcam.pickle'
        with open(file_path,'rb') as file:
            loaded_data = pickle.load(file)

        intrinsic = loaded_data[1]
        dist = loaded_data[2]
        CHECKERBOARD = (9,6)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        objp = []
        for i in range(CHECKERBOARD[1]):
            for j in range(CHECKERBOARD[0]):
                objp.append([j*25.0, i*25.0, 0.0])

        objp = np.array(objp, np.float32)


        x_history = []
        y_history = []
        z_history = []
        t_history = []
    
        t = time.time()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ani = animation.FuncAnimation(fig, plotting, fargs=(t_history, x_history,  y_history, z_history), interval=50)
        cap = cv2.VideoCapture(0)
        thread = Thread(target=main)
        thread.start()
        plt.show()
        thread.join()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        cap.release()
        pass
    
    