import time

from talon import actions, app, cron, tracking_system
from talon.track import tobii

from .poller import Poller


class EyeTrackerPoller(Poller):
    enabled = False
    content = None
    job = None
    latest_frame = None

    def enable(self):
        if not self.enabled:
            self.enabled = True
            # !!! Using unstable private API that may break at any time !!!
            tracking_system.register("gaze", self._on_gaze)
            self.job = cron.interval("200ms", self.eye_tracker_check)
            self.active = None
            self.active_icon = self.content.create_status_icon(
                "eye_tracker",
                "eyemouse",
                None,
                "Eye Tracker Active",
                lambda _, _2: None,
            )
            self.inactive_icon = self.content.create_status_icon(
                "eye_tracker",
                "no-camera",
                None,
                "Eye Tracker Inactive",
                lambda _, _2: None,
            )

    def disable(self):
        if self.enabled:
            self.enabled = False
            cron.cancel(self.job)
            self.job = None
            self.latest_frame = None
            # !!! Using unstable private API that may break at any time !!!
            tracking_system.unregister("gaze", self._on_gaze)
            self.content.publish_event("status_icons", "eye_tracker", "remove")

    def eye_tracker_check(self):
        active = bool(
            self.latest_frame and self.latest_frame.ts > time.perf_counter() - 0.5
        )
        if self.active is None or active != self.active:
            self.active = active
            status_icon = self.active_icon if active else self.inactive_icon
            self.content.publish_event(
                "status_icons", status_icon.topic, "replace", status_icon
            )

    def _on_gaze(self, frame: tobii.GazeFrame):
        if not frame or not frame.gaze:
            return
        self.latest_frame = frame


def add_statusbar_eye_tracker_icon(_=None):
    actions.user.hud_activate_poller("eye_tracker")


def remove_statusbar_eye_tracker_icon(_=None):
    actions.user.hud_deactivate_poller("eye_tracker")
    actions.user.hud_remove_status_icon("eye_tracker")


def register_eye_tracker_poller():
    actions.user.hud_add_poller("eye_tracker", EyeTrackerPoller())

    default_option = actions.user.hud_create_button(
        "Add Eye Tracker", add_statusbar_eye_tracker_icon, "eyemouse"
    )
    activated_option = actions.user.hud_create_button(
        "Remove Eye Tracker", remove_statusbar_eye_tracker_icon, "eyemouse"
    )
    status_option = actions.user.hud_create_status_option(
        "eye_tracker", default_option, activated_option
    )
    actions.user.hud_publish_status_option("eye_tracker_option", status_option)


app.register("ready", register_eye_tracker_poller)
