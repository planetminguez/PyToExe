import SwiftUI
import UniformTypeIdentifiers
import os.log

struct ContentView: View {
    @State private var isDropping = false
    @State private var outputMessage = "Drag and drop a Python (.py) file"
    @State private var isProcessing = false
    @State private var showingAlert = false
    @State private var alertMessage = ""
    @State private var outputPath = ""
    @State private var progressValue: Double = 0.0
    @State private var progressMessage = ""
    @State private var showCompletion = false
    @State private var completionMessage = ""
    
    // Logger for debugging
    private let logger = OSLog(subsystem: "com.python2exe.Python2Exe", category: "drag-drop")
    
    // Custom colors
    private let primaryRed = Color(red: 0.8, green: 0.1, blue: 0.1)
    private let accentRed = Color(red: 0.9, green: 0.2, blue: 0.2)
    private let softBlack = Color(red: 0.1, green: 0.1, blue: 0.1)
    private let charcoal = Color(red: 0.2, green: 0.2, blue: 0.2)
    
    var body: some View {
        ZStack {
            // Background gradient
            LinearGradient(
                gradient: Gradient(colors: [Color.black, softBlack]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(spacing: 25) {
                // Header section with logo-style design
                VStack(spacing: 12) {
                    HStack {
                        Image(systemName: "terminal.fill")
                            .font(.system(size: 36, weight: .bold))
                            .foregroundColor(primaryRed)
                        
                        VStack(alignment: .leading, spacing: 2) {
                            Text("PYTHON2EXE")
                                .font(.system(size: 28, weight: .black, design: .rounded))
                                .foregroundColor(.white)
                            
                            Text("CONVERTER")
                                .font(.system(size: 16, weight: .medium, design: .rounded))
                                .foregroundColor(primaryRed)
                                .tracking(2)
                        }
                    }
                    .padding(.top, 20)
                    
                    Text("Transform Python scripts into standalone executables")
                        .font(.system(size: 14, weight: .medium))
                        .foregroundColor(.white.opacity(0.8))
                        .multilineTextAlignment(.center)
                        .padding(.horizontal)
                }
                
                // Status message with modern styling
                Text(outputMessage)
                    .font(.system(size: 16, weight: .medium))
                    .foregroundColor(isProcessing ? primaryRed : .white.opacity(0.7))
                    .padding(.horizontal, 20)
                    .padding(.vertical, 8)
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(charcoal.opacity(0.3))
                    )
                
                // Drop zone with premium styling
                RoundedRectangle(cornerRadius: 20)
                    .fill(
                        LinearGradient(
                            gradient: Gradient(colors: [
                                isDropping ? primaryRed.opacity(0.2) : charcoal.opacity(0.3),
                                isDropping ? accentRed.opacity(0.1) : softBlack.opacity(0.5)
                            ]),
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 20)
                            .stroke(
                                LinearGradient(
                                    gradient: Gradient(colors: [
                                        isDropping ? primaryRed : .white.opacity(0.2),
                                        isDropping ? accentRed : .white.opacity(0.1)
                                    ]),
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                ),
                                lineWidth: isDropping ? 3 : 2
                            )
                    )
                    .frame(height: 220)
                    .overlay(
                        VStack(spacing: 15) {
                            ZStack {
                                Circle()
                                    .fill(isDropping ? primaryRed.opacity(0.2) : .white.opacity(0.1))
                                    .frame(width: 80, height: 80)
                                
                                Image(systemName: isDropping ? "arrow.down.circle.fill" : "doc.text.fill")
                                    .font(.system(size: 40, weight: .bold))
                                    .foregroundColor(isDropping ? primaryRed : .white.opacity(0.8))
                            }
                            .scaleEffect(isDropping ? 1.1 : 1.0)
                            .animation(.spring(response: 0.3, dampingFraction: 0.6), value: isDropping)
                            
                            VStack(spacing: 8) {
                                Text(isDropping ? "Release to convert" : "Drop Python Files Here")
                                    .font(.system(size: 18, weight: .bold))
                                    .foregroundColor(isDropping ? primaryRed : .white)
                                
                                Text("Supports .py files • PyInstaller powered")
                                    .font(.system(size: 12, weight: .medium))
                                    .foregroundColor(.white.opacity(0.6))
                            }
                        }
                    )
                    .onDrop(of: [UTType.fileURL], isTargeted: $isDropping) { providers in
                        handleDrop(providers: providers)
                        return true
                    }
                    .padding(.horizontal, 30)
                    .shadow(color: isDropping ? primaryRed.opacity(0.3) : .black.opacity(0.3), radius: 10, x: 0, y: 5)
            
                // Progress section with premium red theme
                if isProcessing {
                    VStack(spacing: 20) {
                        HStack(spacing: 12) {
                            ZStack {
                                Circle()
                                    .fill(primaryRed.opacity(0.2))
                                    .frame(width: 50, height: 50)
                                
                                Image(systemName: "gearshape.2.fill")
                                    .font(.system(size: 24, weight: .bold))
                                    .foregroundColor(primaryRed)
                                    .rotationEffect(.degrees(progressValue * 3.6))
                                    .animation(.linear(duration: 2).repeatForever(autoreverses: false), value: progressValue)
                            }
                            
                            VStack(alignment: .leading, spacing: 4) {
                                Text("CONVERTING")
                                    .font(.system(size: 18, weight: .black, design: .rounded))
                                    .foregroundColor(.white)
                                    .tracking(1)
                                
                                Text("Python → Executable")
                                    .font(.system(size: 14, weight: .medium))
                                    .foregroundColor(primaryRed)
                            }
                            
                            Spacer()
                            
                            Text("\(Int(progressValue))%")
                                .font(.system(size: 20, weight: .black, design: .rounded))
                                .foregroundColor(.white)
                        }
                        .padding(.horizontal, 25)
                        .padding(.vertical, 15)
                        
                        // Custom progress bar
                        VStack(spacing: 10) {
                            ZStack(alignment: .leading) {
                                RoundedRectangle(cornerRadius: 6)
                                    .fill(charcoal.opacity(0.8))
                                    .frame(height: 12)
                                
                                RoundedRectangle(cornerRadius: 6)
                                    .fill(
                                        LinearGradient(
                                            gradient: Gradient(colors: [primaryRed, accentRed]),
                                            startPoint: .leading,
                                            endPoint: .trailing
                                        )
                                    )
                                    .frame(width: CGFloat(progressValue / 100) * 300, height: 12)
                                    .animation(.easeInOut(duration: 0.5), value: progressValue)
                            }
                            .frame(width: 300)
                            
                            Text(progressMessage)
                                .font(.system(size: 14, weight: .medium))
                                .foregroundColor(.white.opacity(0.8))
                                .multilineTextAlignment(.center)
                                .frame(minHeight: 20)
                        }
                    }
                    .padding(25)
                    .background(
                        RoundedRectangle(cornerRadius: 16)
                            .fill(
                                LinearGradient(
                                    gradient: Gradient(colors: [charcoal.opacity(0.8), softBlack.opacity(0.9)]),
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(primaryRed.opacity(0.3), lineWidth: 1)
                    )
                    .padding(.horizontal, 30)
                    .shadow(color: primaryRed.opacity(0.2), radius: 15, x: 0, y: 5)
                }
                
                // Completion section with themed styling
                if showCompletion {
                    VStack(spacing: 20) {
                        ZStack {
                            Circle()
                                .fill(completionMessage.contains("✅") ? Color.green.opacity(0.2) : primaryRed.opacity(0.2))
                                .frame(width: 80, height: 80)
                            
                            Image(systemName: completionMessage.contains("✅") ? "checkmark.circle.fill" : "xmark.circle.fill")
                                .font(.system(size: 48, weight: .bold))
                                .foregroundColor(completionMessage.contains("✅") ? Color.green : primaryRed)
                        }
                        .scaleEffect(1.1)
                        .animation(.spring(response: 0.5, dampingFraction: 0.6), value: showCompletion)
                        
                        VStack(spacing: 8) {
                            Text(completionMessage.contains("✅") ? "SUCCESS" : "ERROR")
                                .font(.system(size: 20, weight: .black, design: .rounded))
                                .foregroundColor(.white)
                                .tracking(2)
                            
                            Text(completionMessage)
                                .font(.system(size: 14, weight: .medium))
                                .foregroundColor(.white.opacity(0.8))
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 20)
                        }
                        
                        if completionMessage.contains("✅") {
                            Button(action: { resetForNewConversion() }) {
                                HStack(spacing: 8) {
                                    Image(systemName: "arrow.clockwise")
                                        .font(.system(size: 16, weight: .bold))
                                    Text("NEW CONVERSION")
                                        .font(.system(size: 14, weight: .bold, design: .rounded))
                                        .tracking(1)
                                }
                                .foregroundColor(.white)
                                .padding(.horizontal, 20)
                                .padding(.vertical, 12)
                                .background(
                                    RoundedRectangle(cornerRadius: 8)
                                        .fill(
                                            LinearGradient(
                                                gradient: Gradient(colors: [primaryRed, accentRed]),
                                                startPoint: .leading,
                                                endPoint: .trailing
                                            )
                                        )
                                )
                            }
                            .buttonStyle(PlainButtonStyle())
                        }
                    }
                    .padding(30)
                    .background(
                        RoundedRectangle(cornerRadius: 16)
                            .fill(
                                LinearGradient(
                                    gradient: Gradient(colors: [charcoal.opacity(0.8), softBlack.opacity(0.9)]),
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(
                                completionMessage.contains("✅") ? Color.green.opacity(0.3) : primaryRed.opacity(0.3),
                                lineWidth: 1
                            )
                    )
                    .padding(.horizontal, 30)
                    .shadow(color: .black.opacity(0.3), radius: 15, x: 0, y: 5)
                }
                
                // Output path section
                if !outputPath.isEmpty {
                    VStack(spacing: 12) {
                        HStack {
                            Text("OUTPUT")
                                .font(.system(size: 16, weight: .black, design: .rounded))
                                .foregroundColor(.white)
                                .tracking(1)
                            
                            Spacer()
                            
                            Button(action: { revealInFinder(path: outputPath) }) {
                                HStack(spacing: 6) {
                                    Image(systemName: "folder.fill")
                                        .font(.system(size: 14, weight: .bold))
                                    Text("REVEAL")
                                        .font(.system(size: 12, weight: .bold, design: .rounded))
                                        .tracking(0.5)
                                }
                                .foregroundColor(.white)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 6)
                                .background(
                                    RoundedRectangle(cornerRadius: 6)
                                        .fill(primaryRed)
                                )
                            }
                            .buttonStyle(PlainButtonStyle())
                        }
                        
                        Text(outputPath)
                            .font(.system(size: 12, weight: .medium, design: .monospaced))
                            .foregroundColor(.white.opacity(0.7))
                            .padding(12)
                            .background(
                                RoundedRectangle(cornerRadius: 8)
                                    .fill(charcoal.opacity(0.6))
                            )
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    .padding(20)
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(softBlack.opacity(0.8))
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(.white.opacity(0.1), lineWidth: 1)
                    )
                    .padding(.horizontal, 30)
                }
                
                Spacer()
                
                // Quit button with themed styling
                Button(action: { NSApplication.shared.terminate(nil) }) {
                    HStack(spacing: 8) {
                        Image(systemName: "power")
                            .font(.system(size: 16, weight: .bold))
                        Text("QUIT")
                            .font(.system(size: 16, weight: .black, design: .rounded))
                            .tracking(1)
                    }
                    .foregroundColor(.white)
                    .padding(.horizontal, 30)
                    .padding(.vertical, 12)
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(
                                LinearGradient(
                                    gradient: Gradient(colors: [charcoal, softBlack]),
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(.white.opacity(0.2), lineWidth: 1)
                    )
                }
                .buttonStyle(PlainButtonStyle())
                .padding(.bottom, 15)
                
                // Designer credit and donation section
                VStack(spacing: 12) {
                    // Designer credit with stylish presentation
                    HStack(spacing: 8) {
                        Image(systemName: "sparkles")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(primaryRed)
                        
                        Text("Designed by")
                            .font(.system(size: 12, weight: .medium, design: .rounded))
                            .foregroundColor(.white.opacity(0.7))
                        
                        Text("@planetminguez")
                            .font(.system(size: 14, weight: .black, design: .rounded))
                            .foregroundColor(primaryRed)
                            .tracking(0.5)
                        
                        Image(systemName: "sparkles")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(primaryRed)
                    }
                    .padding(.horizontal, 16)
                    .padding(.vertical, 8)
                    .background(
                        RoundedRectangle(cornerRadius: 20)
                            .fill(
                                LinearGradient(
                                    gradient: Gradient(colors: [charcoal.opacity(0.6), softBlack.opacity(0.8)]),
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 20)
                            .stroke(
                                LinearGradient(
                                    gradient: Gradient(colors: [primaryRed.opacity(0.3), .white.opacity(0.1)]),
                                    startPoint: .leading,
                                    endPoint: .trailing
                                ),
                                lineWidth: 1
                            )
                    )
                    
                    // Donation call-to-action with attractive styling
                    VStack(spacing: 6) {
                        HStack(spacing: 6) {
                            Image(systemName: "heart.fill")
                                .font(.system(size: 12, weight: .bold))
                                .foregroundColor(primaryRed)
                            
                            Text("Support the developer")
                                .font(.system(size: 11, weight: .semibold, design: .rounded))
                                .foregroundColor(.white.opacity(0.8))
                            
                            Image(systemName: "heart.fill")
                                .font(.system(size: 12, weight: .bold))
                                .foregroundColor(primaryRed)
                        }
                        
                        Text("Donate anything you can to")
                            .font(.system(size: 10, weight: .medium, design: .rounded))
                            .foregroundColor(.white.opacity(0.6))
                        
                        // Payment options with attractive styling
                        HStack(spacing: 12) {
                            // Cash App option - clickable
                            Button(action: { openCashApp() }) {
                                VStack(spacing: 4) {
                                    HStack(spacing: 2) {
                                        Image(systemName: "dollarsign.circle.fill")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(Color.green)
                                        
                                        Text("$planetminguez")
                                            .font(.system(size: 11, weight: .black, design: .rounded))
                                            .foregroundColor(Color.green)
                                            .tracking(0.3)
                                    }
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(
                                        RoundedRectangle(cornerRadius: 8)
                                            .fill(Color.green.opacity(0.15))
                                    )
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 8)
                                            .stroke(Color.green.opacity(0.4), lineWidth: 1)
                                    )
                                    
                                    Text("Cash App")
                                        .font(.system(size: 8, weight: .medium, design: .rounded))
                                        .foregroundColor(.white.opacity(0.5))
                                        .tracking(0.5)
                                }
                            }
                            .buttonStyle(PlainButtonStyle())
                            .scaleEffect(1.0)
                            .onHover { isHovered in
                                // Add subtle hover effect
                            }
                            
                            // Venmo option - clickable
                            Button(action: { openVenmo() }) {
                                VStack(spacing: 4) {
                                    HStack(spacing: 2) {
                                        Image(systemName: "creditcard.circle.fill")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(Color.blue)
                                        
                                        Text("@planetminguez")
                                            .font(.system(size: 11, weight: .black, design: .rounded))
                                            .foregroundColor(Color.blue)
                                            .tracking(0.3)
                                    }
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(
                                        RoundedRectangle(cornerRadius: 8)
                                            .fill(Color.blue.opacity(0.15))
                                    )
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 8)
                                            .stroke(Color.blue.opacity(0.4), lineWidth: 1)
                                    )
                                    
                                    Text("Venmo")
                                        .font(.system(size: 8, weight: .medium, design: .rounded))
                                        .foregroundColor(.white.opacity(0.5))
                                        .tracking(0.5)
                                }
                            }
                            .buttonStyle(PlainButtonStyle())
                            .scaleEffect(1.0)
                            .onHover { isHovered in
                                // Add subtle hover effect
                            }
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.vertical, 10)
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(
                                LinearGradient(
                                    gradient: Gradient(colors: [softBlack.opacity(0.4), charcoal.opacity(0.2)]),
                                    startPoint: .top,
                                    endPoint: .bottom
                                )
                            )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(.white.opacity(0.1), lineWidth: 1)
                    )
                    
                    // Footer with subtle styling
                    Text("POWERED BY PYINSTALLER")
                        .font(.system(size: 8, weight: .medium, design: .rounded))
                        .foregroundColor(.white.opacity(0.3))
                        .tracking(1)
                        .padding(.top, 4)
                }
                .padding(.bottom, 20)
            }
        }
        .frame(minWidth: 600, minHeight: 700)
        .alert("Error", isPresented: $showingAlert) {
            Button("OK") { }
        } message: {
            Text(alertMessage)
        }
    }
    
    private func handleDrop(providers: [NSItemProvider]) {
        // Add immediate logging
        print("[DEBUG] handleDrop called!")
        os_log("handleDrop function called with %d providers", log: logger, type: .info, providers.count)
        
        guard let provider = providers.first else { 
            print("[ERROR] No providers in drop")
            os_log("No providers in drop", log: logger, type: .error)
            return 
        }
        
        print("[DEBUG] Provider type identifiers: \(provider.registeredTypeIdentifiers)")
        os_log("DEBUG: handleDrop called with %d providers", log: logger, type: .debug, providers.count)
        
        // Debug: Print available type identifiers
        os_log("Available type identifiers: %@", log: logger, type: .debug, provider.registeredTypeIdentifiers.joined(separator: ", "))
        
        // Try the most common type identifiers in order of preference
        let typeIdentifiers = [
            "public.file-url",
            "public.url", 
            "com.apple.finder.node",
            "public.data"
        ]
        
        func tryLoadWithTypeIdentifier(_ typeId: String) {
            if provider.hasItemConformingToTypeIdentifier(typeId) {
                provider.loadItem(forTypeIdentifier: typeId, options: nil) { item, error in
                    DispatchQueue.main.async {
                        if let error = error {
                            os_log("Error loading %@: %@", log: self.logger, type: .error, typeId, error.localizedDescription)
                            return
                        }
                        
                        var url: URL?
                        
                        // Handle different data types
                        if let data = item as? Data {
                            url = URL(dataRepresentation: data, relativeTo: nil)
                        } else if let urlItem = item as? URL {
                            url = urlItem
                        } else if let string = item as? String {
                            url = URL(string: string)
                        }
                        
                        guard let fileURL = url else {
                            os_log("Could not create URL from item type: %@", log: self.logger, type: .error, String(describing: type(of: item)))
                            if typeId != typeIdentifiers.last {
                                // Try next type identifier
                                if let nextIndex = typeIdentifiers.firstIndex(of: typeId),
                                   nextIndex + 1 < typeIdentifiers.count {
                                    tryLoadWithTypeIdentifier(typeIdentifiers[nextIndex + 1])
                                }
                            } else {
                                self.showError("Could not process the dropped file")
                            }
                            return
                        }
                        
                        // Check if it's a Python file
                        guard fileURL.pathExtension.lowercased() == "py" else {
                            self.showError("Please select a Python (.py) file")
                            return
                        }
                        
                        os_log("Successfully loaded file: %@", log: self.logger, type: .info, fileURL.path)
                        self.convertPythonFile(at: fileURL)
                    }
                }
                return
            }
        }
        
        // Try each type identifier
        tryLoadWithTypeIdentifier(typeIdentifiers[0])
    }
    
    private func convertPythonFile(at url: URL) {
        isProcessing = true
        showCompletion = false
        outputMessage = "Converting \(url.lastPathComponent)..."
        outputPath = ""
        progressValue = 10.0
        progressMessage = "Initializing conversion process..."
        
        // Debug: Print file path
        os_log("Converting file: %@", log: logger, type: .info, url.path)
        
        // Start progress simulation after a small delay
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            self.simulateProgress()
        }
        
        let task = Process()
        let pipe = Pipe()
        
        // Get desktop path
        let desktopPath = FileManager.default.urls(for: .desktopDirectory, in: .userDomainMask).first!.path
        os_log("Desktop path: %@", log: logger, type: .debug, desktopPath)
        
        task.standardOutput = pipe
        task.standardError = pipe
        
        // Try different Python paths in order of preference
        let pythonPaths = [
            "/usr/local/bin/python3",
            "/opt/homebrew/bin/python3",
            "/usr/bin/python3",
            "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3",
            "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3",
            "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3"
        ]
        
        var pythonPath: String?
        for path in pythonPaths {
            if FileManager.default.fileExists(atPath: path) {
                pythonPath = path
                break
            }
        }
        
        guard let validPythonPath = pythonPath else {
            DispatchQueue.main.async {
                self.isProcessing = false
                self.showCompletion = true
                self.showError("Python3 not found. Please install Python 3.")
                self.outputMessage = "❌ Python not found"
                self.completionMessage = "❌ Python Not Found\n\nPython 3 is required but not found in standard locations."
            }
            return
        }
        
        task.launchPath = validPythonPath
        task.arguments = ["-m", "PyInstaller", "--onefile", "--distpath", desktopPath, "--clean", "--noconfirm", url.path]
        task.currentDirectoryPath = url.deletingLastPathComponent().path
        
        // Set environment variables for better PyInstaller compatibility
        var environment = ProcessInfo.processInfo.environment
        environment["PATH"] = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin"
        environment["PYTHONPATH"] = ""
        task.environment = environment
        
        os_log("PyInstaller command: %@", log: logger, type: .debug, task.arguments?.joined(separator: " ") ?? "unknown")
        os_log("Working directory: %@", log: logger, type: .debug, task.currentDirectoryPath ?? "unknown")
        
        task.terminationHandler = { process in
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            let output = String(data: data, encoding: .utf8) ?? "Unknown error"
            
            DispatchQueue.main.async {
                // Ensure progress reaches 100% before showing completion
                self.progressValue = 100.0
                self.progressMessage = "Finishing conversion..."
                
                // Log the full output for debugging
                os_log("PyInstaller full output: %@", log: self.logger, type: .info, output)
                os_log("PyInstaller termination status: %d", log: self.logger, type: .info, process.terminationStatus)
                
                // Wait a moment before hiding progress and showing completion
                DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
                    self.isProcessing = false
                    self.showCompletion = true
                    
                    if process.terminationStatus == 0 {
                        // Success - find the generated executable on desktop
                        let executableName = url.deletingPathExtension().lastPathComponent
                        let executablePath = URL(fileURLWithPath: desktopPath).appendingPathComponent(executableName).path
                        
                        os_log("Looking for executable at: %@", log: self.logger, type: .info, executablePath)
                        
                        if FileManager.default.fileExists(atPath: executablePath) {
                            self.outputPath = executablePath
                            self.outputMessage = "✅ Successfully converted to executable on Desktop!"
                            self.completionMessage = "✅ Conversion Successful!\n\nYour Python script has been converted to a standalone executable and saved on your Desktop."
                        } else {
                            self.outputMessage = "⚠️ Conversion completed but executable not found on Desktop"
                            self.completionMessage = "⚠️ Conversion Completed\n\nPyInstaller finished successfully, but the executable could not be found on the Desktop."
                        }
                    } else {
                        // Error - log full output
                        os_log("PyInstaller error output: %@", log: self.logger, type: .error, output)
                        
                        // Check for specific errors
                        if output.contains("No module named 'PyInstaller'") {
                            self.showError("PyInstaller is not installed. Please install it using: pip install pyinstaller")
                            self.completionMessage = "❌ PyInstaller Not Found\n\nPlease install PyInstaller using: pip install pyinstaller"
                        } else if output.contains("Permission denied") {
                            self.showError("Permission denied. The app may not have permission to run PyInstaller.")
                            self.completionMessage = "❌ Permission Denied\n\nThe app doesn't have permission to run the conversion process."
                        } else if output.contains("command not found") {
                            self.showError("Python or PyInstaller not found in PATH")
                            self.completionMessage = "❌ Command Not Found\n\nPython or PyInstaller could not be found. Please ensure they are installed."
                        } else {
                            // Show a truncated version of the error in the dialog
                            let truncatedOutput = String(output.prefix(500))
                            self.showError("Conversion failed: \(truncatedOutput)")
                            self.completionMessage = "❌ Conversion Failed\n\nThe conversion process encountered an error. Check the Console app for detailed logs."
                        }
                        self.outputMessage = "❌ Conversion failed"
                    }
                }
            }
        }
        
        do {
            try task.run()
            os_log("PyInstaller task started successfully", log: logger, type: .info)
        } catch {
            DispatchQueue.main.async {
                self.isProcessing = false
                self.showCompletion = true
                self.showError("Failed to start conversion: \(error.localizedDescription)")
                self.outputMessage = "❌ Failed to start conversion"
                self.completionMessage = "❌ Failed to Start\n\nCould not start the conversion process. Error: \(error.localizedDescription)"
            }
            os_log("Failed to start PyInstaller task: %@", log: logger, type: .error, error.localizedDescription)
        }
    }
    
    private func showError(_ message: String) {
        alertMessage = message
        showingAlert = true
    }
    
    private func revealInFinder(path: String) {
        NSWorkspace.shared.selectFile(path, inFileViewerRootedAtPath: "")
    }
    
    private func simulateProgress() {
        let progressSteps = [
            (10.0, "Checking Python environment..."),
            (20.0, "Analyzing script dependencies..."),
            (35.0, "Setting up PyInstaller configuration..."),
            (50.0, "Collecting Python modules..."),
            (65.0, "Building executable structure..."),
            (80.0, "Optimizing executable size..."),
            (95.0, "Finalizing executable..."),
            (100.0, "Conversion complete!")
        ]
        
        var currentStep = 0
        
        func updateProgress() {
            guard currentStep < progressSteps.count else { return }
            
            let (progress, message) = progressSteps[currentStep]
            
            DispatchQueue.main.async {
                self.progressValue = progress
                self.progressMessage = message
            }
            
            currentStep += 1
            
            if currentStep < progressSteps.count {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) {
                    updateProgress()
                }
            }
        }
        
        updateProgress()
    }
    
    private func resetForNewConversion() {
        showCompletion = false
        outputPath = ""
        progressValue = 0.0
        progressMessage = ""
        completionMessage = ""
        outputMessage = "Drag and drop a Python (.py) file"
    }
    
    private func openCashApp() {
        // Open Cash App web URL directly - most reliable approach
        let cashAppURL = "https://cash.app/$planetminguez"
        
        if let url = URL(string: cashAppURL) {
            print("[DEBUG] Opening Cash App URL: \(cashAppURL)")
            NSWorkspace.shared.open(url)
        } else {
            print("[ERROR] Could not create Cash App URL")
        }
    }
    
    private func openVenmo() {
        // Open Venmo web URL directly - most reliable approach
        let venmoWebURL = "https://venmo.com/u/planetminguez"
        
        if let url = URL(string: venmoWebURL) {
            print("[DEBUG] Opening Venmo URL: \(venmoWebURL)")
            NSWorkspace.shared.open(url)
        } else {
            print("[ERROR] Could not create Venmo URL")
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
