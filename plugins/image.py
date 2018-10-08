import boto3
from PIL import Image

IMAGE_DIR = './data/'
SHOWWIN_FACE_WIDTH = 218
SHOWWIN_FACE_HEIGHT = 320
S3_BUCKET = 'showwin-face'
MASK = './data/mask.png'
SHOWWIN_BASE = './data/showwin.png'


def upload_image(file_path):
    s3 = boto3.resource('s3')
    s3.Bucket(S3_BUCKET).upload_file(IMAGE_DIR + file_path, file_path)


def get_face_coordinate(file_path):
    """
    画像の中に写っている顔の座標の配列を返す
    """
    bucket = S3_BUCKET
    client = boto3.client('rekognition')

    response = client.detect_faces(Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': file_path
        }}, Attributes=['ALL'])

    face_count = len(response["FaceDetails"])
    print(f'Detected {face_count} faces for {file_path}')
    if face_count == 0:
        return None

    coordinate_list = []
    for face_info in response['FaceDetails']:
        coordinate_list.append(face_info['BoundingBox'])
    return coordinate_list


def get_face_part(face_crd, filename):
    img = Image.open(IMAGE_DIR + filename)
    width = img.width * face_crd['Width']
    height = img.height * face_crd['Height']
    left = img.width * face_crd['Left']
    top = img.height * face_crd['Top']

    # 取得部分が顔に近すぎるのでもう少し周囲も取る
    reduction_rate_width = 1 / 12  # 顔の左右を元画像の 1/12 だけ広く取る
    reduction_rate_top = 7 / 48  # 顔の上を元画像の 7/48 だけ広く取る
    reduction_rate_down = 1 / 48  # 顔の下を元画像の 1/48 だけ広く取る
    face_part = img.crop((
        max(left - width * reduction_rate_width, 0),
        max(top - (height * reduction_rate_top), 0),
        left + width * (1 + reduction_rate_width),
        top + height * (1 + reduction_rate_down)))
    return face_part


def resize_to_showwin(face_part):
    # face_part の高さを SHOWWIN_FACE_HEIGHT に合わせて拡大/縮小
    ratio = SHOWWIN_FACE_HEIGHT / face_part.height
    resized_face = face_part.resize(
        (int(face_part.width * ratio), int(face_part.height * ratio))
    )

    # face を mask のサイズに合わせる
    # face の方が横に大きいので、その部分を切り取る
    resized_face = resized_face.crop((
        (resized_face.width - SHOWWIN_FACE_WIDTH) / 2,
        0,
        SHOWWIN_FACE_WIDTH + (resized_face.width - SHOWWIN_FACE_WIDTH) / 2,
        SHOWWIN_FACE_HEIGHT))

    return resized_face


def create_showwin_icon(filename, filetype):
    file_path = filename + '.' + filetype
    upload_image(file_path)
    face_crd_list = get_face_coordinate(file_path)

    image_files = []

    for i, face_coordinate in enumerate(face_crd_list):
        face_part = get_face_part(face_coordinate, file_path)
        face = resize_to_showwin(face_part)

        # base に face をマージ
        base = Image.open(SHOWWIN_BASE)
        base.paste(face, (142, 273), Image.open(MASK))  # 顔画像の左上の座標
        image_file = f'{filename}-{i}.{filetype}'
        base.save(IMAGE_DIR + image_file)
        image_files.append(image_file)

    return image_files
