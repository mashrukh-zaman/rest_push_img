import torch
import os
import pandas as pd
from PIL import Image
from torch.nn.modules.distance import PairwiseDistance
from . import config
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk
from tkinter.messagebox import showinfo


class SearchCattle:
    def __init__(self, embedding_dir, model, device, transform):
        self.transform = transform
        self.model = model
        self.device = device

        self.lower_threshold = config.lower_threshold
        self.upper_threshold = config.upper_threshold
        self.embedding_df = pd.read_excel(embedding_dir, index_col=0)
        

    def set_threshold(self, lower_threshold, upper_threshold):
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        
        
    def find_match(self, image_dir):

        lower_threshold = self.lower_threshold
        upper_threshold = self.upper_threshold
        cattle_names = self.embedding_df.columns
        base_name = os.path.basename(image_dir)

        pdist = PairwiseDistance(2)
        image_embd = torch.from_numpy(get_embedding(image_path=image_dir,\
                                                    model=self.model, device=self.device,\
                                                    transform=self.transform)).to(device=self.device)
        def dist_func(cattle_name):
            embd_to_cmp = torch.from_numpy(self.embedding_df[cattle_name].values).to(device=self.device)
            dist = pdist(embd_to_cmp, image_embd).detach().cpu().numpy().item()
            return (cattle_name, dist)
        
        
        
        distances = dict(map(dist_func, cattle_names))
        min_value = min(distances.values())
        
        if min_value <= lower_threshold:
            matched_cattle = min(distances, key=distances.get)
            if base_name.split('_')[0] == matched_cattle:
                print_msg = config.CGREEN+f'Matched with {matched_cattle}'+ config.CEND
            else:
                print_msg = config.CGREEN+f'Matched with '+config.CEND \
                             + config.CRED+f'{matched_cattle}'+config.CEND 

        elif lower_threshold < min_value <= upper_threshold:
            print_msg = config.CVIOLET+'Please provide a better image'+config.CEND
        else:
            print_msg = config.CRED+'Not Enrolled in database'+config.CEND
        
        print(print_msg, end='\n')
        # showinfo(title="Search Result", message=print_msg)
        print(f'Minimum distance: {min_value}', end='\n\n')

        
        


class ImageBrowser(tk.Tk):
    def __init__(self, search_cattle_object):
        super().__init__()
        
        self.search_cattle_object = search_cattle_object

        self.title('Enrollment checking')
        self.geometry('300x450')
        
        self.button = ttk.Button(self, text='Browse Image')
        self.button['command'] = self.check_enrollment
        self.button.pack()

        self.label = tk.Label(self)
        self.label.pack()

        self.frame = tk.Frame()

    def check_enrollment(self):

        def show_image(image_path):
            img = Image.open(image_path)
            img.thumbnail((250,250))
            img  = ImageTk.PhotoImage(img)
            self.label.configure(image=img)
            self.label.image = img

        self.image_dialog_box = \
        filedialog.askopenfilename(initialdir= config.all_img_dir, 
                                    title = "Select an Image", 
                                    filetypes= (("PNG files", "*.png*"), ("all files", "*.*")))
        show_image(self.image_dialog_box)
        self.search_cattle_object.find_match(self.image_dialog_box)




def get_embedding(image_path, model, device, transform):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).reshape(1, 3, 224, 224).to(device)
    image_embd = model(image).detach().cpu().numpy().flatten()
    return image_embd

def get_embedding_view(image, model, device, transform):
    
    image = transform(image).reshape(1, 3, 224, 224).to(device)
    image_embd = model(image).detach().cpu().n.flatten()
    return image_embd


def create_embeddings(root_dir, embd_dir, model, device, transform):
    cattle_names = list(os.walk(root_dir))[1:]
    all_embd_dict = {}

    if not os.path.isdir(embd_dir):
        os.makedirs(embd_dir)
    
    def get_path(embd_dir, cattle_name):
        image_root_dir = cattle_name[0]
        image_name = cattle_name[2][0]
        base_name = os.path.basename(image_root_dir)
        image_path = os.path.join(image_root_dir, image_name)
        xlsx_name = image_name.split('.')[0] + '.xlsx'
        xlsx_folder_path = os.path.join(embd_dir, base_name)
        if not os.path.isdir(xlsx_folder_path):
            os.mkdir(xlsx_folder_path)
        xlsx_path = os.path.join(xlsx_folder_path, xlsx_name)
        return image_path, xlsx_path, base_name

    for cattle_name in cattle_names:
        image_path, xlsx_path, base_name = get_path(embd_dir, cattle_name)
        image_embd = get_embedding(image_path, model, device, transform)
        df_embd = pd.DataFrame(image_embd)
        all_embd_dict[base_name] = image_embd
        df_embd.to_excel(xlsx_path)

    all_embd_df = pd.DataFrame(all_embd_dict)
    all_embd_df.to_excel(os.path.join(embd_dir, 'all_embeddings.xlsx'))


def check_bulk_enrollment(search_cattle_obj, data_dir):
    folders = list(os.walk(data_dir))[1:]
    for folder in folders:
        folder_dir = folder[0]
        images = folder[2]
        print(f'Testing for {os.path.basename(folder_dir)}: ')
        print('---------------------------------')

        for image in images:
            print(f'For {image}: ')
            cattle_img = os.path.join(folder_dir, image)
            search_cattle_obj.find_match(cattle_img)
        print()
            
def check_single_enrollment(search_cattle_obj):
    img_gui = ImageBrowser(search_cattle_obj)
    img_gui.mainloop()


    
