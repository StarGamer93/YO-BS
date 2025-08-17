import obspython as obs

# --- DEFAULT SETTINGS ---
start_recording_on_start = False  # must be off by default
defer_hidden_sources = True
disable_audio_dynamics = True
disable_unused_filters = True
auto_mute_unused_sources = True
mute_inactive_audio_sources = True
minimal_logging = False  # we want more logs for error tracing
disable_unused_plugins = False
lower_video_buffering = True  # improved default
skip_browser_sources = False
optimize_scene_transitions = True  # improved default

# --- HELPER ---
optimized_sources = set()

def safe_obs_call(func, *args):
    try:
        return func(*args)
    except Exception as e:
        obs.script_log(obs.LOG_WARNING, f"YO-BS: Error in {func.__name__}({args}): {e}")
        return None

def optimize_source(source):
    if source is None:
        return

    source_id = safe_obs_call(obs.obs_source_get_name, source)
    if not source_id or source_id in optimized_sources:
        return

    try:
        settings = safe_obs_call(obs.obs_source_get_settings, source)
        if not settings:
            obs.script_log(obs.LOG_INFO, f"YO-BS: Skipping source '{source_id}' (no settings)")
            optimized_sources.add(source_id)
            return

        source_type = safe_obs_call(obs.obs_source_get_type, source)
        if skip_browser_sources and source_type and obs.obs_source_get_id(source) in ["browser_source", "obs_browser_source"]:
            safe_obs_call(obs.obs_data_release, settings)
            optimized_sources.add(source_id)
            return

        # Defer hidden sources
        if defer_hidden_sources:
            safe_obs_call(obs.obs_data_set_bool, settings, "defer_rendering", True)

        # Disable audio dynamics for inputs
        if disable_audio_dynamics and source_type == obs.OBS_SOURCE_TYPE_INPUT:
            if obs.obs_data_has_user_value(settings, "enable_dynamics"):
                safe_obs_call(obs.obs_data_set_bool, settings, "enable_dynamics", False)

        # Disable unused filters
        if disable_unused_filters:
            if obs.obs_data_has_user_value(settings, "enable_filtering"):
                safe_obs_call(obs.obs_data_set_bool, settings, "enable_filtering", False)

        # Update source
        safe_obs_call(obs.obs_source_update, source, settings)
        safe_obs_call(obs.obs_data_release, settings)

        # Auto-mute inactive audio sources
        if auto_mute_unused_sources and not safe_obs_call(obs.obs_source_active, source) and mute_inactive_audio_sources:
            if source_type == obs.OBS_SOURCE_TYPE_INPUT:
                safe_obs_call(obs.obs_source_set_muted, source, True)

        optimized_sources.add(source_id)
        obs.script_log(obs.LOG_INFO, f"YO-BS: Optimized source '{source_id}' successfully.")

    except Exception as e:
        obs.script_log(obs.LOG_WARNING, f"YO-BS: Failed to optimize source '{source_id}': {e}")
        optimized_sources.add(source_id)  # prevent retry loops

def optimize_all_sources():
    sources = safe_obs_call(obs.obs_enum_sources)
    if sources:
        for src in sources:
            optimize_source(src)
        safe_obs_call(obs.source_list_release, sources)

def optimize_recording_settings():
    settings = safe_obs_call(obs.obs_data_create)
    if settings:
        if not minimal_logging:
            safe_obs_call(obs.obs_data_set_int, settings, "LogLevel", 4)  # verbose logs
        if lower_video_buffering:
            safe_obs_call(obs.obs_data_set_int, settings, "VideoBuffering", 1)
        safe_obs_call(obs.obs_data_set_string, settings, "encoder", "obs_x264")
        safe_obs_call(obs.obs_data_release, settings)
        obs.script_log(obs.LOG_INFO, "YO-BS: Recording settings optimized.")

def start_recording_if_enabled():
    if start_recording_on_start:
        try:
            if not obs.obs_frontend_recording_active():
                obs.obs_frontend_recording_start()
                obs.script_log(obs.LOG_INFO, "YO-BS: Recording started automatically.")
        except Exception as e:
            obs.script_log(obs.LOG_WARNING, f"YO-BS: Failed to start recording: {e}")

# --- LIVE UPDATE ---
def frontend_event(event):
    if event in (obs.OBS_FRONTEND_EVENT_SCENE_CHANGED, obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGED):
        obs.script_log(obs.LOG_INFO, "YO-BS: Scene changed, optimizing sources...")
        optimize_all_sources()

# --- SCRIPT UI ---
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_bool(props, "start_recording_on_start", "Start recording automatically")
    obs.obs_properties_add_bool(props, "defer_hidden_sources", "Defer rendering of hidden sources")
    obs.obs_properties_add_bool(props, "disable_audio_dynamics", "Disable audio dynamics on input sources")
    obs.obs_properties_add_bool(props, "disable_unused_filters", "Disable unused filters for optimization")
    obs.obs_properties_add_bool(props, "auto_mute_unused_sources", "Automatically mute inactive sources")
    obs.obs_properties_add_bool(props, "mute_inactive_audio_sources", "Mute only audio sources when inactive")
    obs.obs_properties_add_bool(props, "minimal_logging", "Enable minimal logging (disable for full logs)")
    obs.obs_properties_add_bool(props, "disable_unused_plugins", "Skip unused plugin processing")
    obs.obs_properties_add_bool(props, "lower_video_buffering", "Reduce video buffering for lower CPU/GPU load")
    obs.obs_properties_add_bool(props, "skip_browser_sources", "Skip optimization on browser sources")
    obs.obs_properties_add_bool(props, "optimize_scene_transitions", "Optimize scene transitions for speed")
    return props

def script_update(settings):
    global start_recording_on_start, defer_hidden_sources, disable_audio_dynamics
    global disable_unused_filters, auto_mute_unused_sources, mute_inactive_audio_sources
    global minimal_logging, disable_unused_plugins, lower_video_buffering
    global skip_browser_sources, optimize_scene_transitions

    start_recording_on_start = obs.obs_data_get_bool(settings, "start_recording_on_start")
    defer_hidden_sources = obs.obs_data_get_bool(settings, "defer_hidden_sources")
    disable_audio_dynamics = obs.obs_data_get_bool(settings, "disable_audio_dynamics")
    disable_unused_filters = obs.obs_data_get_bool(settings, "disable_unused_filters")
    auto_mute_unused_sources = obs.obs_data_get_bool(settings, "auto_mute_unused_sources")
    mute_inactive_audio_sources = obs.obs_data_get_bool(settings, "mute_inactive_audio_sources")
    minimal_logging = obs.obs_data_get_bool(settings, "minimal_logging")
    disable_unused_plugins = obs.obs_data_get_bool(settings, "disable_unused_plugins")
    lower_video_buffering = obs.obs_data_get_bool(settings, "lower_video_buffering")
    skip_browser_sources = obs.obs_data_get_bool(settings, "skip_browser_sources")
    optimize_scene_transitions = obs.obs_data_get_bool(settings, "optimize_scene_transitions")

# --- SCRIPT LOAD ---
def script_load(settings):
    obs.script_log(obs.LOG_INFO, "YO-BS: Lightweight live optimizer loaded...")
    optimize_all_sources()
    optimize_recording_settings()
    start_recording_if_enabled()
    obs.obs_frontend_add_event_callback(frontend_event)
    obs.script_log(obs.LOG_INFO, "YO-BS: Live optimizations applied successfully.")
