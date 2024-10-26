import os
import cv2
import torch
import zipfile
import librosa
import numpy as np
import tensorflow_addons as tfa
import tensorflow as tf
from facenet_pytorch import MTCNN
from rawnet import RawNet

# Set random seed for reproducibility.
tf.random.set_seed(42)

# Unzip the model file if not already done
local_zip = "./efficientnet-b0.zip"
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall()
zip_ref.close()

# Load the EfficientNet model
model = tf.keras.models.load_model("efficientnet-b0/")

class DetectionPipeline:
    """Pipeline class for detecting faces in the frames of a video file."""

    def __init__(self, n_frames=None, batch_size=60, resize=None, input_modality='video'):
        """Constructor for DetectionPipeline class."""
        self.n_frames = n_frames
        self.batch_size = batch_size
        self.resize = resize
        self.input_modality = input_modality

    def __call__(self, filename):
        """Load frames from a video or image, or load audio data."""
        if self.input_modality == 'video':
            print('Input modality is video.')
            return self._process_video(filename)
        elif self.input_modality == 'image':
            print('Input modality is image.')
            return self._process_image(filename)
        elif self.input_modality == 'audio':
            print('Input modality is audio.')
            return self._process_audio(filename)
        else:
            raise ValueError("Invalid input modality. Must be 'video', 'image', or 'audio'")

    def _process_video(self, filename):
        v_cap = cv2.VideoCapture(filename)
        v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if self.n_frames is None:
            sample = np.arange(0, v_len)
        else:
            sample = np.linspace(0, v_len - 1, self.n_frames).astype(int)

        faces = []
        for j in range(v_len):
            success = v_cap.grab()
            if j in sample:
                success, frame = v_cap.retrieve()
                if not success:
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if self.resize is not None:
                    frame = cv2.resize(frame, (int(frame.shape[1] * self.resize), int(frame.shape[0] * self.resize)))

                face2 = cv2.resize(frame, (224, 224))
                faces.append(face2)

        v_cap.release()
        return faces

    def _process_image(self, filename):
        image = cv2.imread(filename)
        if image is None:
            raise ValueError(f"Could not open or find the image at path: {filename}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        return image

    def _process_audio(self, filename):
        x, sr = librosa.load(filename)
        x_pt = torch.Tensor(x)
        x_pt = torch.unsqueeze(x_pt, dim=0)
        return x_pt

# Instantiate pipelines
detection_video_pipeline = DetectionPipeline(n_frames=5, batch_size=1, input_modality='video')
detection_image_pipeline = DetectionPipeline(batch_size=1, input_modality='image')

def deepfakes_video_predict(input_video):
    faces = detection_video_pipeline(input_video)
    total = 0
    real_res = []
    fake_res = []

    for face in faces:
        face2 = face / 255.0
        pred = model.predict(np.expand_dims(face2, axis=0))[0]
        real, fake = pred[0], pred[1]
        real_res.append(real)
        fake_res.append(fake)

        total += 1

        pred2 = pred[1]

        if pred2 > 0.5:
            fake += 1
        else:
            real += 1

    real_mean = np.mean(real_res)
    fake_mean = np.mean(fake_res)
    print(f"Real Faces: {real_mean}")
    print(f"Fake Faces: {fake_mean}")
    text = ""

    if real_mean >= 0.5:
        text = "The video is REAL."
        text = "The video is FAKE."

    return text


def deepfakes_image_predict(input_image):
    faces = detection_image_pipeline(input_image)
    face2 = faces / 255.0
    pred = model.predict(np.expand_dims(face2, axis=0))[0]
    real, fake = pred[0], pred[1]
    if real > 0.5:
        text2 = "The image is REAL."
    else:
        text2 = "The image is FAKE."
    return text2

def load_audio_model():
    d_args = {
        "nb_samp": 64600,
        "first_conv": 1024,
        "in_channels": 1,
        "filts": [20, [20, 20], [20, 128], [128, 128]],
        "blocks": [2, 4],
        "nb_fc_node": 1024,
        "gru_node": 1024,
        "nb_gru_layer": 3,
        "nb_classes": 2
    }
    
    model = RawNet(d_args=d_args, device='cpu')

    # Load checkpoint
    model_dict = model.state_dict()
    ckpt = torch.load('RawNet2.pth', map_location=torch.device('cpu'))
    model.load_state_dict(ckpt, strict=False)
    return model

audio_label_map = {
    0: "Real audio",
    1: "Fake audio"
}

def deepfakes_audio_predict(input_audio):
    # Unpack the input audio into x and sr (ensure input_audio contains exactly two elements)
    if isinstance(input_audio, tuple) and len(input_audio) == 2:
        x, sr = input_audio
    else:
        raise ValueError("Expected input_audio to be a tuple containing (audio_data, sample_rate)")

    x_pt = torch.Tensor(x)
    x_pt = torch.unsqueeze(x_pt, dim=0)

    # Load model
    model = load_audio_model()

    # Perform inference
    grads = model(x_pt)

    # Get the argmax
    grads_np = grads.detach().numpy()
    result = np.argmax(grads_np)

    return audio_label_map[result]

