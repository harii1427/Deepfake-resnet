import gradio as gr
import pipeline
from block import blockchain_upload_interface

title = "EfficientNetV2 Deepfakes Video Detector"
description = "EfficientNetV2 Deepfakes Image Detector by using frame-by-frame detection."


def upload_to_blockchain(file_path):
    # Use the blockchain_upload_interface function from blockchain.py
    return blockchain_upload_interface(file_path)


def modified_deepfakes_video_predict(file_path):
    # Upload the video file to blockchain before processing
    blockchain_tx_hash = upload_to_blockchain(file_path)
    return pipeline.deepfakes_video_predict(file_path), blockchain_tx_hash


def modified_deepfakes_image_predict(file_path):
    # Upload the image file to blockchain before processing
    blockchain_tx_hash = upload_to_blockchain(file_path)
    return pipeline.deepfakes_image_predict(file_path), blockchain_tx_hash


def modified_deepfakes_audio_predict(file_path):
    # Upload the audio file to blockchain before processing
    blockchain_tx_hash = upload_to_blockchain(file_path)
    return pipeline.deepfakes_audio_predict(file_path), blockchain_tx_hash


video_interface = gr.Interface(
    modified_deepfakes_video_predict,
    gr.Video(label="Upload Video"),
    ["text", "text"],
    examples=["videos/celeb_synthesis.mp4", "videos/real-1.mp4"],
    cache_examples=False
)

image_interface = gr.Interface(
    modified_deepfakes_image_predict,
    gr.Image(label="Upload Image"),
    ["text", "text"],
    examples=["images/lady.jpg", "images/fake_image.jpg"],
    cache_examples=False
)

audio_interface = gr.Interface(
    modified_deepfakes_audio_predict,
    gr.Audio(label="Upload Audio"),
    ["text", "text"],
    examples=["audios/DF_E_2000027.flac", "audios/DF_E_2000031.flac"],
    cache_examples=False
)

app = gr.TabbedInterface(
    interface_list=[image_interface, video_interface, audio_interface],
    tab_names=['Image inference', 'Video inference', 'Audio inference']
)

if __name__ == '__main__':
    app.launch(share=False)
