import torch
import sys, os
import numpy as np
import warnings
from pathlib import Path
import whisper

def transcribe(filepath, title):
    device = torch.device('cuda')
    print('Using device:', device, file=sys.stderr)

    # Model selection
    model = 'medium'
    whisper_model = whisper.load_model(model)

    # Parameters
    language = "Auto detection"
    verbose = 'Live transcription'
    output_format = 'txt'
    task = 'transcribe'
    temperature = 0.15
    temperature_increment_on_fallback = 0.2
    best_of = 5
    beam_size = 8
    patience = 1.0
    length_penalty = -0.05
    suppress_tokens = "-1"
    initial_prompt = ""
    condition_on_previous_text = True
    fp16 = True
    compression_ratio_threshold = 2.4
    logprob_threshold = -1.0
    no_speech_threshold = 0.6

    verbose_lut = {
        'Live transcription': True,
        'Progress bar': False,
        'None': None
    }

    args = dict(
        language=(None if language == "Auto detection" else language),
        verbose=verbose_lut[verbose],
        task=task,
        temperature=temperature,
        temperature_increment_on_fallback=temperature_increment_on_fallback,
        best_of=best_of,
        beam_size=beam_size,
        patience=patience,
        length_penalty=(length_penalty if length_penalty >= 0.0 else None),
        suppress_tokens=suppress_tokens,
        initial_prompt=(None if not initial_prompt else initial_prompt),
        condition_on_previous_text=condition_on_previous_text,
        fp16=fp16,
        compression_ratio_threshold=compression_ratio_threshold,
        logprob_threshold=logprob_threshold,
        no_speech_threshold=no_speech_threshold
    )

    if temperature_increment_on_fallback is not None:
        temperature = tuple(np.arange(temperature, 1.0 + 1e-6, temperature_increment_on_fallback))
    else:
        temperature = [temperature]

    if model.endswith(".en") and args["language"] not in {"en", "English"}:
        warnings.warn(f"{model} is an English-only model but receipted '{args['language']}'; using English instead.")
        args["language"] = "en"

    audio_path_local = Path(filepath).resolve()
    print("audio local path:", audio_path_local)

    args.pop('temperature_increment_on_fallback', None)
    transcription = whisper.transcribe(
        whisper_model,
        str(audio_path_local),
        **args,
    )
    if not os.path.exists("Texts"):
        os.makedirs("Texts")
    # Save output as a text file
    with open(os.path.join("Texts", f"{title}.txt"), "w",encoding='utf-8') as f:
        f.write(transcription["text"])

    print(f"Transcript file created: {title}.txt")
