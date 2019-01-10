from json import loads
import python3_gearman as gearman
import numpy as np
from keras.models import model_from_json
from skimage.transform import resize
from PIL import Image

import warnings
warnings.filterwarnings("ignore")
print("Ignorando warnings, especialmente do scikit-image")

gm_worker = gearman.GearmanWorker(['localhost:4730'])

def process(gearman_worker, gearman_job):
    try:
        #
        ### Carregar o modelo de arquivos JSON e H5
        #
        print("Carregando modelo")
        json_file = open("/home/diego/projetos/ferias2018.2/core/mnist/model/model.json")
        h5file = "/home/diego/projetos/ferias2018.2/core/mnist/model/model.h5"
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(h5file)

        #
        ### Ler a imagem do disco, tratá-la e  dar o veredito
        #
        arquivo_imagem = gearman_job.data
        print ("Trabalhando com %s" % arquivo_imagem)
        img = Image.open(arquivo_imagem)
        img = (img / np.max(img))[:, :, 0] * 255
        img = resize(img, (28, 28))

        entrada = np.reshape(img, (1, 784))
        resultado = loaded_model.predict(x=entrada)
        resultado = np.argmax(resultado)

        print("Resultado: ", resultado)

        return str(resultado)

    except Exception as e:
        if hasattr(e, "message"):
            gearman_worker.send_job_warning(gearman_job, e.message)
        elif hasattr(e, "args"):
            gearman_worker.send_job_warning(gearman_job, " | ".join(e.args))
        else:
            gearman_worker.send_job_warning(gearman_job, u"Uma exceção indetectável foi detectada!")
        return ''


gm_worker.set_client_id('python-worker')
gm_worker.register_task('MNISTProcess', process)
gm_worker.work()