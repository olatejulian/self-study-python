from pytube import YouTube


class StreamsFilterError(Exception):
    pass


def youtube_download(
    url: str,
    output_path: str,
    only_audio: bool,
    filename: str | None = None,
    **kwargs,
) -> str:
    yt = YouTube(url, **kwargs)

    if streams := yt.streams.filter(only_audio=only_audio):
        if get_first_stream := streams.first():
            downloaded_file_path = get_first_stream.download(
                output_path=output_path, filename=filename
            )

        else:
            raise StreamsFilterError()

    else:
        raise StreamsFilterError()

    return downloaded_file_path
