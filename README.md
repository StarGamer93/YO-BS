YO-BS: Lightweight Live Optimizer for OBS Studio.
YO-BS is a Python script for OBS Studio designed to enhance live streaming and recording performance. It intelligently optimizes sources, reduces unnecessary processing, and provides detailed logging to help track any issues—all while remaining fully configurable.

Features
Automatic Source Optimization: Optimizes all sources in your scenes automatically.

Defer Hidden Sources: Reduces GPU load by rendering only visible sources.

Audio Dynamics Management: Disables audio dynamics on input sources to save CPU resources.

Filter Optimization: Disables unused filters for better overall performance.

Auto-Mute Inactive Sources: Mutes inactive audio sources to reduce processing overhead.

Scene Transition Optimization: Speeds up scene switching by optimizing transitions.

Reduced Video Buffering: Lowers CPU/GPU usage by reducing unnecessary buffering.

Browser Source Handling: Optionally skip heavy browser sources for stability.

Detailed Logging: Provides verbose logs for identifying issues or performance bottlenecks.

Configurable Settings: Control all optimizations through the OBS script interface.

Optional Auto Recording: Start recording automatically if desired.

Default Settings
Setting	Default
Start recording automatically	❌ Off
Defer hidden sources	✅ On
Disable audio dynamics	✅ On
Disable unused filters	✅ On
Auto-mute inactive sources	✅ On
Mute inactive audio sources	✅ On
Minimal logging	❌ Off
Disable unused plugins	❌ Off
Lower video buffering	✅ On
Skip browser sources	❌ Off
Optimize scene transitions	✅ On

Export to Sheets
How YO-BS Improves Performance
YO-BS reduces the CPU and GPU load in several ways:

Skipping Inactive or Hidden Sources: Only visible sources are rendered, preventing unnecessary GPU usage.

Disabling Unused Filters and Dynamics: Many filters and audio processing features can be resource-intensive. Disabling unused features frees CPU cycles.

Optimizing Scene Transitions: Faster scene switching reduces frame drops and delays.

Auto-Muting Inactive Audio: Avoids processing audio from sources that are not currently active.

Lower Video Buffering: Reduces memory and CPU overhead for smoother streaming and recording.

Error-Resilient and Lightweight: Handles exceptions gracefully, ensuring optimizations continue without impacting OBS stability.

These combined strategies result in smoother streaming, faster scene switching, and lower system resource usage.

Installation
Download YO-BS.py.

Open OBS Studio → Tools → Scripts.

Click + and select YO-BS.py.

Configure settings in the script properties as needed.

Usage
YO-BS automatically optimizes sources whenever scenes or scene collections change.

Verbose logs show optimization progress and any issues for debugging.

Enable Start recording automatically if you want the script to begin recording on load.

Logging
Each optimized source is logged, including any errors encountered.

Helps quickly identify which source or setting might be causing performance issues.

Logs are visible in OBS’s log window.

Contributing
Contributions are welcome! Fork the repository, improve optimizations, or add new features. Report issues or performance problems via the repository’s issue tracker.

License
MIT License. Free to use, modify, and distribute.

Notes
Recommended for OBS Studio 28+ with Python 3.9+.

Designed to maximize performance while maintaining stability.

Heavy sources (e.g., 4K browser sources) can optionally be skipped to prevent lag.
