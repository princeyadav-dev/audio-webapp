from pydub import AudioSegment, silence, effects

def full_audio_edit(input_file, output_file, silence_thresh=-40, min_silence_len=500):
    # Step 1: Load audio
    audio = AudioSegment.from_file(input_file)

    # Step 2: Remove silence
    chunks = silence.split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    audio = AudioSegment.empty()
    for chunk in chunks:
        audio += chunk + AudioSegment.silent(duration=150)

    # Step 3: Normalize
    audio = effects.normalize(audio)

    # Step 4: Speed increase 2%
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 1.02)
    }).set_frame_rate(audio.frame_rate)

    # Step 5: Light noise reduction (simulated)
    audio = audio.low_pass_filter(20000).high_pass_filter(100)

    # Step 6: Amplify +5 dB
    audio += 5

    # Step 7: Convert to 16kHz mono
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)

    # Step 8: Final normalize
    audio = effects.normalize(audio)

    # Step 9: Export
    audio.export(output_file, format="mp3")

    return output_file
