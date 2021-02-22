"""Regression tests for testing simulation setup using membrane"""

import shutil
import os
import filecmp
from pathlib import Path
from lightdock.test.bin.regression import RegressionTest


class TestSetupWithMembrane(RegressionTest):

    def __init__(self):
        super().__init__()
        self.path = Path(__file__).absolute().parent
        self.test_path = self.path / 'scratch_setup_membrane'
        self.golden_data_path = self.path / 'golden_data' / 'regression_setup_membrane'

    def setup(self):
        self.ini_test_path()
        shutil.copy(self.golden_data_path / 'receptor_membrane.pdb', self.test_path)
        shutil.copy(self.golden_data_path / 'ligand.pdb', self.test_path)

    def teardown(self):
        self.clean_test_path()

    def test_lightdock_setup_with_membrane_automatic(self):
        os.chdir(self.test_path)

        num_glowworms = 50

        command = f"lightdock3_setup.py receptor_membrane.pdb ligand.pdb -g {num_glowworms} --noxt --noh"
        command += " -membrane>> test_lightdock.out"
        os.system(command)

        assert filecmp.cmp(self.golden_data_path / 'init' / 'swarm_centers.pdb',
                           self.test_path / 'init' / 'swarm_centers.pdb')
        assert filecmp.cmp(self.golden_data_path / 'setup.json',
                           self.test_path / 'setup.json')
        assert filecmp.cmp(self.golden_data_path / 'init' / 'initial_positions_0.dat',
                           self.test_path / 'init' / 'initial_positions_0.dat')
        assert filecmp.cmp(self.golden_data_path / 'init' / 'initial_positions_35.dat',
                           self.test_path / 'init' / 'initial_positions_35.dat')
        assert filecmp.cmp(self.golden_data_path / 'init' / 'initial_positions_139.dat',
                           self.test_path / 'init' / 'initial_positions_139.dat')
        assert filecmp.cmp(self.golden_data_path / 'lightdock_receptor_membrane.pdb',
                           self.test_path / 'lightdock_receptor_membrane.pdb')
        assert filecmp.cmp(self.golden_data_path / 'lightdock_ligand.pdb',
                           self.test_path / 'lightdock_ligand.pdb')



class TestSetupWithMembraneAndRestraints(RegressionTest):

    def __init__(self):
        super().__init__()
        self.path = Path(__file__).absolute().parent
        self.test_path = self.path / 'scratch_setup_membrane_restraints'
        self.golden_data_path = self.path / 'golden_data' / 'regression_setup_membrane_restraints'

    def setup(self):
        self.ini_test_path()
        shutil.copy(self.golden_data_path / 'receptor_membrane.pdb', self.test_path)
        shutil.copy(self.golden_data_path / 'ligand.pdb', self.test_path)
        shutil.copy(self.golden_data_path / 'restraints.list', self.test_path)

    def teardown(self):
        self.clean_test_path()

    def test_lightdock_setup_with_membrane_automatic(self):
        os.chdir(self.test_path)

        num_glowworms = 50

        command = f"lightdock3_setup.py receptor_membrane.pdb ligand.pdb -g {num_glowworms} --noxt --noh"
        command += " -membrane -rst restraints.list >> test_lightdock.out"
        os.system(command)

        assert filecmp.cmp(self.golden_data_path / 'init' / 'swarm_centers.pdb',
                           self.test_path / 'init' / 'swarm_centers.pdb')
        assert filecmp.cmp(self.golden_data_path / 'setup.json',
                           self.test_path / 'setup.json')
        assert filecmp.cmp(self.golden_data_path / 'init' / 'initial_positions_0.dat',
                           self.test_path / 'init' / 'initial_positions_0.dat')
        assert filecmp.cmp(self.golden_data_path / 'init' / 'initial_positions_10.dat',
                           self.test_path / 'init' / 'initial_positions_10.dat')
        assert filecmp.cmp(self.golden_data_path / 'init' / 'initial_positions_20.dat',
                           self.test_path / 'init' / 'initial_positions_20.dat')
        assert filecmp.cmp(self.golden_data_path / 'init' / 'initial_positions_46.dat',
                           self.test_path / 'init' / 'initial_positions_46.dat')
        assert filecmp.cmp(self.golden_data_path / 'lightdock_receptor_membrane.pdb',
                           self.test_path / 'lightdock_receptor_membrane.pdb')
        assert filecmp.cmp(self.golden_data_path / 'lightdock_ligand.pdb',
                           self.test_path / 'lightdock_ligand.pdb')
