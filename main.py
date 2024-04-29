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
texture_field = InputField(y=.4,x=-.5,register_mouse_input=True, default_value='path/to/pics/here', active=True)
save_field = InputField(y=.45,x=-.5,register_mouse_input=True, default_value='your image out name here', active=True)
my_video_dir = "C:/Users/Maste/Downloads/mlrotater-main/mlrotater-main/video_temp"
my_output_folder = "C:/Users/Maste/Downloads/output"

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

def start_session():
    if angledeb.value != 0 or angledeb2.value != 0 or angledeb3.value != 0:
        global start
        vr.start_recording()
        start = not start
        b3.text = f"srs: {start}"
    else:
        b3.text = f"srs: 000?"

b3.on_click = start_session

def crop_image():
    my_video_dir = "C:/Users/Maste/Downloads/video_temp"
    my_output_folder = "C:/Users/Maste/Downloads/output"
    my_newsubf = f"C:/Users/Maste/Downloads/output/{str(save_field.text)}"
    i = 0
    for filename in os.listdir(my_video_dir):
        i += 1
        print(filename)
        img = Image.open(os.path.join(my_video_dir, filename))
        #715, 349, 820, 484
        left, top, right, bottom = 715, 379, 820, 484
        cropped_img = img.crop((left, top, right, bottom))
        if not os.path.exists(my_newsubf):
            os.mkdir(os.path.join(my_output_folder, str(save_field.text)))
        
        cropped_img.save(os.path.join(my_newsubf, f"{save_field.text}{i}.png"))
    print("Success!")
b2.on_click = crop_image  # Assign the click handler
def update():
    c,v,b = 0,0,0
    global start
    if not start:
        modeler.rotation = 0
    else:
        modeler.rotation_x += int(angledeb.value)
        modeler.rotation_y += int(angledeb2.value)
        modeler.rotation_z += int(angledeb3.value)
        
        if abs(modeler.rotation_x) >= 360 or abs(modeler.rotation_y) >= 360 or abs(modeler.rotation_z) >= 360:
            vr.stop_recording()
            start = not start
            crop_image()
app.run()
