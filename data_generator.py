import os
import random
import cv2
from PIL import Image, ImageFilter, ImageOps
import numpy as np

from computer_text_generator import ComputerTextGenerator

try:
    from handwritten_text_generator import HandwrittenTextGenerator
except ImportError as e:
    print('Missing modules for handwritten text generation.')
from background_generator import BackgroundGenerator
from distorsion_generator import DistorsionGenerator


class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        cls.generate(*t)

    @staticmethod
    def crop_like_segment(img):
        img = np.array(img)
        list_index = np.array(np.where(img == 255))
        x_min = np.min(list_index[0])
        x_max = np.max(list_index[0])
        y_min = np.min(list_index[1])
        y_max = np.max(list_index[1])
        if x_max != img.shape[1]:
            x_max += 1
        if y_max != img.shape[0]:
            y_max += 1
        if x_max == img.shape[1]:
            border_image = np.array(img[x_min:, y_min: y_max])
        elif y_max == img.shape[0]:
            border_image = np.array(img[x_min: x_max, y_min:])
        else:
            border_image = np.array(img[x_min:x_max, y_min:y_max])
        border_image = cv2.cvtColor(border_image, cv2.COLOR_GRAY2BGR)
        new_height, new_width, _ = border_image.shape
        top, bottom, left, right = 0, 0, 0, 0
        delta = abs(new_height - new_width)
        if new_height > new_width:
            left = right = delta // 2
        elif new_width > new_height:
            bottom = top = delta // 2
        # border_image = cv2.copyMakeBorder(border_image, top, bottom, left, right, cv2.BORDER_CONSTANT, (0, 0, 0))
        # print("size: ", np.max(new_height, new_width))
        add = np.max([new_height, new_width])//8
        index_top = random.choice([-1, 0, 1])
        index_left = random.choice([-1, 0, 1])
        top += add + index_top
        bottom += add - index_top
        left += add + index_left
        right += add - index_left
        border_image = cv2.copyMakeBorder(border_image, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                          (0, 0, 0))

        resized_border_image = cv2.resize(border_image, (50, 50))
        resized_border_image = cv2.cvtColor(resized_border_image, cv2.COLOR_BGR2GRAY)
        return resized_border_image

    @classmethod
    def generate(cls, index, text, font, out_dir, size, extension, skewing_angle, random_skew, blur, random_blur,
                 background_type, distorsion_type, distorsion_orientation, is_handwritten, name_format, width,
                 alignment, text_color, orientation, space_width, dilate_size, scale_ratio, erode_size):
        image = None
        ##########################
        # Create picture of text #
        ##########################
        if is_handwritten:
            if orientation == 1:
                raise ValueError("Vertical handwritten text is unavailable")
            image = HandwrittenTextGenerator.generate(text)
        else:
            image = ComputerTextGenerator.generate(text, font, text_color, size, orientation, space_width)

        random_angle = random_skew

        rotated_img = image.rotate(skewing_angle if not random_skew else random_angle, expand=1)

        #############################
        # Apply distorsion to image #
        #############################
        if distorsion_type == 0:
            distorted_img = rotated_img  # Mind = blown
        elif distorsion_type == 1:
            distorted_img = DistorsionGenerator.sin(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )
        elif distorsion_type == 2:
            distorted_img = DistorsionGenerator.cos(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )
        else:
            distorted_img = DistorsionGenerator.random(
                rotated_img,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
            )

        ##################################
        # Resize image to desired format #
        ##################################

        # # Horizontal text
        # if orientation == 0:
        #     new_width = int(float(distorted_img.size[0] + 10) * (float(size) / float(distorted_img.size[1] + 10)))
        #     resized_img = distorted_img.resize((new_width, size - 10), Image.ANTIALIAS)
        #     background_width = width if width > 0 else new_width + 10
        #     background_height = size
        # # Vertical text
        # elif orientation == 1:
        #     new_height = int(float(distorted_img.size[1] + 10) * (float(size) / float(distorted_img.size[0] + 10)))
        #     resized_img = distorted_img.resize((size - 10, new_height), Image.ANTIALIAS)
        #     background_width = size
        #     background_height = new_height + 10
        # else:
        #     raise ValueError("Invalid orientation")
        background_height = distorted_img.size[1]
        background_width = distorted_img.size[0]
        resized_img = distorted_img
        #############################
        # Generate background image #
        #############################
        if background_type == 0:
            background = BackgroundGenerator.gaussian_noise(background_height, background_width)
        elif background_type == 1:
            background = BackgroundGenerator.plain_white(background_height, background_width)
        elif background_type == 2:
            background = BackgroundGenerator.quasicrystal(background_height, background_width)
        else:
            background = BackgroundGenerator.picture(background_height, background_width)

        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = resized_img.size

        if alignment == 0:
            background.paste(resized_img, (0, 0), resized_img)
        elif alignment == 1:
            background.paste(resized_img, (int(background_width / 2 - new_text_width / 2), 5), resized_img)
        else:
            background.paste(resized_img, (background_width - new_text_width - 5, 5), resized_img)

        ##################################
        # Apply gaussian blur            #
        ##################################

        final_image = background.filter(
            ImageFilter.GaussianBlur(
                radius=(blur if not random_blur else random.randint(0, blur))
            )
        )

        ##################################
        # Apply scale #
        ##################################

        if scale_ratio != 0:
            final_image = final_image.resize((int(final_image.width * scale_ratio), final_image.height))
            border = int(final_image.width * (1 - scale_ratio))
            final_image = ImageOps.expand(final_image, border=(border, 0), fill='white')

        #####################################
        # Generate name for resulting image #
        #####################################
        font_name = font.split('/')[1]
        if name_format == 0:
            image_name = '{}_{}.{}'.format(text, str(index), extension)
        elif name_format == 1:
            image_name = '{}_{}.{}'.format(str(index), text, extension)
        elif name_format == 2:
            image_name = '{}_{}.{}'.format(str(font_name),str(index), extension)
        else:
            print('{} is not a valid name format. Using default.'.format(name_format))
            image_name = '{}_{}.{}'.format(text, str(index), extension)
        final_image = np.array(final_image.convert('L'), dtype=np.uint8)
        _, binary_image = cv2.threshold(final_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Dilate image
        if dilate_size != 0:
            dilate_kernel = np.ones((dilate_size, dilate_size), np.uint8)
            binary_image = cv2.dilate(binary_image, dilate_kernel, iterations=1)
        # Erode Image
        if erode_size != 0:
            erode_kernel = np.ones((erode_size, erode_size), np.uint8)
            if erode_size == 2:
                binary_image = cv2.erode(binary_image, erode_kernel, iterations=2)
            else:
                binary_image = cv2.erode(binary_image, erode_kernel, iterations=1)
        final_image = cls.crop_like_segment(binary_image)
        # final_image = binary_image
        # Save the image
        image_dir_path = os.path.join(out_dir, text)
        os.makedirs(image_dir_path, exist_ok=True)
        cv2.imwrite(os.path.join(image_dir_path, image_name), final_image)
