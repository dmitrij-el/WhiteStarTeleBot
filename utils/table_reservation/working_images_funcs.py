from PIL import Image, PngImagePlugin
from data.models_peewee import data_tables
from datetime import datetime
import os


async def processing_images(close_tables_list: list) -> Image:
    plan = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plan.png'))
    reserved = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reserved.png'))
    modified_plan = plan.copy()
    for num_close_table in close_tables_list:
        for tables in data_tables:
            if tables['number_table'] == num_close_table:
                cor_x = tables['cor_x']
                cor_y = tables['cor_y']
                modified_plan.paste(reserved, (cor_x, cor_y))
    if not close_tables_list:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plan.png')
    file_name = f'utils/table_reservation/modified_plans/modified_plan{datetime.now().strftime("%d%m%Y%H%M%S")}.png'
    modified_plan.save(file_name)
    return file_name
