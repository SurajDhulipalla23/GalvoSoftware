# test_guiapp.py
import pytest
from logic import ImageLogic
from GUIapp import GUIApp
from PIL import Image
import tkinter as tk

@pytest.fixture
def root():
    return tk.Tk()

@pytest.fixture
def logic():
    return ImageLogic()

@pytest.fixture
def app(root, logic):
    return GUIApp(root, logic)

def test_open_image(app):
    app.open_image()
    # assert not app.placeholder_label.winfo_exists()

def test_save_image(app):
    # Mock the filedialog.asksaveasfilename method
    app.save_image()  # You can provide a mocked file path here if needed

def test_update_timestamp(app):
    # Mock the root.after method to immediately call the update_timestamp method
    app.update_timestamp() 
    # Assert that the timestamp label is updated after 1 second
    old_timestamp = app.timestamp_label.cget('text')
    app.root.update_idletasks()  # Update the GUI to trigger the timestamp update
    new_timestamp = app.timestamp_label.cget('text')
    # assert old_timestamp != new_timestamp



# # test_guiapp.py
# import pytest
# from unittest.mock import MagicMock
# from logic import ImageLogic
# from GUIapp import GUIApp
# from PIL import Image, ImageTk
# import tkinter as tk

# @pytest.fixture
# def logic():
#     return ImageLogic()

# @pytest.fixture
# def app(root, logic):
#     return GUIApp(root, logic)

# @pytest.fixture
# def test_open_image(app):
#     # Mock file dialog to return a file path
#     app.logic.load_image = MagicMock(return_value=Image.new("RGB", (100, 100)))
#     app.root.filename = "test_image.jpg"
#     app.open_image()
#     assert app.logic.load_image.called

# @pytest.fixture
# def test_save_image(app):
#     # Mock file dialog to return a file path
#     app.logic.save_image = MagicMock()
#     app.save_image()
#     assert app.logic.save_image.called

# @pytest.fixture
# def test_update_timestamp(app):
#     # Assert that the timestamp label is updated after 1 second
#     old_timestamp = app.timestamp_label.cget('text')
#     app.update_timestamp()
#     app.root.after(1000)
#     new_timestamp = app.timestamp_label.cget('text')
#     assert old_timestamp != new_timestamp

# # Run the tests
# def test_guiapp():
#     root = tk.Tk()
#     logic = ImageLogic()
#     app = GUIApp(root, logic)
#     test_open_image(app)
#     test_save_image(app)
#     test_update_timestamp(app)
