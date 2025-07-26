import SwiftUI

struct ContentView: View {
    @State private var isDropping = false
    @State private var outputMessage = "Drag and drop an app file"
    
    var body: some View {
        VStack {
            Text("App2DMG Converter")
                .font(.largeTitle)
                .padding()
            
            Text(outputMessage)
                .foregroundColor(.gray)
                .padding()
            
            Rectangle()
                .fill(isDropping ? Color.blue.opacity(0.2) : Color.gray.opacity(0.2))
                .frame(height: 200)
                .overlay(
                    Text("Drop your .app file here")
                        .foregroundColor(isDropping ? .blue : .black)
                )
                .onDrop(of: ["public.file-url"], isTargeted: $isDropping) { providers in
                    handleDrop(providers: providers)
                    return true
                }
                .padding()
        }
    }
    
    private func handleDrop(providers: [NSItemProvider]) {
        if let item = providers.first {
            item.loadItem(forTypeIdentifier: "public.file-url", options: nil) { item, error in
                if let data = item as? Data {
                    let url = NSURL(absoluteURLWithDataRepresentation: data, relativeTo: nil) as URL
                    processAppFile(at: url)
                }
            }
        }
    }

    private func processAppFile(at url: URL) {
        let task = Process()
        task.launchPath = "/Users/minguez/Desktop/App2DMG/app2dmg"
        task.arguments = [url.path]

        task.terminationHandler = { _ in
            DispatchQueue.main.async {
                outputMessage = "Conversion complete: \(url.lastPathComponent)"
            }
        }

        do {
            try task.run()
        } catch {
            print("Error: \(error.localizedDescription)")
            DispatchQueue.main.async {
                outputMessage = "Error converting \(url.lastPathComponent)"
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
