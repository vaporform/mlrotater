from ursina import *
from ursina.prefabs import video_recorder
from PIL import Image
import numpy
import os

def load_texture(path):
    try:
        return Texture(path)
    except FileNotFoundError:
        print("Error: Texture file not found!")
        return None
start = False

app = Ursina()
modeler = Entity(model='quad',texture="brick")
bg = Entity(model='quad',color=color.white,scale=3,z=5)
texture_field = InputField(y=.4,register_mouse_input=True, default_value='path/to/pics/here', active=True)

b = Button(model='quad', scale=.1, y=.3, color=color.lime, text='retexture', text_size=.5, text_color=color.black)
b2 = Button(model='quad', scale=.1, y=.2, color=color.red, text='convert', text_size=.5, text_color=color.black)
b3 = Button(model='quad', scale=.1, y=.3,x=.1, color=color.pink, text='srs: false', text_size=.5, text_color=color.black)

angledeb = ThinSlider(text='Angle x', dynamic=True, min=0,max=360,step=1, y=-.3)
angledeb2 = ThinSlider(text='Angle y', dynamic=True, min=0,max=360,step=1, y=-.35)
angledeb3 = ThinSlider(text='Angle z', dynamic=True, min=0,max=360,step=1, y=-.4)
vr = video_recorder.VideoRecorder(duration=10000000000)

def on_button_click():
    new_texture = load_texture(texture_field.text)
    modeler.rotation = Vec3(0,0,0)
    if new_texture is not None:
        modeler.texture = new_texture
    else:
        print("Texture loading failed. Please check the path.")

b.on_click = on_button_click  # Assign the click handler

def crop_images(folder_path, output_folder="output", crop_box=(666, 342, 861, 520)):
  # Create the output folder if it doesn't exist
  if not os.path.exists(output_folder):
      os.makedirs(output_folder)

  for filename in os.listdir(folder_path):
      # Check for image extensions (modify as needed)
      if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
          image_path = os.path.join(folder_path, filename)
          try:
              img = Image.open(image_path)
              cropped_img = img.crop(crop_box)
              cropped_img.save(os.path.join(output_folder, filename))
              os.remove(image_path)
          except (IOError, OSError) as e:
              print(f"Error processing {filename}: {e}")

def start_session():
    if angledeb.value != 0 or angledeb2.value != 0 or angledeb3.value != 0:
        global start
        vr.start_recording()
        start = not start
        b3.text = f"srs: {start}"
    else:
        b3.text = f"srs: 000?"

b3.on_click = start_session

def update():
    global start
    if not start:
        modeler.rotation = 0
    else:
        modeler.rotation_x += int(angledeb.value)
        modeler.rotation_y += int(angledeb2.value)
        modeler.rotation_z += int(angledeb3.value)

        if modeler.rotation_x >= 360 or modeler.rotation_y >= 360 or modeler.rotation_z >= 360:
            vr.stop_recording()
            start = not start
            crop_images("video_temp")

app.run()
