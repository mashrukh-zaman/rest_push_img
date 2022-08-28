from torchvision import transforms
from . import models_2 
import torch

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'
CEND    = '\033[0m'

transform = transforms.Compose([
                    transforms.Resize(224),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                ])
model = models_2.FaceNetModel()
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_state_dir = 'D:/Work/cattle_identification_v2/aPS_cattle_face.pth'
data_dir = './testing_section/data'
enrolled_img_dir = './testing_section/data/enrolled_images'
enrolled_embd_dir = './testing_section/data/enrolled_embeddings'
all_embd_xlsx = './testing_section/data/enrolled_embeddings/all_embeddings.xlsx'
all_img_dir = 'D:/Himel_APS/FaceNet/codes/version_2_codes/version_2_cattle_database/ALL'


lower_threshold = 2.6
upper_threshold = 3.0

def eval_model(model_state_dir=model_state_dir):
    model.load_state_dict(torch.load(model_state_dir, map_location=torch.device('cpu'))['state_dict'])
    model.to(device)
    model.eval()
    return model