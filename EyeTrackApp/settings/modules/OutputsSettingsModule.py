from config import EyeTrackSettingsConfig
from settings.modules.BaseModule import BaseSettingsModule, BaseValidationModel
import PySimpleGUI as sg

from utils.misc_utils import resource_user_data_folder


class OutputsSettingsValidationModel(BaseValidationModel):
	gui_should_save_video_right: bool
	gui_should_save_video: bool
	gui_video_save_path_right: str
	gui_video_save_path: str
    # gui_flip_x_axis_right: bool
    # gui_flip_y_axis: bool
    # gui_outer_side_falloff: bool
    # gui_update_check: bool
    # gui_right_eye_dominant: bool
    # gui_left_eye_dominant: bool
    # gui_eye_dominant_diff_thresh: float


class OutputsSettingsModule(BaseSettingsModule):
    def __init__(self, config, widget_id, **kwargs):
        super().__init__(config=config, widget_id=widget_id, **kwargs)
        self.validation_model = OutputsSettingsValidationModel
        self.gui_should_save_video = f"-SHOULDSAVEVIDEO{widget_id}-"
        self.gui_should_save_video_right = f"-SHOULDSAVEVIDEORIGHT{widget_id}-"
        self.gui_video_save_path = f"-VIDEOSAVEPATH{widget_id}-"
        self.gui_video_save_path_right = f"-VIDEOSAVEPATHRIGHT{widget_id}-"
        # self.gui_flip_y_axis = f"-FLIPYAXIS{widget_id}-"
        # self.gui_outer_side_falloff = f"-EYEFALLOFF{widget_id}-"
        # self.gui_eye_dominant_diff_thresh = f"-DIFFTHRESH{widget_id}-"
        # self.gui_left_eye_dominant = f"-LEFTEYEDOMINANT{widget_id}-"
        # self.gui_right_eye_dominant = f"-RIGHTEYEDOMINANT{widget_id}-"
        # self.gui_update_check = f"-UPDATECHECK{widget_id}-"

    # gui_right_eye_dominant: bool = False
    # gui_left_eye_dominant: bool = False
    # gui_outer_side_falloff: bool = True
    # gui_eye_dominant_diff_thresh: float = 0.3

    def get_layout(self):        
        return [
            [
                sg.Text("Output Settings:", background_color="#242224"),
            ],
            [
                sg.Checkbox(
                    "Save Left Eye Video",
                    default=self.config.gui_should_save_video,
                    key=self.gui_should_save_video,
                    background_color="#424042",
                    tooltip="Toggles whether to save recieved video frames for the Right eye.",
                ),
                sg.Checkbox(
                    "Save Right Eye Video",
                    default=self.config.gui_should_save_video_right,
                    key=self.gui_should_save_video_right,
                    background_color="#424042",
                    tooltip="Toggles whether to save recieved video frames for the Left eye.",
                ),
            ],
			[
                sg.Text("Left Video Save Path:", background_color="#242224"),
                sg.InputText(
                    self.config.gui_video_save_path,
                    key=self.gui_video_save_path,
                    size=(20, 10),
                    tooltip="Path to save video frames to for the Right eye.",
                ),
            ],
			[
                sg.Text("Right Video Save Path:", background_color="#242224"),
                sg.InputText(
                    self.config.gui_video_save_path_right,
                    key=self.gui_video_save_path_right,
                    size=(40, 10),
                    tooltip="Path to save video frames to for the Left eye.",
                ),
            ],
            
        ]
