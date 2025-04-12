models link -> https://drive.google.com/drive/folders/1fPQ2apLOn_xEjmZE-gdcMLwHbA01dKHD?usp=drive_link

This is a web application that allows users to upload black & white images and transforms them into colorized versions using a deep learning model. The frontend provides a drag-and-drop interface, and the backend uses OpenCV and a pre-trained Caffe model for colorization.

🛠️ Steps to Run This Project (for GitHub ReadMe):

Clone the Repo:

bash
Copy
Edit
git clone <your-repo-link>
cd image-colorizer
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt

Add the Model Files (manually):

Place the following in a model/ folder:

colorization_deploy_v2.prototxt

pts_in_hull.npy

colorization_release_v2.caffemodel

Run the Server:

bash
Copy
Edit
python app.py
Open the Web App: Visit http://localhost:5000 in your browser.
