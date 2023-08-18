# To create a program that uses facial recognition to examine a set of images and categorize them into folders corresponding to identified actors using face recognition.

import os
import face_recognition
import shutil

def load_face_encodings_from_folder(folder_path):
    face_encodings = []
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        img = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(img)
        if len(face_encoding) == 1:
            face_encodings.append(face_encoding[0])
    return face_encodings

def recognize_and_organize(actors_folder, photos_folder):
    
    actors_folder = os.path.abspath(actors_folder)
    photos_folder = os.path.abspath(photos_folder)

    #  face encodings from reference image from actor folder
    actors = os.listdir(actors_folder)
    actor_encodings = {}
    for actor in actors:
        actor_folder_path = os.path.join(actors_folder, actor)
        actor_encodings[actor] = load_face_encodings_from_folder(actor_folder_path)

    for actor in actors:
        actor_folder = os.path.join(os.getcwd(), actor)
        if not os.path.exists(actor_folder):
            os.makedirs(actor_folder)

    image_files = [f for f in os.listdir(photos_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Performing face recognition and move images to thwe actor's folders
    for image_file in image_files:
        image_path = os.path.join(photos_folder, image_file)
        img = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(img)

        if len(face_locations) == 1:
            face_encoding = face_recognition.face_encodings(img, face_locations)[0]

            recognized_actor = None
            min_distance = float("inf")
            for actor, encodings in actor_encodings.items():
                for encoding in encodings:
                    distance = face_recognition.face_distance([encoding], face_encoding)
                    if distance < min_distance:
                        min_distance = distance
                        recognized_actor = actor


            if recognized_actor:
                shutil.move(image_path, os.path.join(os.getcwd(), recognized_actor, image_file))
            else:
                print(f"Could not recognize any known actor for {image_file}")
        else:
            print(f"Could not recognize face in {image_file} or there are multiple faces.")

if __name__ == "__main__":
    # actors_folder contains reference images which is used by face_recognition module to load face encodings of the actors
    actors_folder = "actors_folder"

    photos_folder = "photos"
    recognize_and_organize(actors_folder, photos_folder)
