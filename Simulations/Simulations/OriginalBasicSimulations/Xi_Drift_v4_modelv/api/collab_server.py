from fastapi import FastAPI
from aiortc import RTCPeerConnection, VideoStreamTrack

app = FastAPI()
pcs = set()

@app.post("/offer")
async def offer(sdp: str):
    pc = RTCPeerConnection()
    pcs.add(pc)
    
    # Send field data over WebRTC data channel
    channel = pc.createDataChannel("xi")
    channel.send(np.load("output/xi_field_log.npy").tobytes())
    
    # Add video stream for 3D rendering
    pc.addTrack(VideoStreamTrack())
    
    await pc.setRemoteDescription(sdp)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return {"sdp": pc.localDescription.sdp}
