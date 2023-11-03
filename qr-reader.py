import cv2

# Sets the default
camera_id = 0
delay = 1
window_name = 'OpenCV QR Code'

# Creates a QRCodeDetector + VideoCapture object
qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture(camera_id)


# Basically just an infinite loop
goodLink = True

while goodLink:
    ret, frame = cap.read()

    if ret:
        ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
        if ret_qr:
            for s, p in zip(decoded_info, points):
                if s:
                    print(s)
                    color = (0, 255, 0)
                    goodLink = False
                    break

                else:
                    color = (0, 0, 255)
                frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
        cv2.imshow(window_name, frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break


# Now destroys the
cv2.destroyWindow(window_name)
