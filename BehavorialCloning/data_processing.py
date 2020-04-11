import csv
from matplotlib import pyplot as plt
import cv2

def read_csv_data(csv_path):
    ''' Reads CSV data from simulator
        Uses only center images
    '''
    with open(csv_path, newline='') as f:
        csv_data = list(csv.reader(f, skipinitialspace=True, delimiter=',', quoting=csv.QUOTE_NONE))
    
    image_paths, angles = [], []
    straight_count = 0
    for row in csv_data:
        # Only consider data when speed > 0.2
        if float(row[6]) < 0.2:
            continue

        angle = float(row[3])
        if 0.0 <= angle <= 0.09:
            if straight_count % 10 == 0:
                image_paths.append(row[0])
                angles.append(angle)
            straight_count += 1
    
        else:
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
        

def main():
    csv_path = 'driving_log.csv'
    image_paths, angles = read_csv_data(csv_path)
    
    print(len(angles))
    print(len(image_paths))


    # display_data(image_paths, angles)
    flipped = [-x for x in angles if x<0.0 or x>0.25]

    plt.hist(angles, 20, facecolor='green')
    plt.show()

    plt.hist(angles + flipped, 20, facecolor='green')
    plt.show()


if __name__=='__main__':
    main()