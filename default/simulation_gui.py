""" simple PyQt5 simulation controller """
import multiprocessing
#
# Copyright (C) 2017  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# or open http://www.fsf.org/licensing/licenses/gpl.html
#
import sys
from PyQt5 import QtWidgets

import galaxy_renderer, systemrenderer
from simulation_constants import END_MESSAGE
from PyQt5.Qt import QIntValidator, QSlider, QRegExp, QRegExpValidator
from PyQt5 import  QtGui, uic, QtWidgets
from multiprocessing import Manager

class SimulationGUI(QtWidgets.QDialog):
    """
        Implementing simulation_ui.ui and connecting the buttons (exitProgramm does not work for some reason)
    """
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        
        float_ex = QRegExp("[0-9]+[.]?[0-9]{1,2}")
        float_validator = QRegExpValidator(float_ex)
        
        self.ui = uic.loadUi('simulator_ui.ui')
        self.ui.startSimulation.clicked.connect(self.start_simulation)
        self.ui.stopSimulation.clicked.connect(self.stop_simulation)
        self.ui.exitProgramm.clicked.connect(self.exit_application)
        
        self.ui.slider.valueChanged.connect(self.update_slider_label)
        
        self.ui.stepScale.editingFinished.connect(self.update_slider)
        self.ui.stepScale.setValidator(QIntValidator())
        
        self.ui.slider_label.editingFinished.connect(self.slider_label_changed)
        self.ui.slider_label.setValidator(float_validator)
        
        self.renderer_conn, self.simulation_conn = None, None
        self.render_process = None
        self.simulation_process = None
        multiprocessing.set_start_method('spawn')
        
        self.manager = Manager()
        self.step_scale = self.manager.Value('int', 0)
        
        self.update_slider_label()
        
    def start_simulation(self):
        """
            Start simulation and render process connected with a pipe.
            Collects User Input from the UI and sends it to the SystemGenerator
        """
        bodyCount =  int(self.ui.bodyCount.text())
        minMass  = int(self.ui.minMass.text())* (10 ** int(self.ui.minMassPot.text()))
        maxMass  = int(self.ui.maxMass.text())* (10  ** int(self.ui.maxMassPot.text()))
        minRad = int(self.ui.minRad.text())* (10  ** int(self.ui.minRadPot.text()))
        maxRad = int(self.ui.maxRad.text())* (10  ** int(self.ui.maxRadPot.text()))
        centerMass = int(self.ui.centerMass.text())* (10  ** int(self.ui.centerMassPot.text()))
        centerRad = int(self.ui.centerRad.text())* (10 ** int(self.ui.centerRadPot.text()))
        scale = int(self.ui.scale.text())* (10  ** int(self.ui.scalePot.text()))
        
        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = \
            multiprocessing.Process(target=systemrenderer.startup,
                                    args=(self.simulation_conn, bodyCount, minMass, maxMass, minRad, maxRad, centerMass, centerRad, scale, self.step_scale))
        self.render_process = \
            multiprocessing.Process(target=galaxy_renderer.startup,
                                    args=(self.renderer_conn, 60))
        self.simulation_process.start()
        self.render_process.start()
        
        self.set_enabled_for_gen_buttons(False)

    def stop_simulation(self):
        """
            Stop simulation and render process by sending END_MESSAGE
            through the pipes.
        """
        if self.simulation_process is not None:
            self.simulation_conn.send(END_MESSAGE)
            self.simulation_process = None

        if self.render_process is not None:
            self.renderer_conn.send(END_MESSAGE)
            self.render_process = None
            
        self.set_enabled_for_gen_buttons(True)

    def exit_application(self):
        """
            Stop simulation and exit.
        """
        self.stop_simulation()
        self.close()
        
    def update_slider(self):
        step_scale = float(self.ui.stepScale.text())
        slider_label_value = float(self.ui.slider_label.text())
        
        percentage = 0
        
        if slider_label_value != 0:
            percentage = slider_label_value / step_scale
            
        self.ui.slider.setValue(percentage*100)
        
    def update_slider_label(self):
        stepValue = float(self.ui.stepScale.text())
        sliderValue = (float(self.ui.slider.value()))/100
        self.step_scale.value = sliderValue*stepValue
        self.ui.slider_label.setText("{0:.2f}".format(self.step_scale.value))
        
    def slider_label_changed(self):
        #get value of slider label
        self.step_scale.value = float(self.ui.slider_label.text())
        #get value of step scale
        stepScaleValue = float(self.ui.stepScale.text())
        
        if self.step_scale.value > stepScaleValue:
            stepScaleValue = self.step_scale.value
            self.ui.stepScale.setText(str(stepScaleValue))
            
        new_slider_value = self.step_scale.value/stepScaleValue*100
        self.ui.slider.setValue(new_slider_value)
        
        
    def set_enabled_for_gen_buttons(self, value):
        self.ui.bodyCount.setEnabled(value)
        self.ui.minMass.setEnabled(value)
        self.ui.minMassPot.setEnabled(value)
        self.ui.maxMass.setEnabled(value)
        self.ui.maxMassPot.setEnabled(value)
        self.ui.minRad.setEnabled(value)
        self.ui.minRadPot.setEnabled(value)
        self.ui.maxRad.setEnabled(value)
        self.ui.maxRadPot.setEnabled(value)
        self.ui.centerMass.setEnabled(value)
        self.ui.centerMassPot.setEnabled(value)
        self.ui.centerRad.setEnabled(value)
        self.ui.centerRadPot.setEnabled(value)
        self.ui.scale.setEnabled(value)
        self.ui.scalePot.setEnabled(value)

def _main(argv):
    """
        Main function to avoid pylint complains concerning constant names.
    """
    app = QtWidgets.QApplication(argv)
    simulation_gui = SimulationGUI()
    simulation_gui.ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    _main(sys.argv)
