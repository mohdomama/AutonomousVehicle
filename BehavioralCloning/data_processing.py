import csv
from matplotlib import pyplot as plt
import cv2
from sklearn.model_selection import train_test_split
import numpy as np
import os



def read_raw_csv_data(csv_path):
    ''' Reads CSV data from simulator
        Uses only center images
    '''
    with open(csv_path, newline='') as f:
        csv_data = list(csv.reader(f, skipinitialspace=True, delimiter=',', quoting=csv.QUOTE_NONE))
    
    image_paths, angles = [], []
    for row in csv_data:
        # Only consider data when speed > 0.2
        if float(row[6]) < 0.2:
            continue

        angle = float(row[3])
        image_paths.append(row[0])
        angles.append(angle)

    return image_paths, angles

def read_csv_data(csv_path):
    with open(csv_path, newline='') as f:
        csv_data = list(csv.reader(f, skipinitialspace=True, delimiter=',', quoting=csv.QUOTE_NONE))
    
    image_paths, angles = [], []
    for row in csv_data:
        angle = float(row[1])
        image_paths.append(row[0])
        angles.append(angle)

    return image_paths, angles


def display_data(image_paths, angles):
    for i, path in enumerate(image_paths):
        img = cv2.imread(path, 0)
        # img = cv2.resize(img, (160, 80))
        print(angles[i], img.shape)
        cv2.imshow('frame', img)
        cv2.waitKey(10)
    cv2.destroyAllWindows()

def get_image_data(image_paths, angles):
    X, Y = [], []
    for i, path in enumerate(image_paths):
        img = cv2.imread(path, 0)
        X.append(img)
    Y = angles + []
    return X, Y

def clean_data(ang_max, skip_count):
    csv_path = 'simulator-linux/driving_log.csv'
    image_paths, angles = read_raw_csv_data(csv_path)

    new_data = []
    straight_count = 0
    for i, path in enumerate(image_paths):
        if 0.0 <= angles[i] <= ang_max:
            if straight_count % skip_count == 0:
                img = cv2.imread(path, 0)
                cv2.imwrite(path[78:], img)
                new_data.append([path[78:], angles[i]])
                
            straight_count += 1
    
        else:
            img = cv2.imread(path, 0)
            cv2.imwrite(path[78:], img)
            new_data.append([path[78:], angles[i]])
    
    with open('driving_log.csv', mode='a') as f:
        for data in new_data:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(data)

def show_clead_data(flip_angle):
    csv_path = 'driving_log.csv'
    image_paths, angles = read_csv_data(csv_path)
    
    print(len(angles))
    print(len(image_paths))

    # clean_data(image_paths, angles)
    plt.hist(angles, 20, facecolor='green')
    plt.show()

    flipped = [-x for x in angles if abs(x) > flip_angle]
    print(len(angles+flipped))
    plt.hist(angles + flipped, 20, facecolor='green')
    plt.show()

def delete_previous_data():
    os.system('rm -r IMG/*')
    os.system('rm driving_log.csv')

def show_raw_data():
    csv_path = 'simulator-linux/driving_log.csv'
    image_paths, angles = read_raw_csv_data(csv_path)
    
    print(len(angles))
    print(len(image_paths))

    # clean_data(image_paths, angles)
    plt.hist(angles, 20, facecolor='green')
    plt.show()


def main():
    # clean_data(ang_max=0.05, skip_count=10)
    show_clead_data(0.10)

    # show_raw_data()




if __name__=='__main__':
    main()