from django.shortcuts import render
from .models import UploadedPhoto
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
import io

def index(request): 
    if request.method == 'POST' and request.FILES.get('photo'):
        uploaded_photo = request.FILES['photo']

        # Chemin de la photo de base
        base_path = 'originals/base.jpg'

        # Ouvre les images
        base_img = Image.open(f'media/{base_path}').convert('RGBA')
        user_img = Image.open(uploaded_photo).convert('RGBA')

        # Découpe les 2/3 supérieurs
        width, height = user_img.size
        crop_height = int(height * 2.5 / 3)
        user_img = user_img.crop((0, 0, width, crop_height))
        size = 420
        # Redimensionne en carré (pour cercle parfait)
        user_img = user_img.resize((size, size))

        # Crée un masque circulaire
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        # Applique le masque à l'image et créer un fond transparent
        circular_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        circular_img.paste(user_img, (0, 0), mask)
        
        # Position où coller sur la base
        position = (-35, 630)

        # Coller l'image circulaire
        base_img.paste(circular_img, position, circular_img)

        # Convertir en RGB pour sauvegarde JPEG
        result = base_img.convert('RGB')

        # Sauvegarde dans un buffer
        buffer = io.BytesIO()
        result.save(buffer, format='JPEG')
        image_file = ContentFile(buffer.getvalue(), name='result.jpg')

        # Sauvegarde en base
        photo_obj = UploadedPhoto.objects.create(
            original=uploaded_photo,
            base=base_path,
            result=image_file
        )

        return render(request, 'index.html', {'photo': photo_obj})

    return render(request, 'index.html')



'''
def index(request): 
    if request.method == 'POST' and request.FILES.get('photo'):
        uploaded_photo = request.FILES['photo']

        base_path = 'originals/base.jpg'
        base_img = Image.open(f'media/{base_path}').convert('RGBA')
        user_img = Image.open(uploaded_photo).convert('RGBA')

        width, height = user_img.size
        crop_height = int(height * 2.5 / 3)
        user_img = user_img.crop((0, 0, width, crop_height))

        # Nouvelle taille carrée plus petite
        size = int(350)

        user_img = user_img.resize((size, size))

        mask = Image.new('L', (size, size), 255)

        # Image avec fond transparent
        square_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        square_img.paste(user_img, (0, 0), mask)

        # Ajuste la position selon la nouvelle taille (exemple)
        position = (20, 675)  # Tu peux ajuster X ou Y ici si besoin

        base_img.paste(square_img, position, square_img)

        result = base_img.convert('RGB')

        buffer = io.BytesIO()
        result.save(buffer, format='JPEG')
        image_file = ContentFile(buffer.getvalue(), name='result.jpg')

        photo_obj = UploadedPhoto.objects.create(
            original=uploaded_photo,
            base=base_path,
            result=image_file
        )

        return render(request, 'index.html', {'photo': photo_obj})

    return render(request, 'index.html')

'''
