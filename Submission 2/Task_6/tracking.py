import cv2

def Tracking(tracker_type):

    # Initialize the video capture
    # cap = cv2.VideoCapture('walking.mp4')
    capture = cv2.VideoCapture('video001_kort.mp4')

    # Initialize the tracker (e.g., using MIL tracking)
    match tracker_type:
        case "1":
            tracker = cv2.TrackerMIL_create()
        case "2":
            tracker = cv2.TrackerKCF_create()
        case "3":
            tracker = cv2.TrackerCSRT_create()
        case _:
            print("Invalid choice")
            exit()

    # Read the first frame
    ret, frame = capture.read()
    bbox = cv2.selectROI("Select Object to Track", frame)
    tracker.init(frame, bbox)

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        # Update the tracker
        success, bbox = tracker.update(frame)

        # Draw bounding box around the tracked object
        if success:
            (x, y, w, h) = tuple(map(int, bbox))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Object Tracking", frame)

        # Exit the loop if 'q' key is pressed or if the window is closed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # 'q' key or Esc key
            break

    capture.release()
    cv2.destroyAllWindows()
