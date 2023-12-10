import json
import customtkinter as gui


class GPDWin4CP(gui.CTk):
    GYRO_CFG_PATH = '/home/arch/GPD/BMI260/gyro.json'
    SET_TDP_PATH = '/home/arch/GPD/TDP/set_tdp'
    TDP_LIM_PATH = '/home/arch/GPD/TDP/get_tdp_lim'

    def __init__(self):
        super().__init__()
        self.gyro_cfg = json.load(open(self.GYRO_CFG_PATH))
        self.last_tdp = int(open(self.TDP_LIM_PATH).read())

        self.title('GPD Win 4 Control Panel')
        self.geometry('300x310')
        self.resizable(False, True)

        self._init_tdp()
        self._init_gyro()
        self._init_exit()

    def _init_tdp(self):
        self.tdp_frame = gui.CTkFrame(self)
        self.tdp_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='NSEW')

        self.tdp_label = gui.CTkLabel(self.tdp_frame, text=f'TDP {self.last_tdp}w')
        self.tdp_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.tdp_slider = gui.CTkSlider(self.tdp_frame, from_=4, to=28, number_of_steps=24, command=self.tdp_slider_cb)
        self.tdp_slider.set(self.last_tdp)
        self.tdp_slider.grid(row=0, column=1, sticky='w')

    def _init_gyro(self):
        self.gyro_frame = gui.CTkFrame(self)
        self.gyro_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky='NSEW')

        self.gyro_label = gui.CTkLabel(self.gyro_frame, text='Gyro')
        self.gyro_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.gyro_enable = gui.CTkSwitch(self.gyro_frame, text='Enable', command=self.gyro_enable_cb)

        if self.gyro_cfg['enable']:
            self.gyro_enable.select()
        else:
            self.gyro_enable.deselect()

        self.gyro_enable.grid(row=0, column=1, sticky='w')

        self.gyro_mode_label = gui.CTkLabel(self.gyro_frame, text='Mode')
        self.gyro_mode_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.gyro_mode = gui.CTkComboBox(self.gyro_frame, values=['Mouse', 'Gamepad', 'gamepad_l', 'gamepad_r'], command=self.gyro_mode_cb)
        self.gyro_mode.set(self.gyro_cfg['mode'])
        self.gyro_mode.grid(row=1, column=1, sticky='w')

        self.gyro_sens_label = gui.CTkLabel(self.gyro_frame, text=f'Sens {self.gyro_cfg["sens"]}')
        self.gyro_sens_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.gyro_sens = gui.CTkSlider(self.gyro_frame, from_=0, to=1, number_of_steps=100, command=self.gyro_sens_slider_cb)
        self.gyro_sens.set(self.gyro_cfg['sens'])
        self.gyro_sens.grid(row=2, column=1, sticky='w')

        self.gyro_plane_label = gui.CTkLabel(self.gyro_frame, text='Plane')
        self.gyro_plane_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.gyro_plane = gui.CTkComboBox(self.gyro_frame, values=['XY', 'XZ'], command=self.gyro_plane_cb)
        self.gyro_plane.set(self.gyro_cfg['plane'].upper())
        self.gyro_plane.grid(row=3, column=1, sticky='w')

    def _init_exit(self):
        self.exit_but = gui.CTkButton(self, text='Ok', command=self.exit_cb)
        self.exit_but.grid(row=2, column=0, padx=10, pady=(10, 0), sticky='NSEW')

    def save_gyro(self):
        json.dump(self.gyro_cfg, open(self.GYRO_CFG_PATH, 'w'))

    def tdp_slider_cb(self, val):
        print(f'TDP: {int(val)}')
        self.tdp_label.configure(text=f'TDP {int(val)}w')
        open(self.SET_TDP_PATH, 'w').write(str(int(val)))

    def gyro_sens_slider_cb(self, val):
        self.gyro_cfg['sens'] = round(val, 2)
        self.gyro_sens_label.configure(text=f'Sens {self.gyro_cfg["sens"]}')
        self.save_gyro()
        print(f'sens: {self.gyro_cfg["sens"]}')

    def gyro_enable_cb(self):
        self.gyro_cfg['enable'] = not self.gyro_cfg['enable']
        self.save_gyro()
        print(f'enable: {self.gyro_cfg["enable"]}')

    def gyro_mode_cb(self, mode):
        self.gyro_cfg['mode'] = mode.lower()
        self.save_gyro()
        print(f'mode: {self.gyro_cfg["mode"]}')

    def gyro_plane_cb(self, plane):
        self.gyro_cfg['plane'] = plane.lower()
        self.save_gyro()
        print(f'plane: {self.gyro_cfg["plane"]}')

    def exit_cb(self):
        quit()


# settings
gui.set_appearance_mode('dark')
gui.set_default_color_theme('blue')

# app
app = GPDWin4CP()
app.mainloop()
