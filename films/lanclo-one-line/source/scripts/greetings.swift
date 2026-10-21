// Render the 17 study languages' greetings to assets/greet/<code>.png with CoreText (PIL here has no
// complex-script shaping). Zen Maru Gothic first; CoreText falls back per script (Hangul, Thai, Devanagari...).
// usage: swift scripts/greetings.swift
import AppKit
import CoreText

let root = URL(fileURLWithPath: CommandLine.arguments[0]).deletingLastPathComponent().deletingLastPathComponent()
let assets = root.appendingPathComponent("assets")
let out = assets.appendingPathComponent("greet")
try? FileManager.default.createDirectory(at: out, withIntermediateDirectories: true)
CTFontManagerRegisterFontsForURL(assets.appendingPathComponent("fonts/ZenMaruGothic-Bold.ttf") as CFURL, .process, nil)

// Same order and codes as packages/core/src/studyLanguages.ts
let greetings: [(String, String)] = [
    ("en", "Hello"), ("ja", "こんにちは"), ("zh", "你好"), ("ko", "안녕하세요"), ("fr", "Bonjour"),
    ("es", "¡Hola!"), ("th", "สวัสดี"), ("yue", "哈囉"), ("de", "Hallo"), ("it", "Ciao"),
    ("pt-BR", "Olá"), ("id", "Halo"), ("vi", "Xin chào"), ("hi", "नमस्ते"), ("bn", "নমস্কার"),
    ("ru", "Привет"), ("tr", "Merhaba"),
]
let size: CGFloat = 160
let font = CTFontCreateWithName("ZenMaruGothic-Bold" as CFString, size, nil)
let ink = CGColor(red: 0x27 / 255.0, green: 0x3b / 255.0, blue: 0x4b / 255.0, alpha: 1)

for (code, s) in greetings {
    let attr = NSAttributedString(string: s, attributes: [
        NSAttributedString.Key(kCTFontAttributeName as String): font,
        NSAttributedString.Key(kCTForegroundColorAttributeName as String): ink,
    ])
    let line = CTLineCreateWithAttributedString(attr)
    let b = CTLineGetBoundsWithOptions(line, [.useGlyphPathBounds])
    let pad: CGFloat = 24
    // fixed line box (so every greeting shares one baseline), width from the glyphs
    let w = Int(ceil(b.width + 2 * pad)), h = Int(size * 1.6)
    let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
                        space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.setShouldSmoothFonts(false)
    ctx.textPosition = CGPoint(x: pad - b.minX, y: size * 0.5)
    CTLineDraw(line, ctx)
    let rep = NSBitmapImageRep(cgImage: ctx.makeImage()!)
    try! rep.representation(using: .png, properties: [:])!.write(to: out.appendingPathComponent("\(code).png"))
}
print("wrote \(greetings.count) greetings to \(out.path)")
