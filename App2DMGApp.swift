import SwiftUI

@main
struct App2DMGApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)
        .commands {
            CommandGroup(after: .appInfo) {
                Button("About App2DMG") {
                    NSApplication.shared.orderFrontStandardAboutPanel(nil)
                }
                .keyboardShortcut("a", modifiers: [.command])
            }
        }
    }
}
