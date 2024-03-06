import os
import argparse
from pytube import YouTube

def download_video(url, video_format, output_path=None):
    try:
        y = YouTube(url)
        if video_format == "mp4":
            stream = y.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        else:
            stream = y.streams.filter(file_extension=video_format).order_by("resolution").desc().first()

        if stream:
            if output_path is None:
                output_path = os.getcwd()
            stream.download(output_path=output_path)
            print(f"[+] Downloaded successfully: {y.title}.{stream.subtype} [+]")
        else:
            print("[!] No stream found for the specified format. [!]")
    except KeyError:
        print(f"[!] No video found at URL: {url} [!]")
    except Exception as e:
        print(f"[!] Error occurred: {e} [!]")

def download_videos_from_list(file_path, video_format, output_path=None):
    try:
        with open(file_path, "r") as file:
            urls = file.readlines()

        for url in urls:
            url = url.strip()
            print(f"\n[+] Downloading: {url} [+]")
            download_video(url, video_format=video_format, output_path=output_path)

        print("\n[+] All videos downloaded successfully. [+]")
    except Exception as e:
        print(f"\n[!] Error occurred: {e} [!]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos.")
    parser.add_argument("-fl", "--file", type=str, help="Path to the file containing list of YouTube video URLs")
    parser.add_argument("-f", "--format", type=str, default="mp4", help="Desired video format (e.g., mp4, webm)")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output directory")
    args = parser.parse_args()

    if args.file:
        download_videos_from_list(args.file, video_format=args.format, output_path=args.output)
    else:
        parser.print_help()
