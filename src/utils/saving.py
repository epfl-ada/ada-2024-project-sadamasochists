import os

# Get the saving path for a specific file
def get_saving_path(subtask,file_name,is_image=False):
    file_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(os.path.join(file_path, '../../docs'),'img' if is_image else 'plots',subtask)
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.join(path,file_name)


print(get_saving_path('NLP', 'test.txt'))