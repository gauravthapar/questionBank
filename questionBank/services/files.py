import os


def check_file_extension(files):
    for f in files:
        extension = os.path.splitext(f.name)[1]  
        valid_extensions = [".jpg", ".png", ".jpeg", ".gif", ".tiff", ".docs", ".txt", ".pdf", ".html", ".rtf", "docx", ".pptx", ".ppt"]
        if extension.lower() in valid_extensions:
            return True
        return False