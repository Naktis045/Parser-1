import pytesseract
import asyncio
import os
import cv2
from telethon.sync import TelegramClient, events
from pars_conf import account # импортируем данные из файла конфигурации


api_id = account[0]  # задаем API
api_hash = account[1]  # задаем HASH
channel_id = account[0]
print(account)


pytesseract.pytesseract.tesseract_cmd='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
client = TelegramClient('my_account', account[0], account[1])  # собираем телеграм клиента


async def process_image_and_send_text():
    await client.start()
    image = await cv2.imread('photo.jpg')# Load the image
    gray = await cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# Convert the image to grayscale
    _, thresh = await cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)# Apply a threshold to get binary image
    contours, _ = await cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# Find contours in the binary image
    contours = sorted(contours, key= await cv2.contourArea, reverse=True)[:7]# Sort contours by area in descending order
# Draw outlines around the 7 largest squares
    for contour in contours:
        x, y, w, h = await cv2.boundingRect(contour)
        await cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    await cv2.imwrite('r_photo.jpg', image)# Save the processed image
# Remove the original image file
    await os.remove('photo.jpg')# Remove the original image file
    processed_image = await cv2.imread('r_photo.jpg')# Load the processed image
# Extract text from the 7 outlined squares
    text = ""
    for contour in contours:
        x, y, w, h = await cv2.boundingRect(contour)
        square_image = processed_image[y:y + h, x:x + w]
        text += pytesseract.image_to_string(square_image)
        print(text) # Print the extracted text
# Send the extracted text to the user
        await client.forward_messages(account[2],text)
        await client.send_message(api_id, f"Extracted Text:\n{text}")
        await asyncio.sleep()
        await asyncio.create_task(process_image_and_send_text())
        await client.disconnect()


if __name__ == '__main__':
    while True:
        if os.path.exists('photo.jpg'):
            process_image_and_send_text()
  
