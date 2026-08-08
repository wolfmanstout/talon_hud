import logging
import time

from talon import Module, actions, app, scope, settings, speech_system

from .poller import Poller

mod = Module()
mod.setting(
    "talon_hud_show_rejected_commands",
    type=bool,
    default=True,
    desc="Show rejected speech in the HUD event log.",
)

# Handles state of phrases
# Inspired by the command history from knausj
class HistoryPoller(Poller):
    enabled = False
    content = None

    def enable(self):
    	if not self.enabled:
            self.enabled = True
            speech_system.register("phrase", self.on_phrase)

    def disable(self):
        self.enabled = False    
        speech_system.unregister("phrase", self.on_phrase)
            
    def on_phrase(self, j):
        log_type = "command"
        try:
            command = actions.user.history_transform_phrase_text(j.get("text"))
        except:
            if "text" in j and j["text"]:
                word_list = j["text"]
                command = " ".join(word for word in word_list)
            else:
                word_list = j["phrase"]
                command = " ".join(word.split("\\")[0] for word in word_list)

        # If no command but speech was recognized, show as rejected
        if command is None:
            if not settings.get("user.talon_hud_show_rejected_commands"):
                return
            # Skip rejections while Talon is asleep; they are not shown in the UI either.
            if "sleep" in scope.get("mode"):
                return
            emit_text = j.get("_metadata", {}).get("emit", "")
            if emit_text:
                logging.debug(f"Rejected command: {emit_text}")
                command = f"- {emit_text}"
                log_type = "warning"
            else:
                return

        self.content.add_log(log_type, command)
        
        # Debugging data
        time_ms = 0.0
        timestamp = time.time()
        model = "-"
        mic = actions.sound.active_microphone()
        if "_metadata" in j:
            meta = j["_metadata"]
            time_ms += meta["total_ms"] if "total_ms" in meta else 0
            time_ms += meta["audio_ms"] if "audio_ms" in meta else 0
            model = meta["desc"] if "desc" in meta else "-"
        
        metadata = {
            "phrase": command,
            "time_ms": time_ms,
            "timestamp": timestamp,
            "model": model,
            "microphone": mic
        }
        
        self.content.add_log("phrase", command, timestamp, metadata)
        
def on_ready():
    # This poller needs to be kept alive so that the phrases are properly registered
    actions.user.hud_add_poller("history", HistoryPoller(), True)

app.register("ready", on_ready)
