# ProtoNet pre-trained network embedding based on the FS-Mol dataset for few-shot learning

## Model identifiers
- Slug: fs-mol-protonet
- Ersilia ID: eos3sa2
- Tags: Embedding, Few-shot

## Model description

This model provides a 512-dimensional embedding based on the last distance layer of the Prototypical Network (ProtoNet). The pre-trained model is provided by FS-Mol, a dataset for few-shot learning

- Input: COMPOUND (Single SMILES string)
- Output: Descriptor (The output is a 512-dimensional embedding that can be used for distance calculation or as an input for machine learning predictions)
- Model type: Classification
- Training set: ChEMBL27 (233786 training samples)
- Mode of training: Pre-trained

## Source code

Stanley, M., Bronskill, J., Maziarz, K., Misztela, H., Lanini, J., Segler, M., … Brockschmidt, M. (2021, December). FS-Mol: A Few-Shot Learning Dataset of Molecules. NeurIPS 2021. Retrieved from https://www.microsoft.com/en-us/research/publication/fs-mol-a-few-shot-learning-dataset-of-molecules/

- Code: https://github.com/microsoft/FS-Mol
- Checkpoints: https://figshare.com/ndownloader/files/31307479

## License

State the licences used which are GPL v3 license used by Ersilia and the license used by the source code, if any exists. Use [this guide]() on how to license new models to be incorporated into Ersilia's model hub 

## History

- In progress
- Modified the code to extract 512-dimensional embedding based on the last distance layer of the Prototypical Network (ProtoNet).

## About us

The [Ersilia Open Source Initiative](https://ersilia.io) is a Non Profit Organization ([1192266](https://register-of-charities.charitycommission.gov.uk/charity-search/-/charity-details/5170657/full-print)) with the mission is to equip labs, universities and clinics in LMIC with AI/ML tools for infectious disease research.

[Help us](https://www.ersilia.io/donate) achieve our mission or [volunteer](https://www.ersilia.io/volunteer) with us!
