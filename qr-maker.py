import qrcode

correction = int(input("Enter level of error correction wanted (0 to 30): "))
error = qrcode.constants.ERROR_CORRECT_L
if correction > 25:
    error = qrcode.constants.ERROR_CORRECT_H
elif correction > 15:
    error = qrcode.constants.ERROR_CORRECT_Q
elif correction > 7:
    error = qrcode.constants.ERROR_CORRECT_M

size = int(input("Enter size: "))
border = int(input("Enter border size: "))

qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_L,
    box_size = size,
    border = border,
)

url = input("Enter link: ")
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
type(img)  # qrcode.image.pil.PilImage
img_name = input("Enter png name: ")
img.save(img_name + ".png")
