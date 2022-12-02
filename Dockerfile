FROM bentoml/model-server:0.11.0-py37
MAINTAINER ersilia

RUN conda install -c conda-forge rdkit=2021.03.4
RUN conda install pytorch torchvision torchaudio cpuonly -c pytorch
RUN conda install -c conda-forge dpu-utils
RUN conda install scikit-learn 
RUN pip install pandas
RUN pip install py-repo-root
RUN pip install pyprojroot
RUN pip install more-itertools
RUN pip install torch-scatter
RUN pip install sqalchemy==1.3.24


WORKDIR /repo
COPY . /repo
