import csv
from matplotlib import pyplot as plt
import cv2
from sklearn.model_selection import train_test_split
import numpy as np



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

def get_image_data(image_paths, angles):
    X, Y = [], []
    for i, path in enumerate(image_paths):
        img = cv2.imread(path, 0)
        X.append(img)
    Y = angles + []
    return X, Y

def create_data_generator(paths, angles, is_val_data, batch_size):
    X, Y = [], []
    if is_val_data:
        for i, path in enumerate(paths):
            img = cv2.imread(path, 0)
            X.append(x)
            Y.append(angles[i])

            if len(X) == batch_size:
                X = np.array(X).reshape(-1, 160, 320, 1)
                X = X / 255.0
                yield X, Y
                X, Y = ([],[])

    else:
        for i, path in enumerate(paths):
            img = cv2.imread(path, 0)
            X.append(img)
            Y.append(angles[i])

            if len(X) == batch_size:
                X = np.array(X).reshape(-1, 160, 320, 1)
                X = X / 255.0
                yield X, Y
                X, Y = ([],[])
            
            elif abs(angles[i]) > 0.33:
                img = cv2.flip(img, 1)
                angles[i] *= -1
                X.append(img)
                Y.append(angles[i])

                if len(X) == batch_size:
                    X = np.array(X).reshape(-1, 160, 320, 1)
                    X = X / 255.0
                    yield X, Y
                    X, Y = ([],[])
        



def get_data_generators(batch_size):
    csv_path = 'driving_log.csv'
    image_paths, angles = read_csv_data(csv_path)

    # X, Y = get_image_data(image_paths, angles)

    # Y = np.array(Y)
    # X = np.array(X).reshape(-1, 160, 320, 1)
    # X = X / 255.0
    
    paths_train, paths_test, angles_train, angles_test = train_test_split(image_paths, angles, test_size=0.20)

    train_gen = create_data_generator(paths_train, angles_train, is_val_data=False, batch_size=batch_size)
    val_gen = create_data_generator(paths_test, angles_test, is_val_data=True, batch_size=batch_size)

    return train_gen, val_gen, int(len(paths_train) / batch_size)

def main():
    csv_path = 'driving_log.csv'
    image_paths, angles = read_csv_data(csv_path)
    
    print(len(angles))
    print(len(image_paths))

    # display_data(image_paths, angles)

    plt.hist(angles, 20, facecolor='green')
    plt.show()

    flipped = [-x for x in angles if x < -0.01 or x > 0.09]
    plt.hist(angles + flipped, 20, facecolor='green')
    plt.show()

    train_gen, val_gen = get_data_generators()


if __name__=='__main__':
    main()