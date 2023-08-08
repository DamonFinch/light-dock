"""Tests for Initializer module"""

import pytest
from pathlib import Path
from lightdock.gso.initializer import (
    Initializer,
    RandomInitializer,
    FromFileInitializer,
    LightdockFromFileInitializer,
)
from lightdock.gso.parameters import GSOParameters
from lightdock.gso.searchspace.benchmark_ofunctions import J1
from lightdock.mathutil.lrandom import MTGenerator
from lightdock.gso.boundaries import Boundary, BoundingBox
from lightdock.error.lightdock_errors import GSOCoordinatesError
from lightdock.pdbutil.PDBIO import parse_complex_from_file
from lightdock.structure.complex import Complex
from lightdock.scoring.mj3h.driver import MJ3hAdapter, MJ3h


class TestInitializer:
    def test_create_from_interface(self):
        with pytest.raises(NotImplementedError):
            objective_function = J1()
            gso_parameters = GSOParameters()
            number_of_glowworms = 50
            initializer = Initializer(
                objective_function, number_of_glowworms, gso_parameters
            )
            swarm = initializer.generate_glowworms()

            assert swarm.get_size() > 0


class TestInitializerFromFile:
    def setup_class(self):
        self.path = Path(__file__).absolute().parent
        self.golden_data_path = self.path / "golden_data"

    def test_create_swarm(self):
        objective_function = J1()
        gso_parameters = GSOParameters()
        number_of_glowworms = 50
        initializer = FromFileInitializer(
            [objective_function],
            number_of_glowworms,
            gso_parameters,
            2,
            self.golden_data_path / "initial_positions.txt",
        )
        swarm = initializer.generate_glowworms()

        assert number_of_glowworms == swarm.get_size()
        assert (
            str(swarm.glowworms[-1])
            == "(0.617171, -2.85014)   5.00000000  0 0.200   0.00000000"
        )

    def test_generate_landscape_positions_without_coordinates(self):
        with pytest.raises(GSOCoordinatesError):
            objective_function = J1()
            gso_parameters = GSOParameters()
            number_of_glowworms = 50
            initializer = FromFileInitializer(
                [objective_function],
                number_of_glowworms,
                gso_parameters,
                2,
                self.golden_data_path / "initial_positions_empty.txt",
            )
            swarm = initializer.generate_glowworms()

            assert swarm.get_size() > 0

    def test_generate_landscape_positions_num_glowworms_different(self):
        with pytest.raises(GSOCoordinatesError):
            objective_function = J1()
            gso_parameters = GSOParameters()
            number_of_glowworms = 50
            initializer = FromFileInitializer(
                [objective_function],
                number_of_glowworms,
                gso_parameters,
                2,
                self.golden_data_path / "initial_positions_redux.txt",
            )
            swarm = initializer.generate_glowworms()

            assert swarm.get_size() > 0


class TestRandomInitializer:
    def setup_class(self):
        self.path = Path(__file__).absolute().parent
        self.golden_data_path = self.path / "golden_data"

    def test_create_swarm(self):
        objective_function = J1()
        gso_parameters = GSOParameters()
        number_of_glowworms = 15
        seed = 324324
        random_number_generator = MTGenerator(seed)
        bounding_box = BoundingBox([Boundary(1, 2), Boundary(10, 15)])
        initializer = RandomInitializer(
            [objective_function],
            number_of_glowworms,
            gso_parameters,
            bounding_box,
            random_number_generator,
        )
        swarm = initializer.generate_glowworms()

        assert number_of_glowworms == swarm.get_size()

        for glowworm in swarm.glowworms:
            coordinates = glowworm.landscape_positions[0].coordinates
            assert coordinates[0] < 2 and coordinates[0] >= 1
            assert coordinates[1] < 15 and coordinates[1] >= 10


class TestLightdockFromFileInitializer:
    def setup_class(self):
        self.path = Path(__file__).absolute().parent
        self.golden_data_path = self.path / "golden_data"
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1PPErec.pdb"
        )
        self.receptor = Complex(chains, atoms)
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1PPElig.pdb"
        )
        self.ligand = Complex(chains, atoms)
        self.adapter = MJ3hAdapter(self.receptor, self.ligand)
        self.scoring_function = MJ3h()

    def test_create_swarm(self):
        gso_parameters = GSOParameters()
        number_of_glowworms = 5
        seed = 324324
        random_number_generator = MTGenerator(seed)
        initializer = LightdockFromFileInitializer(
            [self.adapter],
            [self.scoring_function],
            number_of_glowworms,
            gso_parameters,
            7,
            self.golden_data_path / "initial_positions_1PPE.txt",
            0.5,
            0.5,
            random_number_generator,
            0.5,
            10,
            10,
        )
        swarm = initializer.generate_glowworms()

        assert number_of_glowworms == swarm.get_size()

    def test_generate_landscape_positions_without_coordinates(self):
        with pytest.raises(GSOCoordinatesError):
            gso_parameters = GSOParameters()
            number_of_glowworms = 5
            seed = 324324
            random_number_generator = MTGenerator(seed)
            initializer = LightdockFromFileInitializer(
                self.adapter,
                self.scoring_function,
                number_of_glowworms,
                gso_parameters,
                7,
                self.golden_data_path / "initial_positions_empty.txt",
                0.5,
                0.5,
                random_number_generator,
                0.5,
                10,
                10,
            )
            swarm = initializer.generate_glowworms()

            assert swarm.get_size() > 0

    def test_generate_landscape_positions_num_glowworms_different(self):
        with pytest.raises(GSOCoordinatesError):
            gso_parameters = GSOParameters()
            number_of_glowworms = 10
            seed = 324324
            random_number_generator = MTGenerator(seed)
            initializer = LightdockFromFileInitializer(
                self.adapter,
                self.scoring_function,
                number_of_glowworms,
                gso_parameters,
                7,
                self.golden_data_path / "initial_positions_1PPE.txt",
                0.5,
                0.5,
                random_number_generator,
                0.5,
                10,
                10,
            )
            swarm = initializer.generate_glowworms()

            assert swarm.get_size() > 0
