// Record the screen of an iPhone connected to this Mac by USB (the same source QuickTime's "New Movie Recording" uses).
// usage: swift kits/mimi-short/app-capture/record-iphone.swift <out.mov> [seconds=15]
// The iPhone must be unlocked and trust this Mac. Screen devices only appear after CoreMediaIO is told to allow them.
import AVFoundation
import CoreMediaIO

let args = CommandLine.arguments
guard args.count >= 2 else { print("usage: record-iphone.swift <out.mov> [seconds]"); exit(2) }
let out = URL(fileURLWithPath: args[1]); let seconds = args.count > 2 ? Double(args[2]) ?? 15 : 15

var prop = CMIOObjectPropertyAddress(mSelector: CMIOObjectPropertySelector(kCMIOHardwarePropertyAllowScreenCaptureDevices),
                                     mScope: CMIOObjectPropertyScope(kCMIOObjectPropertyScopeGlobal),
                                     mElement: CMIOObjectPropertyElement(kCMIOObjectPropertyElementMain))
var allow: UInt32 = 1
CMIOObjectSetPropertyData(CMIOObjectID(kCMIOObjectSystemObject), &prop, 0, nil, UInt32(MemoryLayout<UInt32>.size), &allow)

// Capture needs camera permission for this process; asking also wakes device discovery.
let asked = DispatchSemaphore(value: 0)
AVCaptureDevice.requestAccess(for: .video) { _ in asked.signal() }
_ = asked.wait(timeout: .now() + 30)

func findPhone() -> AVCaptureDevice? {
    AVCaptureDevice.DiscoverySession(deviceTypes: [.external], mediaType: nil, position: .unspecified).devices
        .first { $0.hasMediaType(.muxed) && ($0.modelID == "iOS Device" || $0.modelID.contains("iPhone")) }
}
var device: AVCaptureDevice?
for _ in 0..<80 { device = findPhone(); if device != nil { break }; RunLoop.current.run(until: Date().addingTimeInterval(0.25)) }
guard let phone = device else { print("no iPhone screen found: connect by USB, unlock, trust this Mac"); exit(1) }
print("recording \(phone.localizedName) for \(seconds) s -> \(out.path)")

// AVCaptureMovieFileOutput refuses the iPhone's muxed source ("Cannot Record"), so take frames and write them ourselves.
final class Writer: NSObject, AVCaptureVideoDataOutputSampleBufferDelegate {
    let writer: AVAssetWriter; var input: AVAssetWriterInput?; var started = false; var frames = 0
    init(url: URL) throws { writer = try AVAssetWriter(outputURL: url, fileType: .mov) }
    func captureOutput(_ output: AVCaptureOutput, didOutput buffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        if input == nil, let fmt = CMSampleBufferGetFormatDescription(buffer) {
            let d = CMVideoFormatDescriptionGetDimensions(fmt)
            let i = AVAssetWriterInput(mediaType: .video, outputSettings: [AVVideoCodecKey: AVVideoCodecType.h264,
                AVVideoWidthKey: Int(d.width), AVVideoHeightKey: Int(d.height),
                AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 20_000_000]])
            i.expectsMediaDataInRealTime = true
            writer.add(i); input = i
        }
        guard let input else { return }
        if !started { writer.startWriting(); writer.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(buffer)); started = true }
        if input.isReadyForMoreMediaData { input.append(buffer); frames += 1 }
    }
}
try? FileManager.default.removeItem(at: out)
let session = AVCaptureSession()
session.addInput(try AVCaptureDeviceInput(device: phone))
let video = AVCaptureVideoDataOutput()
video.videoSettings = [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA]
let w = try Writer(url: out)
let queue = DispatchQueue(label: "frames")
video.setSampleBufferDelegate(w, queue: queue)
session.addOutput(video)
session.startRunning()
RunLoop.current.run(until: Date().addingTimeInterval(seconds))
session.stopRunning()
queue.sync {}
let done = DispatchSemaphore(value: 0)
w.input?.markAsFinished()
w.writer.finishWriting { done.signal() }
done.wait()
print("saved \(out.path) (\(w.frames) frames, \(w.writer.status == .completed ? "ok" : "failed: \(String(describing: w.writer.error))"))")
