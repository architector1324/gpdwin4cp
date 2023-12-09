import json
import customtkinter as gui


class GPDWin4CP(gui.CTk):
    GYRO_CFG_PATH = '/home/arch/GPD/BMI260/gyro.json'

    def __init__(self):
        super().__init__()
        self.gyro_cfg = json.load(open(self.GYRO_CFG_PATH))
        self.last_tdp = int(open('/home/arch/GPD/TDP/get_tdp_lim').read())

        self.geometry('320x200')
        self.title('GPD Win 4 Control Panel')

        self._init_tdp()
        self._init_gyro()

    def _init_tdp(self):
        self.tdp_label = gui.CTkLabel(self, text=f'TDP {self.last_tdp}w')
        self.tdp_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.tdp_slider = gui.CTkSlider(self, from_=4, to=28, number_of_steps=24, width=230, command=self.tdp_slider_cb)
        self.tdp_slider.set(self.last_tdp)
        self.tdp_slider.grid(row=0, column=1, sticky='w')

    def _init_gyro(self):
        self.gyro_label = gui.CTkLabel(self, text='Gyro')
        self.gyro_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.gyro_enable = gui.CTkCheckBox(self, text='Enable', command=self.gyro_enable_cb)
        self.gyro_enable._check_state = self.gyro_cfg['enable']
        self.gyro_enable.grid(row=1, column=1, sticky='w')

        self.gyro_mode_label = gui.CTkLabel(self, text='Mode')
        self.gyro_mode_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.gyro_mode = gui.CTkComboBox(self, values=['Mouse', 'Gamepad'], command=self.gyro_mode_cb)
        self.gyro_mode.grid(row=2, column=1, sticky='w')

        self.gyro_sens_label = gui.CTkLabel(self, text=f'Sens {self.gyro_cfg["sens"]}')
        self.gyro_sens_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.gyro_sens = gui.CTkSlider(self, from_=0, to=1, number_of_steps=100, width=230, command=self.gyro_sens_slider_cb)
        self.gyro_sens.set(self.gyro_cfg['sens'])
        self.gyro_sens.grid(row=3, column=1, sticky='w')

    def save_gyro(self):
        json.dump(self.gyro_cfg, open(self.GYRO_CFG_PATH, 'w'))

    def tdp_slider_cb(self, val):
        print(f'TDP: {int(val)}')
        self.tdp_label.configure(text=f'TDP {int(val)}w')
        open('/home/arch/GPD/TDP/set_tdp', 'w').write(str(int(val)))

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


# settings
gui.set_appearance_mode('dark')
gui.set_default_color_theme('blue')

# app
app = GPDWin4CP()
app.mainloop()
