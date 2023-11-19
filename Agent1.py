from flask import Flask, render_template, request
import os
from Agent2 import Agent2
from Agent3 import Agent3

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    agent2 = Agent2()
    agent2.cleanModulesList()
    # agent3.cleanText()
    target = os.path.join(app.instance_path, 'codes')
    if not os.path.isdir(target):
        os.makedirs(target)
    #Es un post
    if request.method == "POST":
        #Comprobar si la petición contiene la parte del fichero
        if "file" in request.files:
            file = request.files["file"]
            #Comprobar que si se seleccionó un fichero para obtener su información
            if file.filename:
                destination = '/'.join([target, file.filename])
                file.save(destination)
                modules_list = agent2.getIdentifiersFromFile("instance/codes/" + file.filename)

                agent3 = Agent3("TensorFlow 2.14.0", modules_list[0])
                
                information = agent3.mainFunction()


                return render_template('index.html', title="INFORMATION", information=information)
    else:
        return render_template('index.html', title="NO CODE YET", information="")

@app.route("/response", methods=['GET', 'POST'])
def response():
    return render_template()

if __name__ == "__main__":
    app.run(debug=True)