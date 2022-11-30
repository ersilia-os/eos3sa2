FROM bentoml/model-server:0.11.0-py37
MAINTAINER ersilia

RUN conda install -c conda-forge rdkit=2021.03.4
RUN conda install pytorch torchvision torchaudio cpuonly -c pytorch
RUN pip install -U scikit-learn
RUN pip install pandas

WORKDIR /repo
COPY . /repo
