from PIL import Image

def main():
    image = Image.open(r"C:\Users\Hello\Desktop\AUR-Training-26\task_2\subtask_2\image_project\img.png")
    bw_image = image.convert("L")
    bw_image.show()

if __name__ == "__main__":
    main()