import os

import torch
import zipfile
import torchaudio
from glob import glob

from silero.utils import *


def silero_stt_test(name):
    """    language = 'ru'
    model_id = 'v5'
    device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU
    model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                           model='silero_stt',
                                           language='en',  # also available 'de', 'es'
                                           device=device,
                                           sp=model_id)"""

    device = torch.device('cpu')
    local_file = 'en_v6_xlarge.jit'

    model = torch.jit.load(local_file, map_location=device)
    model.eval()
    decoder = Decoder(model.labels)

    # model, decoder, utils = torch.package.PackageImporter(local_file).load_pickle("stt_models", "model")

    # download a single file in any format compatible with TorchAudio
    test_files = glob(name)
    batches = split_into_batches(test_files, batch_size=10)
    input = prepare_model_input(read_batch(batches[0]),
                                device=device)

    output = model(input)
    for example in output:
        return decoder(example.cpu())
