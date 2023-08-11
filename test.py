from pytube import YouTube

# YouTube video URL
url = "https://www.youtube.com/watch?v=YDyBL3bXOwA"

# Create a YouTube object
yt = YouTube(url)

# Get the best available video stream
stream = yt.streams.get_highest_resolution()

# Print the video title
print("Video Title:", yt.title)

# Start streaming the video
stream.stream_to_buffer()
buffer = stream.stream_buffer

# Stream the video in chunks
while True:
    chunk = buffer.read(1024)
    if not chunk:
        break
    # Process the video chunk as needed (e.g., write to a file, display in a player, etc.)
    # Example: print(chunk)

# Cleanup
buffer.close()