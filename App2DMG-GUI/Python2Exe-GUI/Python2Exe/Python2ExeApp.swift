import SwiftUI

@main
struct Python2ExeApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            CommandGroup(after: .appInfo) {
                Button("About Python2Exe") {
                    NSApplication.shared.orderFrontStandardAboutPanel(nil)
                }
                .keyboardShortcut("a", modifiers: [.command])
            }
        }
    }
}
